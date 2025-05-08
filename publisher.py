from campbellcontrol.connection.generic import PahoConnection
import campbellcontrol.control as control
import json

conn = PahoConnection("localhost", 1883)
conn.connect()

command = control.Settings
base_topic = "cs/v2"
serial = "QU8Q-9JTY-HVP8"

conn.publish(
    "cs/v2/cc/QU8Q-9JTY-HVP8/mqttConfig",
    json.dumps(
        {
            "url": "https://github.com/NERC-CEH/campbell-mqtt-control/raw/refs/heads/feature/commands/logger",
            "fileName": "testfile.bin",
        }
    ),
)
