from campbellcontrol.connection.interface import Connection
from typing import TypedDict, Literal, Any
from abc import ABC, abstractmethod


class OSPayload(TypedDict):
    """Payload for the OS command."""
    url: str
    filename: str

class Command(ABC):
    
    command_name: str
    """Name of the Campbell command."""

    response_path: Literal["state","cr"]
    publish_path: Literal["cc"] = "cc"

    @classmethod
    def publish_topic(cls, group_id: str, serial: str) -> str:
        """Return the publish topic for the command."""
        return f"{group_id}/{cls.publish_path}/{serial}/{cls.command_name}"
    
    @classmethod
    def response_topic(cls, group_id: str, serial: str) -> str:
        """Return the response topic for the command."""
        return f"{group_id}/{cls.response_path}/{serial}/{cls.command_name}"
    
    @abstractmethod
    def payload(self, *args, **kwargs) -> Any:
        """Return the payload for the command."""
    
class OS(Command):
    """Command to download an operating system."""
    command_name = "OS"
    response_path = "state"

    @staticmethod
    def payload(url: str, filename: str) -> OSPayload:
        """Return the payload for the OS command."""
        return {
            "url": url,
            "filename": filename
        }

# class Controller:
#     """Controller class to manage connections and operations."""

#     def __init__(self, connection: Connection) -> None:
#         self.broker = connection
#         self.broker.connect()
    
#     def send_command(self, *args, **kwargs) -> None:
#         """Send a command to the broker."""
#         self.broker.publish(*args, **kwargs)