from unittest import TestCase, main
from campbellcontrol.control import PahoCommandHandler, AWSCommandHandler
from campbellcontrol.connection.generic import PahoConnection
from campbellcontrol.connection.aws import AWSConnection
import campbellcontrol.commands as commands
import logging
import pytest

logging.basicConfig(level=logging.DEBUG)


@pytest.mark.hardware
class TestPahoCommandHandler(TestCase):
    def setUp(self):
        self.base_topic = "cs/v2"
        self.serial = "QU8Q-9JTY-HVP8"
        self.client = PahoConnection("test.mosquitto.org", 1883)
        self.command_handler = PahoCommandHandler(self.client)

    def test_list_files(self):
        command = commands.ListFiles(self.base_topic, self.serial)
        response = self.command_handler.send_command(command)

        self.assertEqual(response["success"], True)
        self.assertIn("fileList", response["payload"])
        self.assertIsInstance(response["payload"]["fileList"], list)
        self.assertEqual(response["payload"]["drive"], "CPU:")

    def test_list_files_with_bad_drive(self):
        command = commands.ListFiles(self.base_topic, self.serial)
        response = self.command_handler.send_command(command, drive="noway")

        expected_payload = {
            "success": False,
            "error": "Directory 'noway:' does not exist",
            "payload": {"error": "Directory 'noway:' does not exist"},
        }
        self.assertDictEqual(response, expected_payload)

    def test_os_download_invalid_url(self):
        command = commands.OS(self.base_topic, self.serial)
        url = "bad_url"
        response = self.command_handler.send_command(command, url)

        expected = {
            "success": False,
            "error": "OS Download Failed",
            "payload": {"error": "OS Download Failed"},
        }

        self.assertDictEqual(response, expected)

    def test_os_download_invalid_file(self):
        command = commands.OS(self.base_topic, self.serial)
        url = "https://google.com"
        response = self.command_handler.send_command(command, url)

        expected = {
            "success": False,
            "error": "OS File Check Failed",
            "payload": {"error": "OS File Check Failed"},
        }

        self.assertDictEqual(response, expected)

    def test_program_download_invalid_url(self):
        command = commands.Program(self.base_topic, self.serial)
        url = "bad_url"
        response = self.command_handler.send_command(command, url, "file")

        expected = {
            "success": False,
            "error": "Program download failed",
            "payload": {"error": "Program download failed"},
        }

        self.assertDictEqual(response, expected)

    def test_program_download_file_received(self):
        command = commands.Program(self.base_topic, self.serial)
        url = "https://google.com"
        response = self.command_handler.send_command(command, url, "file")

        expected = {
            "success": True,
            "payload": {"success": "Program loaded successfully"},
        }

        self.assertDictEqual(response, expected)

    def test_mqttconfig_download_invalid_url(self):
        command = commands.MQTTConfig(self.base_topic, self.serial)
        url = "bad_url"
        response = self.command_handler.send_command(command, url)

        expected = {
            "success": False,
            "error": "MQTT Config file download failed, code: 0",
            "payload": {"error": "MQTT Config file download failed, code: 0"},
        }

        self.assertDictEqual(response, expected)

    def test_mqttconfig_download_file_received(self):
        command = commands.MQTTConfig(self.base_topic, self.serial)
        url = "https://google.com"
        response = self.command_handler.send_command(command, url)

        error = "MQTT Config file parse failed"
        expected = {
            "success": False,
            "error": error,
            "payload": {"error": error},
        }

        self.assertDictEqual(response, expected)

    def test_reboot(self):
        command = commands.Reboot(self.base_topic, self.serial)
        response = self.command_handler.send_command(command)

        expected = {
            "success": True,
            "payload": {"success": "Reboot complete"},
        }

        self.assertDictEqual(response, expected)

    def test_set_constant(self):
        # script_url = "https://raw.githubusercontent.com/NERC-CEH/campbell-mqtt-control/refs/heads/feature/hardware-tests/tests/data/logger-script-constants-table.CR1X"
        # self.command_handler.send_command(commands.Program(self.base_topic, self.serial), script_url, "script-constants")
        # self.command_handler.send_command(commands.RunProgram(self.base_topic, self.serial), "script-constants")
        command = commands.EditConstants(self.base_topic, self.serial)
        response = self.command_handler.send_command(command, B=1)

        expected = {
            "success": True,
            "payload": {"success": "Constant set"},
        }

        self.assertDictEqual(response, expected)

    def test_stop_script(self):
        command = commands.StopProgram(self.base_topic, self.serial)
        response = self.command_handler.send_command(command)

        expected = {
            "success": True,
            "payload": {"success": "Script stopped"},
        }

        self.assertDictEqual(response, expected)


class TestAWSCommandHandler(TestPahoCommandHandler):
    def setUp(self):
        self.base_topic = "cs/v2"
        self.serial = "QU8Q-9JTY-HVP8"
        self.client = AWSConnection("testclient", "test.mosquitto.org", 1883)
        self.command_handler = AWSCommandHandler(self.client)
