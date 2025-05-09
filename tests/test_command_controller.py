from unittest import TestCase, main
from campbellcontrol.control import PahoCommandHandler
from campbellcontrol.connection.generic import PahoConnection
import campbellcontrol.commands as commands
import logging

logging.basicConfig(level=logging.DEBUG)

client = PahoConnection("localhost", 1883)
command_handler = PahoCommandHandler(client)


def test_command_controller():
    base_topic = "cs/v2"
    serial = "QU8Q-9JTY-HVP8"

    command_handler.send_command(commands.DeleteFile(base_topic, serial), "testfile")


test_command_controller()
