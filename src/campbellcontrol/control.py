import logging
import time
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Any, Optional

from awscrt.mqtt import QoS
from paho.mqtt.client import Client, MQTTMessage

from campbellcontrol.commands import Command, CommandResponse
from campbellcontrol.connection.interface import Connection

logger = logging.getLogger(__name__)


class CommandHandler(ABC):
    client: Connection
    command: Command
    response: Any = None

    def __init__(self, client: Connection):
        self.client = client

    @abstractmethod
    def handle_response(self, *args, **kwargs) -> None:
        """Handle the response from the logger."""

    @abstractmethod
    def send_command(self, *args, **kwargs) -> None:
        """Send a command to the logger."""


class PahoCommandHandler(CommandHandler):
    def handle_response(self, client: Client, userdata: Any, msg: MQTTMessage) -> None:
        """Handle the response from the logger."""
        response = self.command.handler(msg.topic, msg.payload)

        if response:
            self.response = response

    def send_command(self, command: Command, *args, timeout: int = 20, **kwargs) -> Optional[CommandResponse]:
        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=timeout)
        self.command = command
        self.response = None
        self.client.connect()

        payload = command.json_payload(*args, **kwargs)
        topic = command.publish_topic
        self.client.client.on_message = self.handle_response
        self.client.subscribe(command.response_topic)
        self.client.client.loop_start()
        self.client.publish(topic, payload)

        while not self.response:
            if datetime.now() > end_time:
                logger.info("Timeout waiting for response")
                break
            time.sleep(0.1)

        self.client.client.loop_stop()
        self.client.disconnect()
        if self.response:
            if self.response["success"]:
                logger.info("Command executed successfully")
            else:
                logger.info("Command execution failed")
            return self.response


class AWSCommandHandler(CommandHandler):
    def handle_response(self, topic: str, payload: bytes, dup: bool, qos: QoS, retain: bool, **kwargs) -> None:
        response = self.command.handler(topic, payload)

        if response:
            self.response = response

    def send_command(self, command: Command, *args, timeout: int = 30, **kwargs) -> Optional[CommandResponse]:
        """Send a command to the logger."""
        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=timeout)

        self.command = command
        self.response = None

        self.client.connect()
        payload = command.json_payload(*args, **kwargs)
        topic = command.publish_topic
        self.client.subscribe(command.response_topic, qos=QoS.EXACTLY_ONCE, callback=self.handle_response)
        self.client.publish(topic, payload, QoS.AT_LEAST_ONCE)

        while not self.response:
            if datetime.now() > end_time:
                logger.info("Timeout waiting for response")
                break
            time.sleep(0.1)

        self.client.disconnect()

        if self.response:
            if self.response["success"]:
                logger.info("Command executed successfully")
            else:
                logger.info("Command execution failed")
            return self.response
