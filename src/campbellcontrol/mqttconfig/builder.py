"""This is a temporary module showing an example invocation of how to create a MQTT settings file."""

from struct import pack


def example_file_build(path: str) -> None:
    """Builds a settings file that will update the MQTT endpoint to "test.mosquitto.org"."""
    with open(path, "wb") as f:
        # Write the header
        f.write(pack(">H", 0x0020))
        f.write(pack(">HH", 0x0005, 18) + b"test.mosquitto.org")
        f.write(b"\x00")
