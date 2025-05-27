import logging
from typing import Optional

import yaml


def load_config(config_file: Optional[str] = "config.yaml") -> dict:
    try:
        with open(config_file, "r") as conf_file:
            config = yaml.safe_load(conf_file.read())
    except (FileNotFoundError, TypeError):
        logging.warning(f"Configuration file not found at {config_file}")
        # TODO decide whether to exit or assume defaults, for now:
        raise
    return config
