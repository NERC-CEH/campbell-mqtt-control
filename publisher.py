from campbellcontrol.connection.generic import PahoConnection
from campbellcontrol.connection.aws import AWSConnection
import campbellcontrol.commands as commands
import json
from awscrt.mqtt import QoS

conn = AWSConnection("client_id", "test.mosquitto.org", 1883)
conn.connect()

base_topic = "cs/v2"
serial = "QU8Q-9JTY-HVP8"

# conn.publish(
#     f"{base_topic}/cr/{serial}/fileControl",
#     json.dumps(
#         {"error":"Directory \'USR:\' does not exist"}
#     ),
# )

conn.publish(
    f"{base_topic}/cr/{serial}/fileControl",
    json.dumps(
        {"fileList": "Files listed"}
    ),
    qos=QoS.AT_LEAST_ONCE,
)
conn.disconnect()
