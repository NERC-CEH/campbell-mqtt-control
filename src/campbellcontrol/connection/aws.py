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
    def __init__(self, client_id: str, *args, **kwargs) -> None:
        self.client_id = client_id
        super().__init__(*args, **kwargs)

    def get_client(self, *args, **kwargs) -> awscrt.mqtt.Connection:
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
        future = self.client.connect()
        future.result()

    def disconnect(self) -> None:
        future = self.client.disconnect()
        future.result()

    def subscribe(self, topic: str, qos: QoS = QoS.EXACTLY_ONCE, callback: Callable | None = None) -> None:
        future, _ = self.client.subscribe(topic=topic, qos=qos, callback=callback)

        result = future.result()
        exception = future.exception()

        if exception:
            logger.error("Subscription failed. error: {}".format(exception))
            return
        logger.info("Subscription successful. result: {}".format(result))

    def publish(self, topic: str, payload: str | bytes | bytearray, qos: QoS, retain: bool = False) -> None:
        future, _ = self.client.publish(topic=topic, payload=payload, qos=qos, retain=retain)
        future.result()

    def _on_connection_interrupted(self, connection: awscrt.mqtt.Connection, error: AwsCrtError, **kwargs) -> None:
        logger.error("Connection interrupted. error: {}".format(error))

    def _on_connection_resumed(
        self, connection: awscrt.mqtt.Connection, return_code: ConnectReturnCode, session_present: bool, **kwargs
    ) -> None:
        logger.info("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))

    def _on_connection_success(
        self, connection: awscrt.mqtt.Connection, callback_data: OnConnectionSuccessData
    ) -> None:
        logger.info("Connection successful. callback_data: {}".format(callback_data))

    def _on_connection_failure(
        self, connection: awscrt.mqtt.Connection, callback_data: OnConnectionFailureData
    ) -> None:
        logger.error("Connection failed. callback_data: {}".format(callback_data))

    def _on_connection_closed(self, connection: awscrt.mqtt.Connection, callback_data: OnConnectionClosedData) -> None:
        logger.info("Connection closed. callback_data: {}".format(callback_data))

    @staticmethod
    def _on_message(topic: str, payload: bytes, dup: bool, qos: QoS, retain: bool, **kwargs) -> None:
        logger.info(f"Received message from topic: {topic} with payload: {payload.decode()}")
