import logging
from typing import Any, List

from paho.mqtt.client import CallbackAPIVersion, Client, ConnectFlags, MQTTMessage
from paho.mqtt.properties import Properties
from paho.mqtt.reasoncodes import ReasonCode

from campbellcontrol.connection.interface import Connection

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class PahoConnection(Connection):
    """MQTT connection using the Paho MQTT client."""

    @classmethod
    def get_client(cls, *args, **kwargs) -> Client:
        """Return the Paho MQTT client instance."""
        client = Client(CallbackAPIVersion.VERSION2, *args, **kwargs)
        client.on_message = cls._on_message
        client.on_connect = cls._on_connect
        client.on_disconnect = cls._on_disconnect
        client.on_subscribe = cls._on_subscribe
        client.on_unsubscribe = cls._on_unsubscribe

        return client

    @staticmethod
    def _on_connect(
        client: Client,
        userdata: Any,
        flags: ConnectFlags,
        reason_code: ReasonCode,
        properties: Properties,
    ) -> None:
        logging.info(f"Connected with result code {reason_code}")

    @staticmethod
    def _on_disconnect(
        client: Client,
        userdata: Any,
        flags: ConnectFlags,
        reason_code: ReasonCode,
        properties: Properties,
    ) -> None:
        if reason_code != 0:
            logging.error(f"Unexpected disconnection: {reason_code}")
        else:
            logging.info("Disconnected successfully")

    @staticmethod
    def _on_message(client: Client, userdata: Any, msg: MQTTMessage) -> None:
        logging.info(msg.topic + " " + str(msg.payload))

    @staticmethod
    def _on_subscribe(
        client: Client,
        userdata: Any,
        mid: int,
        reason_code_list: List[ReasonCode],
        properties: Properties,
    ) -> None:
        """Callback for when a subscription is made."""
        logging.info(f"Subscribed: {mid} {reason_code_list}")

    @staticmethod
    def _on_unsubscribe(
        client: Client,
        userdata: Any,
        mid: int,
        reason_code_list: List[ReasonCode],
        properties: Properties,
    ) -> None:
        """Callback for when an unsubscription is made."""
        logging.info(f"Unsubscribed: {mid} {reason_code_list}")
