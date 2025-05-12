"""Module for handling generic MQTT clients"""

import logging
from typing import Any, List

from paho.mqtt.client import CallbackAPIVersion, Client, ConnectFlags, MQTTMessage
from paho.mqtt.properties import Properties
from paho.mqtt.reasoncodes import ReasonCode

from campbellcontrol.connection.interface import Connection

logger = logging.getLogger(__name__)


class PahoConnection(Connection):
    """Connection class for the generic Paho MQTT client."""

    def get_client(self, *args, **kwargs) -> Client:
        """Return the Paho MQTT client instance."""
        client = Client(CallbackAPIVersion.VERSION2, *args, **kwargs)
        client.on_message = self._on_message
        client.on_connect = self._on_connect
        client.on_disconnect = self._on_disconnect
        client.on_subscribe = self._on_subscribe
        client.on_unsubscribe = self._on_unsubscribe

        return client

    @staticmethod
    def _on_connect(
        client: Client,
        userdata: Any,
        flags: ConnectFlags,
        reason_code: ReasonCode,
        properties: Properties,
    ) -> None:
        """Method called when the client connects to the broker.
        Args:
            client: The client instance.
            userdata: User data passed to the callback.
            flags: Response flags from the broker.
            reason_code: The reason code for the connection.
            properties: Properties of the connection.
        """
        logger.info(f"Connected with result code {reason_code}")

    @staticmethod
    def _on_disconnect(
        client: Client,
        userdata: Any,
        flags: ConnectFlags,
        reason_code: ReasonCode,
        properties: Properties,
    ) -> None:
        """Method called when the client disconnects from the broker.
        Args:
            client: The client instance.
            userdata: User data passed to the callback.
            flags: Response flags from the broker.
            reason_code: The reason code for the disconnection.
            properties: Properties of the connection.
        """
        if reason_code != 0:
            logger.error(f"Unexpected disconnection: {reason_code}")
        else:
            logger.info("Disconnected successfully")

    @staticmethod
    def _on_message(client: Client, userdata: Any, msg: MQTTMessage) -> None:
        """Method called when a message is received from the broker on and subscribed topic.
        Args:
            client: The client instance.
            userdata: User data passed to the callback.
            msg: The message received from the broker.
        """
        logger.info(f"Default message handler: {msg.topic}, {msg.payload}")

    @staticmethod
    def _on_subscribe(
        client: Client,
        userdata: Any,
        mid: int,
        reason_code_list: List[ReasonCode],
        properties: Properties,
    ) -> None:
        """Method called when the client subscribes to a topic.
        Args:
            client: The client instance.
            userdata: User data passed to the callback.
            mid: Message ID for the request.
            reason_code_list: A list of reason codes.
            properties: Properties of the connection.
        """
        logger.info(f"Subscribed: {mid} {reason_code_list} {properties}")

    @staticmethod
    def _on_unsubscribe(
        client: Client,
        userdata: Any,
        mid: int,
        reason_code_list: List[ReasonCode],
        properties: Properties,
    ) -> None:
        """Method called when the client unsubscribes from a topic.
        Args:
            client: The client instance.
            userdata: User data passed to the callback.
            mid: Message ID for the request.
            reason_code_list: A list of reason codes.
            properties: Properties of the connection.
        """
        logger.info(f"Unsubscribed: {mid} {reason_code_list} {properties}")
