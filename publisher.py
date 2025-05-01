from campbellcontrol.connection.generic import PahoConnection
import json

conn = PahoConnection("test.mosquitto.org", 1883)
conn.connect()

conn.publish(
    "cs/v2/cc/QU8Q-9JTY-HVP8/talkThru",
    json.dumps({"comPort": "ComG", "outString": "heyyo"}),
)
