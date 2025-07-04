import argparse
import logging

from campbellcontrol.connection.generic import PahoConnection
from campbellcontrol.config import load_config
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

class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    green = "\x1b[32;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(levelname)s - %(message)s"

    FORMATS = {
        logging.DEBUG: green + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno) # default
        if "error" in record.msg:
            log_fmt = self.FORMATS.get(logging.ERROR)
        if "success" in record.msg:
            log_fmt = self.FORMATS.get(logging.DEBUG)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def config_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    ch=logging.StreamHandler()
    ch.setFormatter(CustomFormatter())
    logger.addHandler(ch)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--client", default="QU8Q-9JTY-HVP8", help="Serial number of the datalogger", type=str)
    parser.add_argument(
        "-s", "--server", default="test.mosquitto.org", help="Address of the MQTT test server", type=str
    )
    parser.add_argument("-p", "--port", default=1883, help="MQTT port", type=int)

    args = parser.parse_args()
    config_logger()
    main(args.client, args.server, args.port)


