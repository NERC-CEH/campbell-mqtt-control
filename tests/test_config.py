import pytest
from campbellcontrol.config import load_config, Config


def test_config(config_file):
    config = load_config(config_file)
    assert config.client_id

    with pytest.raises(FileNotFoundError):
        _ = load_config("definitely_not_a_file.md")

    port = config.port
    assert type(port) == int
