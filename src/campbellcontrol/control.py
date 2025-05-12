"""Module for sending commands and receiving responses from loggers."""

import logging
import time
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Any, Optional

from awscrt.mqtt import QoS
from paho.mqtt.client import Client, MQTTMessage

from campbellcontrol.commands.commands import Command, CommandResponse
from campbellcontrol.connection.interface import Connection

logger = logging.getLogger(__name__)


class CommandHandler(ABC):
    """Interface class for command/response handling.
    Different MQTT client objects have different signatures
    for the "on_message" method that must be reduced down to a
    "topic" and "message" to be processed by the current command instance.
    There are also different invocations for sending/receiving a command, so
    multiple CommandHandler classes are needed.
    """

    client: Connection
    """Handle to the broker connection client object."""

    command: Optional[Command] = None
    """The current control command being sent/received."""

    response: Optional[Any] = None
    """The latest response. Used to break out of wait state."""

    def __init__(self, client: Connection) -> None:
        """Initialize the instance.
        Args:
            client: A MQTT client object.
        """
        self.client = client

    def handle_response(self, *args, **kwargs) -> None:
        """Forwards arguments to the command's handler method."""
        response = self.command.handler(*args, **kwargs)

        if response:
            self.response = response

    def reset(self) -> None:
        """Resets the stateful attributes."""
        self.command = None
        self.response = None

    def send_command(self, command: Command, *args, timeout: int = 20, **kwargs) -> Optional[CommandResponse]:
        """Invokes a given MQTT command and awaits the response until timeout is reached.
        Args:
            command: The specified Campbell compatible command.
            *args: Arguments to pass to the given command.
            timeout: Time in seconds before the command aborts.
            **kwargs: Keyword arguments passed to the command.
        Returns:
            A CommandResponse dictionary if a response is received, otherwise None.
        """
        self.reset()

        # Setting up the instance to track the command
        end_time = datetime.now() + timedelta(seconds=timeout)
        self.command = command
        payload = command.json_payload(*args, **kwargs)

        self.client.connect()
        self._initiate_send(command, payload)

        # Blocking wait until a response is received or timeout reached
        while not self.response:
            if datetime.now() > end_time:
                logger.info("Timeout waiting for response")
                break
            time.sleep(0.1)

        self._terminate_send(command)
        self.client.disconnect()

        # Report outcome
        if self.response:
            if self.response["success"]:
                logger.info("Command executed successfully")
            else:
                logger.info("Command execution failed")
            return self.response

    @abstractmethod
    def _initiate_send(self, command: Command, payload: dict) -> None:
        """Prepares client, sends command, and subscribes to the result.
        Args:
            command: The command the send.
            payload: Payload to send.
        """

    @abstractmethod
    def _terminate_send(self, command: Command) -> None:
        """Restores the client to the prior state, unsubscribes from topics.
        Args:
            command: The command that was sent.
        """


class PahoCommandHandler(CommandHandler):
    """Handler class for the generic PAHO based clients."""

    def handle_response(self, client: Client, userdata: Any, msg: MQTTMessage) -> None:
        """Forwards message topic and payload for a message from a logger to
            the command response handler.
        Args:
            client: The MQTT client.
            userdata: Data defined by the user.
            msg: The received message.
        """
        super().handle_response(msg.topic, msg.payload)

    def _initiate_send(self, command: Command, payload: dict) -> None:
        """Prepares client, sends command, and subscribes to the result.
        Args:
            command: The command the send.
            payload: Payload to send.
        """

        # Setting callback handler
        self.client.client.on_message = self.handle_response

        # Subscribing to response topic
        self.client.subscribe(command.response_topic)

        # Starting listening behaviour
        self.client.client.loop_start()

        # Sending the command
        self.client.publish(command.publish_topic, payload)

    def _terminate_send(self, command: Command) -> None:
        """Restores the client to the prior state, unsubscribes from topics,
            ends listen behaviour.
        Args:
            command: The command that was sent.
        """
        self.client.client.loop_stop()
        self.client.unsubscribe(command.response_topic)


class AWSCommandHandler(CommandHandler):
    def handle_response(self, topic: str, payload: bytes, dup: bool, qos: QoS, retain: bool, **kwargs) -> None:
        super().handle_response(topic, payload)

    def _initiate_send(self, command: Command, payload: dict) -> None:
        """Prepares client, sends command, and subscribes to the result.
        Args:
            command: The command the send.
            payload: Payload to send.
        """
        self.client.subscribe(command.response_topic, qos=QoS.EXACTLY_ONCE, callback=self.handle_response)
        self.client.publish(command.publish_topic, payload, QoS.AT_LEAST_ONCE)

    def _terminate_send(self, command: Command) -> None:
        """Restores the client to the prior state, unsubscribes from topics.
        Args:
            command: The command that was sent.
        """
        self.client.unsubscribe(command.response_topic)
