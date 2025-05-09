import time
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Any

from paho.mqtt.client import Client, MQTTMessage

from campbellcontrol.commands import Command
from campbellcontrol.connection.interface import Connection


class CommandHandler(ABC):
    client: Connection
    response: str = None

    def __init__(self, client: Connection):
        self.client = client

    @abstractmethod
    def handle_response(self, command: Command, *args, **kwargs) -> None:
        """Handle the response from the logger."""

    @abstractmethod
    def send_command(self, command: Command, *args, **kwargs) -> None:
        """Send a command to the logger."""


class PahoCommandHandler(CommandHandler):
    command: Command
    response: Any = None

    def handle_response(self, client: Client, userdata: Any, msg: MQTTMessage) -> None:
        """Handle the response from the logger."""
        response = self.command.handler(msg.topic, msg.payload)

        if response:
            self.response = response

    def send_command(self, command: Command, *args, timeout: int = 10, **kwargs) -> None:
        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=timeout)
        self.command = command
        self.client.connect()

        payload = command.json_payload(*args, **kwargs)
        topic = command.publish_topic
        self.client.client.on_message = self.handle_response
        self.client.subscribe(command.response_topic)
        self.client.client.loop_start()
        self.client.publish(topic, payload)

        while not self.response:
            if datetime.now() > end_time:
                print("Timeout waiting for response")
                break
            time.sleep(0.1)

        self.client.client.loop_stop()
        self.client.disconnect()
        if self.response:
            if self.response["success"]:
                print("Command executed successfully")
            else:
                print("Command execution failed")

            print("Response:", self.response)
