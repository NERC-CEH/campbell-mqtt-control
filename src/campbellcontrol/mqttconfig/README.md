# Campbell MQTT Config File Generator

Campbell loggers can read in MQTT settings from a binary formatted file with a very specific format

## How To Format
The formatting consists of 3 chunks
* A header byte indicating the file start. Must be 2 bytes (big-endian Most significant byte first (MSB)) equal to `0x0020`
* A sequence of setting entries, repeating as necessary, consisting of:
    * 2 byte setting ID from `0x0001` to `0x0011` (big-endian MSB first)
    * 4 byte length of the setting value (MSB first)
    * ASCII value of the setting. Must be equal to the setting length. For example changing the MQTT broker endpoint to "test.mosquitto.org" is a length of 18.
* A null byte indicating the file end. Must be null byte `0x0000`

## How it works
When the settings are loaded from a file, the logger recognizes that it's a MQTT settings file from the header byte. It then loops through the settings entries and applies them until it reaches a null byte at which point it exits.

## Known Settings
|Setting | Identifier |
|-|-|
|Account ID | 1 (0x0001) |
| Private key | 2 (0x0002) |
| Public certificate | 3 (0x0003) |
| Root certificate authority | 4 (0x0004) |
| Endpoint | 5 (0x0005) |
| Port number | 6 (0x0006) |
| Username | 7 (0x0007) |
| Password | 8 (0x0008) |
| Keep alive time | 9 (0x0009) |
| Client ID | 10 (0x000A) |
| Last will topic | 11 (0x000B) |
| Last will message | 12 (0x000C) |
| Last will QoS | 13 (0x000D) |
| Last will message retained by broker | 14 (0x000E) |
| Enable TLS in data logger | 15 (0x000F) |
| Base MQTT topic | 16 (0x0010) |
| State publish interval | 18 (0x0012) |
| Status info publish interval | 19 (0x0013) |
| MQTT connect with clean session | 20 (0x0014) |

## Using the Builder

The [builder.py](builder.py) script contains a simple implementation of building a binary file which changes the MQTT endpoint to "test.mosquitto.org"

## Future Development
This module can be developed out to build MQTT settings files from a fixed list of valid settings, but this is just for documenting right now