"""Module for AWS specific MQTT broker connections"""

import logging
from typing import Callable

import awscrt.mqtt
from awscrt import io
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

    def get_client_bootstrap(self) -> io.ClientBootstrap:
        """
        "The ClientBootstrap will default to the static default (Io.ClientBootstrap.get_or_create_static_default)"
        https://awslabs.github.io/aws-crt-python/api/io.html#awscrt.io.ClientBootstrap
        This example is from the mqtt_test.py util in the aws-crt-python repo.
        TODO - understand how this works.
        """
        return None
        event_loop_group = io.EventLoopGroup(1)
        host_resolver = io.DefaultHostResolver(event_loop_group)
        client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
        return client_bootstrap

    def get_client(self, *args, **kwargs) -> awscrt.mqtt.Connection:
        """Return the AWS MQTT client instance.

        Args:
            *args: Additional arguments forwarded to the client.
            **kwargs: Additional keyword arguments forwarded to the client.
        """
        client_bootstrap = self.get_client_bootstrap()

        tls_context = None
        if self.port == 8883:
            assert kwargs.get("private_key")
            assert kwargs.get("public_key")

            tls_context = self._tls_context(
                cert=kwargs["public_key"],
                key=kwargs["private_key"],
                root_ca=kwargs.get("certificate_root", "CARoot.pem"),
            )

        del kwargs["public_key"]
        del kwargs["private_key"]
        del kwargs["certificate_root"]
        client = Client(client_bootstrap, tls_context)
        connection = awscrt.mqtt.Connection(
            client,
            *args,
            host_name=self.endpoint,
            port=self.port,
            client_id=self.client_id,
            on_connection_interrupted=self._on_connection_interrupted,
            on_connection_resumed=self._on_connection_resumed,
            on_connection_success=self._on_connection_success,
            on_connection_failure=self._on_connection_failure,
            on_connection_closed=self._on_connection_closed,
            **kwargs,
        )
        connection.on_message(self._on_message)
        return connection

    def _tls_context(
        self,
        cert: str,
        key: str,
        root_ca: str,
    ) -> io.ClientTlsContext:
        """Set up to authenticate with AWS IoT.

        Args:
            cert: Path to a certificate file
            key: Path to a .pem format key
            root_ca: Path to the AWS CARoot.pem file

        This logic is borrowed from the SDK tests:
        https://github.com/awslabs/aws-crt-python/blob/main/mqtt_test.py#L86

        # TODO Add websockets support, if we (or others) need it
        """
        try:
            tls_options = io.TlsContextOptions.create_client_with_mtls_from_path(cert, key)
        except FileNotFoundError as err:
            logging.error(err)
            exit(1) 

        if root_ca:
            try:
                tls_options.override_default_trust_store_from_path(ca_filepath=root_ca)
            except FileNotFoundError:
                logging.warning("No root CA found")
            except Exception as err:
                logging.error(err)

        tls_context = io.ClientTlsContext(tls_options)
        return tls_context


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
