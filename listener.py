from campbellcontrol.connection.generic import PahoConnection

conn = PahoConnection("test.mosquitto.org", 1883)
conn.connect()
conn.subscribe("cs/v2/cc/QU8Q-9JTY-HVP8/")
conn.subscribe("cs/v2/state/QU8Q-9JTY-HVP8/")
conn.subscribe("cs/v2/state/QU8Q-9JTY-HVP8/#")
conn.subscribe("cs/v2/cc/QU8Q-9JTY-HVP8/#")
conn.subscribe("cs/v2/cr/QU8Q-9JTY-HVP8/#")


conn.client.loop_forever()
