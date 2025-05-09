from campbellcontrol.connection.generic import PahoConnection
import campbellcontrol.commands as commands
import json

conn = PahoConnection("localhost", 1883)
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
        {"success": "File deleted"}
    ),
)
