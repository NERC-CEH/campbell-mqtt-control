import json
from abc import ABC, abstractmethod
from typing import Any, Dict, Literal, Optional, TypedDict


class CommandResponse(TypedDict):
    """Response from the command handler."""

    payload: dict
    success: bool
    error: Optional[str]


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


class GetVarPayload(TypedDict):
    """Payload for a getting a variable"""

    name: str


class SetVarPayload(TypedDict):
    """Payload for setting a variable"""

    name: str
    value: str


class HistoricDataPayload(TypedDict):
    """Payload for getting historic data"""

    table: str
    start: str
    end: str


class TalkThruPayload(TypedDict):
    """Payload for talking to a sensor"""

    comPort: str

    outString: str
    numberTries: Optional[str]

    respDelay: Optional[str]
    abort: Optional[bool]


class Error(TypedDict):
    """Error response"""

    error: str


class Success(TypedDict):
    """Success Response"""

    success: str


class Command(ABC):
    command_name: str
    """Name of the Campbell command."""

    def __init__(self, group_id: str, serial: str) -> None:
        self.publish_topic = f"{group_id}/cc/{serial}/{self.command_name}"
        self.response_topic = f"{group_id}/cr/{serial}/{self.command_name}"
        self.state_topic = f"{group_id}/state/{serial}/"

    @abstractmethod
    def payload(*args, **kwargs) -> Any:
        """Return the payload for the command."""

    def json_payload(self, *args, **kwargs) -> str:
        """Jsonified payload string"""
        return json.dumps(self.payload(*args, **kwargs))

    def handler(self, topic: str, payload: str) -> Optional[CommandResponse]:
        """Handler for payloads that always have either a 'success' or 'error' value."""
        payload = json.loads(payload)

        if "error" in payload:
            return {
                "payload": payload,
                "success": False,
                "error": payload["error"],
            }
        elif "success" in payload:
            return {"payload": payload, "success": True}
        else:
            return None


class OS(Command):
    """Command to download an operating system."""

    command_name = "OS"

    @staticmethod
    def payload(url: str) -> URLPayload:
        """Return the payload for the OS command."""
        return {"url": url}


class Program(Command):
    """Command to download a CRBasic Program.
    The downloaded file is set to the current program and reboots the logger.
    """

    command_name = "program"

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def payload() -> ActionPayload:
        """Return the payload for the Reboot command."""
        return {"action": "reboot"}


class ListFiles(Command):
    """Command to list files on the logger."""

    command_name = "fileControl"

    def payload(self, drive: Optional[str] = None) -> FileListPayload:
        """Return the payload for the ListFiles command."""
        output = {"action": "list"}
        if drive:
            output.update({"drive": drive})
        return output

    def handler(self, topic: str, payload: str) -> Optional[CommandResponse]:
        """Handler for returning a list of files"""
        payload = json.loads(payload)

        if "fileList" in payload:
            return {
                "payload": payload,
                "success": True,
            }
        elif "error" in payload:
            return {
                "payload": payload,
                "success": False,
                "error": payload["error"],
            }


class DeleteFile(Command):
    """Command to delete a file on the logger."""

    command_name = "fileControl"

    def payload(self, filename: str, drive: Optional[str] = None) -> FileActionPayload:
        """Return the payload for the DeleteFile command."""
        output = {"action": "delete", "fileName": filename}
        if drive:
            output.update({"drive": drive})
        return output


class StopProgram(Command):
    command_name = "fileControl"

    @staticmethod
    def payload() -> ActionPayload:
        """Return the payload for the StopProgram command."""
        return {"action": "stop"}


class RunProgram(Command):
    command_name = "fileControl"

    @staticmethod
    def payload(filename: str) -> ActionPayload:
        """Return the payload for the StopProgram command."""
        return {"action": "run", "fileName": filename}


class SetSetting(Command):
    """Set a setting value"""

    command_name = "setting"

    def payload(self, name: str, value: str, apply: bool = False) -> SettingsSetPayload:
        """Return the payload for the SetSetting command."""
        output = {"action": "set", "name": name, "value": value}
        if apply:
            output.update({"apply": apply})
        return output


class ApplySettings(Command):
    """Apply settings"""

    command_name = "setting"

    def payload(self) -> SettingsApplyPayload:
        """Return the payload for the ApplySettings command."""
        return {"action": "apply", "apply": True}


class PublishSetting(Command):
    """Publish setting value"""

    command_name = "setting"

    def payload(self, name: str) -> SettingsPublishPayload:
        """Get a payload for publishing a setting"""
        return {"action": "publish", "name": name}


class SetVar(Command):
    """Set variables present in the logger script"""

    command_name = "SetVar"

    def payload(self, name: str, value: str) -> SetVarPayload:
        """Payload for setting a variable"""
        return {"name": name, "value": value}


class GetVar(Command):
    """Get variables present in the logger script"""

    command_name = "GetVar"

    def payload(self, name: str) -> GetVarPayload:
        """Payload for getting a variable"""
        return {"name": name}


class HistoricData(Command):
    """Retrieve historic data"""

    command_name = "historicData"

    def payload(self, table: str, start: str, end: str) -> HistoricDataPayload:
        """Payload for retrieving historic data"""

        return {"table": table, "start": start, "end": end}


class TalkThru(Command):
    """Talk through to sensor"""

    command_name = "talkThru"

    def payload(
        self,
        com_port: str,
        out_string: str,
        num_tries: Optional[str] = None,
        resp_delay: Optional[str] = None,
        abort: Optional[bool] = None,
    ) -> TalkThruPayload:
        output = {"comPort": com_port, "outString": out_string}

        if num_tries:
            output.update({"numberTries": num_tries})

        if resp_delay:
            output.update({"respDelay": resp_delay})

        if abort:
            output.update({"abort": abort})

        return output

    def handler(self, topic: str, payload: str) -> Optional[CommandResponse]:
        """Handler for returning a talkThru response"""

        payload = json.loads(payload)

        if "response" in payload:
            return {
                "payload": payload,
                "success": True,
            }
        else:
            raise RuntimeError("Unknown response from TalkThru")
