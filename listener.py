from campbellcontrol.connection.generic import PahoConnection

conn = PahoConnection("test.mosquitto.org", 1883)
conn.connect()
conn.subscribe("cs/v2/+/QU8Q-9JTY-HVP8")
conn.subscribe("cs/v2/+/QU8Q-9JTY-HVP8/#")
conn.subscribe("cs/v2/#")
# conn.subscribe("#")


conn.client.loop_forever()
