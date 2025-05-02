from campbellcontrol.connection.generic import PahoConnection
import campbellcontrol.control as control
import json

conn = PahoConnection("test.mosquitto.org", 1883)
conn.connect()

command = control.Settings
base_topic = "cs/v2"
serial = "QU8Q-9JTY-HVP8"

conn.publish(
    topic=command.publish_topic(base_topic, serial),
    payload=command.json_payload(
        action="set", name="PakBusAddress", value="2", apply=False
    ),
)
