import argparse
import logging
import threading

from awscrt import mqtt

from campbellcontrol.config import load_config
from campbellcontrol.connection.aws import AWSConnection

logging.basicConfig(level=logging.DEBUG)

config = load_config()
topic = config.topic

receive_event = threading.Event()


def on_receive_message(topic: str, payload: dict, dup: int, qos: mqtt.QoS, retain: int, **kwargs) -> None:
    print(payload)


def main(client_id: str, server: str, port: int) -> None:
    print(f"Connecting to {config.server}")
    conn = AWSConnection(
        str(config.client_id),
        config.server,
        config.port,
        private_key=config.private_key,
        public_key=config.public_key,
        certificate_root=config.certificate_root,
    )

    conn.connect()
    print("subscribe")
    conn.subscribe(f"{topic}/+/{client_id}", qos=mqtt.QoS.AT_LEAST_ONCE)  # ,callback=on_receive_message)
    conn.subscribe(f"{topic}/+/{client_id}/#", qos=mqtt.QoS.AT_LEAST_ONCE)
    conn.subscribe(f"{topic}/#", qos=mqtt.QoS.AT_LEAST_ONCE, callback=on_receive_message)

    receive_event.wait()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--client", default="22505", help="Serial number of the datalogger", type=str)
    parser.add_argument(
        "-s", "--server", default="test.mosquitto.org", help="Address of the MQTT test server", type=str
    )
    parser.add_argument("-p", "--port", default=1883, help="MQTT port", type=int)

    args = parser.parse_args()
    main(args.client, args.server, args.port)
