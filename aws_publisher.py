import json
import logging

from awscrt.mqtt import QoS

from campbellcontrol.config import load_config
from campbellcontrol.connection.aws import AWSConnection

logging.basicConfig(level=logging.DEBUG)

config = load_config()
topic = config.topic

def main() -> None:
    print(f"Connecting to {config.server}")
    conn = AWSConnection(
        str(config.client_id),
        config.server,
        config.port,
        private_key=config.private_key,
        public_key=config.public_key,
        certificate_root=config.certificate_root,
    )
    topic = f"{config.topic}/cr/cr1000x/22505/fileControl"
    conn.connect()
    publish_future, publish_packet_id = conn.client.publish(
        topic,
        json.dumps({"action": "list"}),
        qos=QoS.AT_LEAST_ONCE,
    )
    publish_results = publish_future.result()
    assert(publish_results['packet_id'] == publish_packet_id)
    conn.disconnect()

if __name__ == '__main__':
    main()
