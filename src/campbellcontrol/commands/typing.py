"""Module for storing payload types used in the Campbell MQTT API."""

from typing import Literal, Optional, TypedDict


class CommandResponse(TypedDict):
    """Response from the command handler."""

    payload: dict
    """The returned payload."""
    success: bool
    """Flag indicating success or failure."""
    error: Optional[str]
    """The error message. Absent if not error."""


class FileDownloadPayload(TypedDict):
    """Payload for a file download."""

    url: str
    """A valid URL to the download."""
    filename: str
    """The file to download it to on the system."""


class URLPayload(TypedDict):
    """Payload for specifying a URL."""

    url: str
    """A valid URL."""


class ActionPayload(TypedDict):
    """Payload for specifying an action."""

    action: str
    """Name of an action."""


class FileActionPayload(TypedDict):
    """Payload for acting on a file."""

    action: str
    """Name of an action."""
    fileName: str
    """Name of the file to act upon."""
    drive: Optional[str]
    """Optional key to the target drive."""


class FileListPayload(TypedDict):
    """Payload for listing files in a directory."""

    action: str
    """Name of the action taken."""
    drive: Optional[str]
    """Optional key to the target drive."""


class SettingsSetPayload(TypedDict):
    """Payload for changing settings."""

    action: Literal["set"]
    """The action to take (must be "set")."""
    name: str
    """Name of the setting to change."""
    value: str
    """New value for the setting."""
    apply: Optional[bool]
    """Optional flag for applying the change immediately."""


class SettingsPublishPayload(TypedDict):
    """Payload for publishing setting values."""

    action: Literal["publish"]
    """The action to take (must be "publish")."""
    name: str
    """Name of the setting to publish"""


class SettingsApplyPayload(TypedDict):
    """Payload for applying Settings."""

    action: Literal["apply"]
    """The action to take (must be "apply")."""
    apply: bool
    """Flag to apply settings."""


class GetVarPayload(TypedDict):
    """Payload for a getting a variable."""

    name: str
    """Name of the variable to publish."""


class SetVarPayload(TypedDict):
    """Payload for setting a variable."""

    name: str
    """Name of the variable to set."""
    value: str
    """New value of the variable."""


class HistoricDataPayload(TypedDict):
    """Payload for getting historic data."""

    table: str
    """The logger table to query."""
    start: str
    """Start date of the query."""
    end: str
    """End date of the query."""


class TalkThruPayload(TypedDict):
    """Payload for talking to a sensor."""

    comPort: str
    """The COM port to talk through."""
    outString: str
    """An ASCII string to send to the sensor."""
    numberTries: Optional[str]
    """ASCII number string indicating number of attempts."""
    respDelay: Optional[str]
    """ASCII number string (milliseconds) of time to wait for response."""
    abort: Optional[bool]
    """Flag to abort TalkThru session."""
