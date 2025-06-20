import argparse
import logging

from campbellcontrol.connection.generic import PahoConnection
from campbellcontrol.config import load_config
logging.basicConfig(level=logging.DEBUG)

config = load_config()
topic = config.topic

def main(client_id: str, server: str, port: int) -> None:
    logging.info(f"Connecting to {server}")
    conn = PahoConnection(server, 1883)
    conn.connect()
    conn.subscribe(f"{topic}/+/{client_id}")
    conn.subscribe(f"{topic}/+/{client_id}/#")
    conn.subscribe(f"{topic}/#")

    conn.client.loop_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--client", default="QU8Q-9JTY-HVP8", help="Serial number of the datalogger", type=str)
    parser.add_argument(
        "-s", "--server", default="test.mosquitto.org", help="Address of the MQTT test server", type=str
    )
    parser.add_argument("-p", "--port", default=1883, help="MQTT port", type=int)

    args = parser.parse_args()
    main(args.client, args.server, args.port)
