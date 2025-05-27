import pytest
from pathlib import Path


def pytest_addoption(parser):
    """Configurable default for device serial # when running hardware tests"""
    parser.addoption("--serial", action="store", default="QU8Q-9JTY-HVP8")
    parser.addoption("--server", action="store", default="test.mosquitto.org")


@pytest.fixture
def fixture_dir():
    return Path(__file__).parent.resolve() / "fixtures"


@pytest.fixture
def config_file(fixture_dir):
    return fixture_dir / "config.yaml"
