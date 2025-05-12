from abc import ABC, abstractmethod
from typing import Any


class Connection(ABC):
    """Base interface for defining MQTT broker connections."""

    endpoint: str
    """The endpoint of the MQTT broker."""
    port: int
    """The port of the MQTT broker."""
    client: Any
    """Handle to the MQTT client object."""

    def __init__(self, endpoint: str, port: int, *args, **kwargs):
        self.endpoint = endpoint
        self.port = port
        self.client = self.get_client(*args, **kwargs)

    @abstractmethod
    def get_client(self, *args, **kwargs) -> Any:
        """Return the client instance."""

    def connect(self) -> None:
        """Connect to the MQTT broker."""
        self.client.connect(self.endpoint, self.port)

    def disconnect(self) -> None:
        """Disconnect from the MQTT broker."""
        self.client.disconnect()

    def publish(self, topic: str, payload: str, *args, **kwargs) -> None:
        """Publish a message to a given topic.

        Args:
            topic: The topic to publish to.
            payload: The message payload.
            *args: Additional arguments forwarded to the client.
            **kwargs: Additional keyword arguments forwarded to the client.
        """
        self.client.publish(topic, payload, *args, **kwargs)

    def subscribe(self, topic: str) -> None:
        """Subscribe to a topic.

        Args:
            topic: The topic to subscribe to."""
        self.client.subscribe(topic)

    def unsubscribe(self, topic: str) -> None:
        """Unsubscribe from a topic.

        Args:
            topic: The topic to unsubscribe from.
        """
        self.client.unsubscribe(topic)
