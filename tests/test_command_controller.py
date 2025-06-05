from unittest import TestCase, main
from campbellcontrol.control import PahoCommandHandler, AWSCommandHandler
from campbellcontrol.connection.generic import PahoConnection
from campbellcontrol.connection.aws import AWSConnection
import campbellcontrol.commands.commands as commands
import time
import logging
import pytest

logging.basicConfig(level=logging.DEBUG)


@pytest.fixture(scope="class")
def client_id(pytestconfig, request):
    request.cls.client_id = pytestconfig.getoption("client_id")


@pytest.fixture(scope="class")
def mqtt_server(pytestconfig, request):
    request.cls.server = pytestconfig.getoption("server")


@pytest.fixture(scope="class")
def topic(pytestconfig, request):
    request.cls.topic = pytestconfig.getoption("topic")


@pytest.mark.usefixtures("client_id", "mqtt_server", "topic")
@pytest.mark.hardware
class TestPahoCommandHandler(TestCase):
    def setUp(self):
        self.base_topic = self.topic if self.topic is not None else "cs/v2"
        self.client = PahoConnection(self.server, 1883)
        self.command_handler = PahoCommandHandler(self.client)

    def test_list_files(self):
        command = commands.ListFiles(self.base_topic, self.client_id, options={"response_suffix": "list"})
        response = self.command_handler.send_command(command)

        self.assertEqual(response["success"], True)
        self.assertIn("fileList", response["payload"])
        self.assertIsInstance(response["payload"]["fileList"], list)
        self.assertEqual(response["payload"]["drive"], "CPU")

    @pytest.mark.skip
    def test_list_files_with_bad_drive(self):
        """Logger doesn't have a response paylod - not a usable test"""
        command = commands.ListFiles(self.base_topic, self.client_id)
        response = self.command_handler.send_command(command, drive="noway")

        self.assertEqual(response, None)

    def test_os_download_invalid_url(self):
        command = commands.OS(self.base_topic, self.client_id)
        url = "bad_url"
        response = self.command_handler.send_command(command, url)

        expected = {
            "success": False,
            "error": "OS Download Failed",
            "payload": {"error": "OS Download Failed"},
        }

        self.assertDictEqual(response, expected)

    def test_os_download_invalid_file(self):
        command = commands.OS(self.base_topic, self.client_id)
        url = "https://google.com"
        response = self.command_handler.send_command(command, url)

        expected = {
            "success": False,
            "error": "OS File Check Failed",
            "payload": {"error": "OS File Check Failed"},
        }

        self.assertDictEqual(response, expected)

    def test_program_download_invalid_url(self):
        command = commands.Program(self.base_topic, self.client_id)
        url = "bad_url"
        response = self.command_handler.send_command(command, url, "file")

        expected = {
            "success": False,
            "payload": {"error": "Program download failed"},
        }

        self.assertDictEqual(response, expected)

    def test_program_download_file_received(self):
        command = commands.Program(self.base_topic, self.client_id)
        url = "https://google.com"
        response = self.command_handler.send_command(command, url, "file")

        expected = {
            "success": True,
            "payload": {"success": "Program loaded successfully"},
        }

        self.assertDictEqual(response, expected)

    def test_program_delete(self):
        command = commands.Program(self.base_topic, self.client_id)
        url = "https://google.com"
        _ = self.command_handler.send_command(command, url, "test_file")
        # Give it a wee while to download and reboot - 6 wasn't enough
        time.sleep(10)

        command = commands.DeleteFile(self.base_topic, self.client_id)
        response = self.command_handler.send_command(command, "test_file")

        self.assertEqual(response["success"], True)

    def test_mqttconfig_download_invalid_url(self):
        command = commands.MQTTConfig(self.base_topic, self.client_id)
        url = "bad_url"
        response = self.command_handler.send_command(command, url)

        expected = {
            "success": False,
            "error": "MQTT Config file download failed, code: 0",
            "payload": {"error": "MQTT Config file download failed, code: 0"},
        }

        self.assertDictEqual(response, expected)

    def test_mqttconfig_download_file_received(self):
        command = commands.MQTTConfig(self.base_topic, self.client_id)
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
        command = commands.Reboot(self.base_topic, self.client_id)
        response = self.command_handler.send_command(command)

        expected = {
            "success": True,
            "payload": {"success": "Rebooting complete"},
        }

        self.assertDictEqual(response, expected)

    def test_set_constant(self):
        # script_url = "https://raw.githubusercontent.com/NERC-CEH/campbell-mqtt-control/refs/heads/feature/hardware-tests/tests/data/logger-script-constants-table.CR1X"
        # self.command_handler.send_command(commands.Program(self.base_topic, self.client_id), script_url, "script-constants")
        # self.command_handler.send_command(commands.RunProgram(self.base_topic, self.client_id), "script-constants")
        command = commands.EditConstants(self.base_topic, self.client_id)
        response = self.command_handler.send_command(command, B=1)

        expected = {
            "success": True,
            "payload": {"success": "Constant set"},
        }

        self.assertDictEqual(response, expected)

    def test_stop_script(self):
        command = commands.StopProgram(self.base_topic, self.client_id)
        response = self.command_handler.send_command(command)

        expected = {
            "success": True,
            "payload": {"success": "Script stopped"},
        }

        self.assertDictEqual(response, expected)

    def test_get_setting(self):
        setting = "PakBusAddress"
        command = commands.PublishSetting(self.base_topic, self.client_id)
        response = self.command_handler.send_command(command, setting)
        assert response["payload"].get("value", None)

    def test_set_setting(self):
        setting = "PakBusAddress"
        command = commands.SetSetting(self.topic, self.client_id)
        get_command = commands.PublishSetting(self.base_topic, self.client_id)

        # Re-run a couple of times in case we're setting a current value
        for value in range(1, 3):
            response = self.command_handler.send_command(command, setting, str(value))
            assert response["success"]
            response = self.command_handler.send_command(get_command, setting)
            assert str(response["payload"].get("value").strip()) == str(value)

        # Note that it fails unless we are explicitly casting to string type
        # Yes, this is a numeric setting in theory
        response = self.command_handler.send_command(command, setting, value)
        assert not response

        # Note that setting an impossible value still yields a success response
        value = "hello"
        response = self.command_handler.send_command(command, setting, value)
        assert response["success"]  # oh really
        response = self.command_handler.send_command(get_command, setting)
        with pytest.raises(AssertionError) as err:
            assert str(response["payload"].get("value").strip()) == str(value)


@pytest.mark.usefixtures("client_id", "mqtt_server", "topic")
class TestAWSCommandHandler(TestPahoCommandHandler):
    def setUp(self):
        self.base_topic = self.topic if self.topic is not None else "cs/v2"
        self.client = AWSConnection("testclient", self.server, 1883)
        self.command_handler = AWSCommandHandler(self.client)
