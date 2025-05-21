def pytest_addoption(parser):
    """Configurable default for device serial # when running hardware tests"""
    parser.addoption("--serial", action="store", default="QU8Q-9JTY-HVP8")
    parser.addoption("--server", action="store", default="test.mosquitto.org")
