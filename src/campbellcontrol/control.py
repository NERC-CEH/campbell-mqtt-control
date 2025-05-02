import json
from abc import ABC, abstractmethod
from typing import Any, Dict, Literal, Optional, TypedDict


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


class FileActionPayload(TypedDict):
    """Payload for acting on files"""

    action: str
    fileName: str
    drive: Optional[str]


class FileListPayload(TypedDict):
    """Payload for listing files in a directory"""

    action: str
    drive: Optional[str]


class SettingsSetPayload(TypedDict):
    """Payload for changing settings"""

    action: Literal["set"]
    name: str
    value: str
    apply: Optional[bool]


class SettingsPublishPayload(TypedDict):
    """Payload for publishing setting values"""

    action: Literal["publish"]
    name: str


class SettingsApplyPayload(TypedDict):
    """Payload for applying Settings"""

    action: Literal["apply"]
    apply: bool


class Error(TypedDict):
    """Error response"""

    error: str


class Success(TypedDict):
    """Success Response"""

    success: str


class Command(ABC):
    command_name: str
    """Name of the Campbell command."""

    @classmethod
    def publish_topic(cls, group_id: str, serial: str) -> str:
        """Return the publish topic for the command."""
        return f"{group_id}/cc/{serial}/{cls.command_name}"

    @classmethod
    def response_topic(cls, group_id: str, serial: str) -> str:
        """Return the response topic for the command."""
        return f"{group_id}/cr/{serial}/{cls.command_name}"

    @staticmethod
    def state_topic(group_id: str, serial: str) -> str:
        """Return the state topic"""
        return f"{group_id}/state/{serial}/"

    @staticmethod
    @abstractmethod
    def payload(*args, **kwargs) -> Any:
        """Return the payload for the command."""

    @classmethod
    def json_payload(cls, *args, **kwargs) -> str:
        """Jsonified payload string"""
        return json.dumps(cls.payload(*args, **kwargs))


class OS(Command):
    """Command to download an operating system."""

    command_name = "OS"

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

    def payload() -> ActionPayload:
        """Return the payload for the Reboot command."""
        return {"action": "reboot"}


class File(Command):
    """Command to manipulate files"""

    command_name = "fileControl"

    @classmethod
    def payload(
        cls,
        action: Literal["list", "delete", "stop", "run"],
        filename: Optional[str] = None,
        drive: Optional[str] = None,
    ) -> FileListPayload | FileActionPayload | ActionPayload:
        """Get payload for file command"""

        if action in ["delete", "run"]:
            if not filename:
                raise RuntimeError(f"`filename` is a requirement argument for the `{action}` action")
            return cls._file_action(action, filename, drive)
        if action == "list":
            return cls._list_files(drive)
        elif action == "stop":
            return cls._stop_program()

    @staticmethod
    def _file_action(action: str, filename: str, drive: Optional[str] = None) -> FileActionPayload:
        output = {
            "action": action,
            "fileName": filename,
        }
        if drive:
            output.update({"drive": drive})

        return output

    @staticmethod
    def _list_files(drive: Optional[str]) -> FileListPayload:
        output = {"action": "list"}
        if drive:
            output.update({"drive": drive})
        return output

    @staticmethod
    def _stop_program() -> ActionPayload:
        """Stops the running program"""

        return {"action": "stop"}


class Settings(Command):
    """Control settings of a logger"""

    command_name = "setting"

    @classmethod
    def payload(
        cls,
        action: Literal["set", "publish", "apply"],
        name: Optional[str] = None,
        value: Optional[str] = None,
        apply: Optional[bool] = None,
    ) -> SettingsSetPayload | SettingsPublishPayload | SettingsApplyPayload:
        """Gets a payload for a setting command"""

        if action == "apply":
            return cls._apply()

        if not name:
            raise RuntimeError(f"`name` argument is required for the `{action}` action")

        if action == "publish":
            return cls._publish(name)

        if not value:
            raise RuntimeError(f"`value` argument is required for the `{action}` action")

        if action == "set":
            return cls._set(name, value, apply)

    @staticmethod
    def _set(name: str, value: str, apply: Optional[bool] = None) -> SettingsSetPayload:
        """Get a payload for changing a setting value"""

        output = {"action": "set", "name": name, "value": value}
        if apply:
            output.update({"apply": apply})
        return output

    @staticmethod
    def _publish(name: str) -> SettingsPublishPayload:
        """Get a payload for publishing a setting"""
        return {"action": "publish", "name": name}

    @staticmethod
    def _apply() -> SettingsApplyPayload:
        """Get a payload for applying setting changes"""
        return {"action": "apply", "apply": True}


# class Controller:
#     """Controller class to manage connections and operations."""

#     def __init__(self, connection: Connection) -> None:
#         self.broker = connection
#         self.broker.connect()

#     def send_command(self, *args, **kwargs) -> None:
#         """Send a command to the broker."""
#         self.broker.publish(*args, **kwargs)
