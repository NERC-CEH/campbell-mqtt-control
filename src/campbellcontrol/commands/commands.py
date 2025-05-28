"""Module for defining MQTT commands, bulding payloads to send commands,
and defining callbacks for handling responses from the logger.
"""

import json
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from campbellcontrol.commands.typing import (
    ActionPayload,
    CommandResponse,
    FileActionPayload,
    FileDownloadPayload,
    FileListPayload,
    GetVarPayload,
    HistoricDataPayload,
    SettingsApplyPayload,
    SettingsPublishPayload,
    SettingsSetPayload,
    SetVarPayload,
    TalkThruPayload,
    URLPayload,
)


class Command(ABC):
    """Base class for defining a Campbell logger MQTT command.
    This class helps to define relevant topics used to interface
    with the command, generation of a payload that must be sent with
    the command, and provides a method to handle the reponse.
    """

    command_name: str
    """Name of the Campbell command used to build topics."""

    publish_topic: str
    """The topic used to send the command to a logger."""

    response_topic: str
    """The topic that response data is typically sent through"""

    state_topic: str
    """The topic that supplimental data regarding the state is sent through,
        useful for logging the changes occuring on the logger rather than only
        the final response
    """

    def __init__(
        self,
        group_id: str,
        serial: str,
        model: Optional[str] = "cr1000x",
        options: Optional[dict] = {},
    ) -> None:
        """Initializes the class. The topics should match that used by the target logger

        Args:
            group_id: The base topic used by the logger.
            serial: The serial number of the target logger
            model: optional, default 'cr1000x' - the model number of the logger
        """
        self.device_id = f"{model}/{serial}"
        self.publish_topic = f"{group_id}/cc/{self.device_id}/{self.command_name}"
        self.response_topic = f"{group_id}/cr/{self.device_id}/{self.command_name}"
        self.state_topic = f"{group_id}/state/{self.device_id}/"

        if options and "response_suffix" in options:
            suffix = options["response_suffix"]
            self.response_topic = f"{self.response_topic}/{suffix}"

        self.state_topic = f"{group_id}/state/{self.device_id}/"

    @abstractmethod
    def payload(*args, **kwargs) -> Any:
        """Return the payload used to send the command."""

    def failed_state(self, *args, **kwargs) -> Any:
        """Return a payload only if it matches specific failure messages.
        Used for handling responses that are made on the state topic"""
        pass

    def json_payload(self, *args, **kwargs) -> str:
        """Jsonified payload string.

        Returns:
            A JSON formatted string payload.
        """
        return json.dumps(self.payload(*args, **kwargs))

    def handler(self, topic: str, message: str) -> Optional[CommandResponse]:
        """Handler for messages that have either a 'success' or 'error' value.

        Args:
            topic: The topic that the message is received from.
            message: The received message.
        """
        message = json.loads(message)

        if "error" in message:
            return {
                "payload": message,
                "success": False,
                "error": message["error"],
            }
        elif "success" in message:
            return {"payload": message, "success": True}
        # Special case where failure payloads are on the state topic
        elif self.failed_state(message):
            return {"payload": message, "success": False}
        else:
            return None


class OS(Command):
    """Command to download and install an operating system."""

    command_name = "OS"

    @staticmethod
    def payload(url: str) -> URLPayload:
        """Return the payload for the OS command.

        Returns:
            A payload dictionary"""
        return {"url": url}


class Program(Command):
    """Command to download a CRBasic Program.
    The downloaded file is set to the current program and reboots the logger.

    If the download fails, the response is sent on `state`, we see two messages:

        {"clientId":"ABC",
         "state":"online",
         "fileTransfer":"CRBasic file transfer started"}

        {"clientId":"ABC",
         "state":"online",
         "fileTransfer":"CRBasic file transfer error"}

    """

    command_name = "program"

    @staticmethod
    def payload(url: str, filename: str) -> FileDownloadPayload:
        """Return the payload for the Program command.

        Args:
            url: Url to a Campbell program.
            filename: Name to assign to the download on the logger.
        Returns:
            A dictionary payload
        """
        return {"url": url, "fileName": filename}

    def failed_state(self, message: dict) -> dict:
        """Accepts the message on a state topic.
        If it matches very specific events, return it as a response
        (Used for handling failures, like file download"""

        # TODO if there are many of these cases, define the strings separately
        if message.get("fileTransfer", None) == "CRBasic file transfer error":
            message["error"] = "Program download failed"
            return message
        return None


class MQTTConfig(Command):
    """Command to reconfigure MQTT settings.
    If the file is valid, the settings are applied and the logger reboots.
    """

    command_name = "mqttConfig"

    @staticmethod
    def payload(url: str) -> URLPayload:
        """Return the payload for the MQTTConfig command.

        Args:
            url: Url to a Campbell proprietary binary formatted settings file.
        Returns:
            A dictionary payload
        """
        return {"url": url}


class EditConstants(Command):
    """Command to edit constants in a CRBasic program.
    Values are converted to correct types by the logger.
    """

    command_name = "editConst"

    @staticmethod
    def payload(*args, **kwargs) -> Dict[str, str]:
        """Return the payload for the EditConstants command.

        Args:
            *args: Any quantity of dictionaries.
            **kwargs: Keyword arguments specifying constants and the new value.
        Returns:
            A dictionary of key value {"constant_name": "value"} pairs.
        """
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
        """Return the payload for the Reboot command.

        Returns:
            A dictionary payload.
        """

        return {"action": "reboot"}


class ListFiles(Command):
    """Command to list files in a drive."""

    command_name = "fileControl"

    def payload(self, drive: Optional[str] = None) -> FileListPayload:
        """Build a payload for the file list command.

        Args:
            drive: An optional string specifying the drive to list.
        Returns:
            A dictionary payload.
        """
        output = {"action": "list"}
        if drive:
            output.update({"drive": drive})
        return output

    @staticmethod
    def handler(topic: str, message: str) -> Optional[CommandResponse]:
        """Handler for returning a list of files.

        Args:
            topic: The topic the message was received on.
            message: The message contents in string format.
        Returns:
            A command reponse.
        """
        message = json.loads(message)
        if "fileList" in message:
            return {
                "payload": message,
                "success": True,
            }
        elif "error" in message:
            return {
                "payload": message,
                "success": False,
                "error": message["error"],
            }


class DeleteFile(Command):
    """Command to delete a file on the logger."""

    command_name = "fileControl"

    def payload(self, filename: str, drive: Optional[str] = None) -> FileActionPayload:
        """Build a payload for the file deletion command.

        Args:
            filename: The file to delete.
            drive: An optional string specifying the drive to target.
        Returns:
            A dictionary payload.
        """
        output = {"action": "delete", "fileName": filename}
        if drive:
            output.update({"drive": drive})
        return output


class StopProgram(Command):
    """Command that stops the currently running logger program."""

    command_name = "fileControl"

    @staticmethod
    def payload() -> ActionPayload:
        """Build a payload for the StopProgram command.

        Returns:
            A dictionary payload.
        """
        return {"action": "stop"}


class RunProgram(Command):
    """Command to a run a logger program from a file located on the device."""

    command_name = "fileControl"

    @staticmethod
    def payload(filename: str) -> ActionPayload:
        """Build a payload for the StopProgram command.

        Args:
            filename: Name of the file to run.
        Returns:
            A dictionary payload.
        """
        return {"action": "run", "fileName": filename}


class SetSetting(Command):
    """Set a setting in the logger"""

    command_name = "setting"

    def payload(self, name: str, value: str, apply: bool = False) -> SettingsSetPayload:
        """Build a payload for the SetSetting command.

        Args:
            name: Name of the setting.
            value: New value to set.
            apply: Applies the change immediately (may cause a logger reboot).
        Returns:
            A dictionary payload.
        """
        output = {"action": "set", "name": name, "value": value}
        if apply:
            output.update({"apply": apply})
        return output


class ApplySettings(Command):
    """Apply changed logger settings"""

    command_name = "setting"

    def payload(self) -> SettingsApplyPayload:
        """Build a payload for the ApplySettings command.

        Returns:
            A dictionary payload
        """
        return {"action": "apply", "apply": True}


class PublishSetting(Command):
    """Publish the value of a setting."""

    command_name = "setting"

    def payload(self, name: str) -> SettingsPublishPayload:
        """Build a payload for publishing a setting.

        Args:
            name: Name of the setting to publish.
        Returns:
            A dictionary payload.
        """
        return {"action": "publish", "name": name}


class SetVar(Command):
    """Set variables present in the logger script."""

    command_name = "SetVar"

    def payload(self, name: str, value: str) -> SetVarPayload:
        """Build a ayload for setting a variable.

        Args:
            name: Name of the setting to change.
            value: New value for the setting.
        Returns:
            A dictionary payload.
        """
        return {"name": name, "value": value}


class GetVar(Command):
    """Publish variables present in the logger script."""

    command_name = "GetVar"

    def payload(self, name: str) -> GetVarPayload:
        """Build a payload for publishing a variable.

        Args:
            name: Name of the variable to publish.
        Returns:
            A dictionary payload.
        """
        return {"name": name}


class HistoricData(Command):
    """Retrieve historic data from a logger table"""

    command_name = "historicData"

    def payload(self, table: str, start: str, end: str) -> HistoricDataPayload:
        """Payload for retrieving historic data from the logger.

        Args:
            table: Name of the table on the logger.
            start: Start datetime to query.
            end: End datetime to query.
        Returns:
            A dictionary payload"""

        return {"table": table, "start": start, "end": end}


class TalkThru(Command):
    """Command to send a TalkThru command and manage the TalkThru session."""

    command_name = "talkThru"

    def payload(
        self,
        com_port: str,
        out_string: str,
        num_tries: Optional[str] = None,
        resp_delay: Optional[str] = None,
        abort: Optional[bool] = None,
    ) -> TalkThruPayload:
        """Build a payload for talking to a sensor.
            This keeps a session open during which time the port doesn't
            send any data and awaits further TalkThru commands. The session
            times out after 1 minute.

        Args:
            comPort: The COM port to talk through.
            outString: String to send to the sensor.
            numberTries: Number of attempts before failure.
            respDelay: Time (milliseconds) to wait for response.
            abort: Flag to end the  TalkThru session.
        Returns:
            A dictionary payload.
        """
        output = {"comPort": com_port, "outString": out_string}

        if num_tries:
            output.update({"numberTries": num_tries})

        if resp_delay:
            output.update({"respDelay": resp_delay})

        if abort:
            output.update({"abort": abort})

        return output

    @staticmethod
    def handler(topic: str, message: str) -> Optional[CommandResponse]:
        """Handler for returning a talkThru response

        Args:
            topic: The message receive topic.
            message: Value of the message.
        Returns:
            A command response or None.
        """

        message = json.loads(message)

        if "response" in message:
            return {
                "payload": message,
                "success": True,
            }
        else:
            raise RuntimeError("Unknown response from TalkThru")
