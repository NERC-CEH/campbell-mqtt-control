import logging

from campbellcontrol.connection.generic import PahoConnection

logging.basicConfig(level=logging.DEBUG)
client_id = "QU8Q-9JTY-HVP8"
conn = PahoConnection("test.mosquitto.org", 1883)
conn.connect()
conn.subscribe(f"cs/v2/+/{client_id}")
conn.subscribe(f"cs/v2/+/{client_id}/#")
conn.subscribe("cs/v2/#")
# conn.subscribe("#")


conn.client.loop_forever()
