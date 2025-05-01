from abc import ABC, abstractmethod
from typing import Any, Dict, Literal, TypedDict


class FileDownloadPayload(TypedDict):
    """Payload for the OS command."""

    url: str
    filename: str


class URLPayload(TypedDict):
    """Payload for specifying a URL."""
    url: str

class ActionPayload(TypedDict):
    """Payload for specifying an action."""
    action: str


class Command(ABC):
    command_name: str
    """Name of the Campbell command."""

    response_path: Literal["state", "cr"]
    publish_path: Literal["cc"] = "cc"

    @classmethod
    def publish_topic(cls, group_id: str, serial: str) -> str:
        """Return the publish topic for the command."""
        return f"{group_id}/{cls.publish_path}/{serial}/{cls.command_name}"

    @classmethod
    def response_topic(cls, group_id: str, serial: str) -> str:
        """Return the response topic for the command."""
        return f"{group_id}/{cls.response_path}/{serial}/{cls.command_name}"

    @staticmethod
    @abstractmethod
    def payload(*args, **kwargs) -> Any:
        """Return the payload for the command."""


class OS(Command):
    """Command to download an operating system."""

    command_name = "OS"
    response_path = "state"

    def payload(url: str) -> URLPayload:
        """Return the payload for the OS command."""
        return {"url": url}


class Program(Command):
    """Command to download a CRBasic Program.
    The downloaded file is set to the current program and reboots the logger.
    """

    command_name = "program"

    def payload(url: str, filename: str) -> FileDownloadPayload:
        """Return the payload for the Program command.
        Args:
            url: Url to a Campbell program.
            filename: Name to assign to the download on the logger.
        Returns:
            A payload
        """
        return {"url": url, "fileName": filename}


class MQTTConfig(Command):
    """Command to reconfigure MQTT settings.
    If the file is valid, the settings are applied and the logger reboots."""

    command_name = "mqttConfig"
    response_path = "state"

    def payload(url: str) -> URLPayload:
        """Return the payload for the MQTTConfig command.
        Args:
            url: Url to a Campbell proprietary binary formatted settings file.
        Returns:
            A payload
        """
        return {"url": url}


class EditConstants(Command):
    """Command to edit constants in a CRBasic program.
        Values are converted to correct types by the logger.
    """

    command_name = "editConst"
    response_path = "state"

    def payload(*args, **kwargs) -> Dict[str, str]:
        """Return the payload for the EditConstants command."""
        output = dict()
        for arg in args:
            if not isinstance(arg, dict):
                raise TypeError("args must be a dictionary")
            output.update(arg)

        output.update(kwargs)
        return output

class Reboot(Command):
    """Command to reboot the logger."""

    command_name = "reboot"
    response_path = "state"

    def payload() -> ActionPayload:
        """Return the payload for the Reboot command."""
        return {"action": "reboot"}

# class Controller:
#     """Controller class to manage connections and operations."""

#     def __init__(self, connection: Connection) -> None:
#         self.broker = connection
#         self.broker.connect()

#     def send_command(self, *args, **kwargs) -> None:
#         """Send a command to the broker."""
#         self.broker.publish(*args, **kwargs)
