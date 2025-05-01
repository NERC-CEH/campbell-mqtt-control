from campbellcontrol.connection.generic import PahoConnection
import json

conn = PahoConnection("test.mosquitto.org", 1883)
conn.connect()

conn.publish(
    "cs/v2/cc/QU8Q-9JTY-HVP8/mqttConfig",
    json.dumps(
        {
            "url": "https://raw.githubusercontent.com/NERC-CEH/campbell-mqtt-control/refs/heads/feature/commands/mqtt.bin",
            "fileName": "testfile.bin",
        }
    ),
)
