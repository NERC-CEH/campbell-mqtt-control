import logging
from typing import Optional, TypedDict

import yaml


class Config(TypedDict):
    serial: int
    topic: str
    broker: str
    certificate_pem: str
    public_key: str
    private_key: str
    server: str
    port: int


def load_config(config_file: Optional[str] = "config.yaml") -> dict:
    try:
        with open(config_file, "r") as conf_file:
            config = yaml.safe_load(conf_file.read())
    except (FileNotFoundError, TypeError):
        logging.warning(f"Configuration file not found at {config_file}")
        # TODO decide whether to exit or assume defaults, for now:
        raise
    return Config(config)
