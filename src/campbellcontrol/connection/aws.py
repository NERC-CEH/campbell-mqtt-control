"""Module for AWS specific MQTT broker connections"""

import logging
from typing import Callable

import awscrt.mqtt
from awscrt.exceptions import AwsCrtError
from awscrt.mqtt import (
    Client,
    ConnectReturnCode,
    OnConnectionClosedData,
    OnConnectionFailureData,
    OnConnectionSuccessData,
    QoS,
)

from campbellcontrol.connection.interface import Connection

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class AWSConnection(Connection):
    """Connection class for the AWS MQTT client."""

    client_id: str
    """The client ID used for the MQTT connection (important for IoT Core authentication)."""

    def __init__(self, client_id: str, *args, **kwargs) -> None:
        """Initialize the AWSConnection instance.

        Args:
            client_id: The client ID used for the MQTT connection.
        """
        self.client_id = client_id
        super().__init__(*args, **kwargs)

    def get_client(self, *args, **kwargs) -> awscrt.mqtt.Connection:
        """Return the AWS MQTT client instance.

        Args:
            *args: Additional arguments forwarded to the client.
            **kwargs: Additional keyword arguments forwarded to the client.
        """
        client = Client()
        connection = awscrt.mqtt.Connection(
            client,
            self.endpoint,
            self.port,
            self.client_id,
            *args,
            on_connection_interrupted=self._on_connection_interrupted,
            on_connection_resumed=self._on_connection_resumed,
            on_connection_success=self._on_connection_success,
            on_connection_failure=self._on_connection_failure,
            on_connection_closed=self._on_connection_closed,
            **kwargs,
        )
        connection.on_message(self._on_message)
        return connection

    def connect(self) -> None:
        """Connect to the MQTT broker."""
        future = self.client.connect()
        try:
            future.result()
        except AwsCrtError as err:
            raise ConnectionError(err)

    def disconnect(self) -> None:
        """Disconnect from the MQTT broker."""
        future = self.client.disconnect()
        future.result()

    def subscribe(self, topic: str, qos: QoS = QoS.EXACTLY_ONCE, callback: Callable | None = None) -> None:
        """Subscribe to a topic.

        Args:
            topic: The topic to subscribe to.
            qos: The Quality of Service level for the subscription.
            callback: Optional method that is called during subscription.
        """

        future, _ = self.client.subscribe(topic=topic, qos=qos, callback=callback)

        result = future.result()
        exception = future.exception()

        if exception:
            logger.error("Subscription failed. error: {}".format(exception))
            return
        logger.info("Subscription successful. result: {}".format(result))

    def publish(
        self,
        topic: str,
        payload: str | bytes | bytearray,
        qos: QoS,
        retain: bool = False,
    ) -> None:
        """Publish a message to a given topic.

        Args:
            topic: The topic to publish to.
            payload: The message payload.
            qos: The Quality of Service level for the publication.
            retain: Whether to retain the message on the broker and deliver it to future subscribers.
        """

        future, _ = self.client.publish(topic=topic, payload=payload, qos=qos, retain=retain)
        future.result()

    @staticmethod
    def _on_connection_interrupted(connection: awscrt.mqtt.Connection, error: AwsCrtError, **kwargs) -> None:
        """Method called when the connection is interrupted.

        Args:
            connection: The connection instance.
            error: The error that caused the interruption.
        """
        logger.error("Connection interrupted. error: {}".format(error))

    @staticmethod
    def _on_connection_resumed(
        connection: awscrt.mqtt.Connection,
        return_code: ConnectReturnCode,
        session_present: bool,
        **kwargs,
    ) -> None:
        """Method called when the connection is resumed.

        Args:
            connection: The connection instance.
            return_code: The return code from the broker.
            session_present: Whether the session is present.
        """
        logger.info("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))

    @staticmethod
    def _on_connection_success(connection: awscrt.mqtt.Connection, callback_data: OnConnectionSuccessData) -> None:
        """Method called when the connection is successful.

        Args:
            connection: The connection instance.
            callback_data: Data related to the successful connection.
        """
        logger.info("Connection successful. callback_data: {}".format(callback_data))

    @staticmethod
    def _on_connection_failure(connection: awscrt.mqtt.Connection, callback_data: OnConnectionFailureData) -> None:
        """Method called when the connection fails.

        Args:
            connection: The connection instance.
            callback_data: Data related to the failed connection.
        """
        logger.error("Connection failed. callback_data: {}".format(callback_data))

    @staticmethod
    def _on_connection_closed(connection: awscrt.mqtt.Connection, callback_data: OnConnectionClosedData) -> None:
        """Method called when the connection is closed.

        Args:
            connection: The connection instance.
            callback_data: Data related to the closed connection.
        """
        logger.info("Connection closed. callback_data: {}".format(callback_data))

    @staticmethod
    def _on_message(topic: str, payload: bytes, dup: bool, qos: QoS, retain: bool, **kwargs) -> None:
        """Method called when a message is received from the broker on a subscribed topic.

        Args:
            topic: The topic of the message.
            payload: The message payload.
            dup: Whether the message is a duplicate.
            qos: The Quality of Service level of the message.
            retain: Whether the message is retained on the broker.
        """
        logger.info(f"Received message from topic: {topic} with payload: {payload.decode()}")
