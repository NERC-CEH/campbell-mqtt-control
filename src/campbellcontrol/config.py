import logging
from dataclasses import dataclass
from typing import Optional

import yaml


@dataclass
class Config:
    """Configure a connection.

    mTLS (public/private key and root CA) left optional for port 1883;
    Could also add a check here if port is 8883
    """

    client_id: str
    topic: str
    broker: str
    server: str
    port: int
    certificate_root: Optional[str] = ""
    public_key: Optional[str] = ""
    private_key: Optional[str] = ""

    def connection_args(self) -> list:
        """Return the positional arguments a Connection wants
        Note that AWSConnection wants the client_id first, Paho doesn't
        """
        return [self.server, self.port]

    def connection_options(self) -> dict:
        """Return the option arguments a Connection wants"""
        return {
            "certificate_root": self.certificate_root,
            "public_key": self.public_key,
            "private_key": self.private_key,
        }


def load_config(config_file: Optional[str] = "config.yaml") -> dict:
    try:
        with open(config_file, "r") as conf_file:
            config = yaml.safe_load(conf_file.read())
    except (FileNotFoundError, TypeError):
        logging.warning(f"Configuration file not found at {config_file}")
        # TODO decide whether to exit or assume defaults, for now:
        raise
    return Config(**config)
