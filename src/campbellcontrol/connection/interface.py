from abc import ABC, abstractmethod
from typing import Any


class Connection(ABC):
    """Base class for MQTT connections."""

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
        """Publish a message to a topic."""
        self.client.publish(topic, payload, *args, **kwargs)

    def subscribe(self, topic: str) -> None:
        """Subscribe to a topic."""
        self.client.subscribe(topic)

    def unsubscribe(self, topic: str) -> None:
        """Unsubscribe from a topic."""
        self.client.unsubscribe(topic)
