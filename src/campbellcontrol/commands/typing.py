"""Module for storing payload types used in the Campbell MQTT API."""

from typing import Literal, Optional, TypedDict


class CommandResponse(TypedDict):
    """Response from the command handler.
    Attributes:
        payload: The returned payload.
        success: Flag indicating success or failure.
        error: The error message. Absent if not error.
    """

    payload: dict
    success: bool
    error: Optional[str]


class FileDownloadPayload(TypedDict):
    """Payload for a file download.
    Attributes:
        url: A valid URL to the download.
        file: The file to download it to on the system.
    """

    url: str
    filename: str


class URLPayload(TypedDict):
    """Payload for specifying a URL.
    Attributes:
        url: A valid URL
    """

    url: str


class ActionPayload(TypedDict):
    """Payload for specifying an action.
    Attributes:
        action: Name of the action.
    """

    action: str


class FileActionPayload(TypedDict):
    """Payload for acting on a file.
    Attributes:
        action: Name of the action taken.
        fileName: Name of the file to act upon.
        drive: Optional key to the target drive.
    """

    action: str
    fileName: str
    drive: Optional[str]


class FileListPayload(TypedDict):
    """Payload for listing files in a directory.
    Attributes:
        action: Name of the action taken.
        drive: Optional key to the target drive.
    """

    action: str
    drive: Optional[str]


class SettingsSetPayload(TypedDict):
    """Payload for changing settings.
    Attributes:
        action: The action to take (must be "set").
        name: Name of the setting to change.
        value: New value for the setting.
        apply: Optional flag for applying the change immediately.
    """

    action: Literal["set"]
    name: str
    value: str
    apply: Optional[bool]


class SettingsPublishPayload(TypedDict):
    """Payload for publishing setting values.
    Attributes:
        action: The action to take (must be "publish").
        name: Name of the setting to publish
    """

    action: Literal["publish"]
    name: str


class SettingsApplyPayload(TypedDict):
    """Payload for applying Settings.
    Attributes:
        action: The action to take (must be "apply").
        apply: Flag to apply settings.
    """

    action: Literal["apply"]
    apply: bool


class GetVarPayload(TypedDict):
    """Payload for a getting a variable.
    Attributes:
        name: Name of the variable to publish.
    """

    name: str


class SetVarPayload(TypedDict):
    """Payload for setting a variable.
    Attributes:
        name: Name of the variable to set.
        value: New value of the variable.
    """

    name: str
    value: str


class HistoricDataPayload(TypedDict):
    """Payload for getting historic data.
    Attributes:
        table: the logger table to query.
        start: Start date of the query.
        end: End date of the query.
    """

    table: str
    start: str
    end: str


class TalkThruPayload(TypedDict):
    """Payload for talking to a sensor
    Attributes:
        comPort: The COM port to talk through.
        outString: An ASCII string to send to the sensor.
        numberTries: ASCII number string indicating number of attempts.
        respDelay: ASCII number string (milliseconds) of time to wait for response.
        abort: Flag to abort TalkThru session.
    """

    comPort: str

    outString: str
    numberTries: Optional[str]

    respDelay: Optional[str]
    abort: Optional[bool]
