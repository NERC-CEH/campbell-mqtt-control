from campbellcontrol.connection.generic import PahoConnection
from campbellcontrol.connection.aws import AWSConnection
import campbellcontrol.commands as commands
import json
from awscrt.mqtt import QoS

import argparse
import logging
import threading

from awscrt import mqtt

from campbellcontrol.config import load_config
from campbellcontrol.connection.aws import AWSConnection

logging.basicConfig(level=logging.DEBUG)

config = load_config()
topic = config.topic

def on_publish(*args, **kwargs):
    print(args)


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
    print(f"{config.topic}/hello/from/mqtt-control")
    import ipdb
    ipdb.set_trace()

    publish_future, publish_packet_id = conn.publish(
        f"{config.topic}/hello/from/mqtt-control",
        "test",
        qos=QoS.AT_LEAST_ONCE,
    )
    publish_results = publish_future.result(5)
    assert(publish_results['packet_id'] == publish_packet_id)
    conn.disconnect()

if __name__ == '__main__':
    main()
