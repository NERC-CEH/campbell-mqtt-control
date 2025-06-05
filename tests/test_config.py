import pytest
from campbellcontrol.config import load_config, Config


def test_config(config_file):
    conf_data = load_config(config_file)
    assert "client_id" in conf_data

    with pytest.raises(FileNotFoundError):
        conf_null = load_config("definitely_not_a_file.md")
        assert "client_id" in conf_null
