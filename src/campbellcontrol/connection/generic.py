import logging
from typing import Any, Callable, Dict, List

from paho.mqtt.client import CallbackAPIVersion, Client, ConnectFlags, MQTTMessage
from paho.mqtt.properties import Properties
from paho.mqtt.reasoncodes import ReasonCode

from campbellcontrol.connection.interface import Connection

logger = logging.getLogger(__name__)


class PahoConnection(Connection):
    """MQTT connection using the Paho MQTT client."""

    topic_handlers: Dict[str, Callable]
    response: Any = None

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
        logger.info(f"Connected with result code {reason_code}")

    @staticmethod
    def _on_disconnect(
        client: Client,
        userdata: Any,
        flags: ConnectFlags,
        reason_code: ReasonCode,
        properties: Properties,
    ) -> None:
        if reason_code != 0:
            logger.error(f"Unexpected disconnection: {reason_code}")
        else:
            logger.info("Disconnected successfully")

    def _on_message(self, client: Client, userdata: Any, msg: MQTTMessage) -> None:
        logger.info(f"Default message handler: {msg.topic}, {msg.payload}")
        self.response = msg.payload

    @staticmethod
    def _on_subscribe(
        client: Client,
        userdata: Any,
        mid: int,
        reason_code_list: List[ReasonCode],
        properties: Properties,
    ) -> None:
        """Callback for when a subscription is made."""
        logger.info(f"Subscribed: {mid} {reason_code_list} {properties}")

    @staticmethod
    def _on_unsubscribe(
        client: Client,
        userdata: Any,
        mid: int,
        reason_code_list: List[ReasonCode],
        properties: Properties,
    ) -> None:
        """Callback for when an unsubscription is made."""
        logger.info(f"Unsubscribed: {mid} {reason_code_list} {properties}")
