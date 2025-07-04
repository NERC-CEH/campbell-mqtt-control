import unittest
import pytest
from campbellcontrol.commands import commands


class TestMQTTCommands(unittest.TestCase):
    def setUp(self) -> None:
        self.group_id = "loggers/cr6"
        self.model = "cr1000x"
        self.serial = "ABC#123!"
        self.device_id = f"{self.model}/{self.serial}"

    def test_os_command(self):
        """Test the OS command."""
        expected_publish_topic = f"{self.group_id}/cc/{self.device_id}/OS"
        expected_state_topic = f"{self.group_id}/state/{self.device_id}/"
        expected_response_topic = f"{self.group_id}/cr/{self.device_id}/OS"

        url = "http://example.com/firmware.bin"
        expected_payload = {"url": url}
        command = commands.OS(self.group_id, self.serial)

        self.assertEqual(command.publish_topic, expected_publish_topic)
        self.assertEqual(command.response_topic, expected_response_topic)
        self.assertEqual(command.state_topic, expected_state_topic)
        self.assertEqual(command.payload(url), expected_payload)

    def test_program_command(self):
        """Test the Program command."""
        expected_publish_topic = f"{self.group_id}/cc/{self.device_id}/program"
        expected_response_topic = f"{self.group_id}/cr/{self.device_id}/program"
        expected_state_topic = f"{self.group_id}/state/{self.device_id}/"

        url = "http://example.com/programCR6.crb"
        filename = "testScript.crb"
        expected_payload = {"url": url, "fileName": filename}
        command = commands.Program(self.group_id, self.serial)
        self.assertEqual(command.publish_topic, expected_publish_topic)
        self.assertEqual(command.response_topic, expected_response_topic)
        self.assertEqual(command.state_topic, expected_state_topic)
        self.assertEqual(command.payload(url, filename), expected_payload)

    def test_mqtt_config_command(self):
        """Test the MQTT setting configuration command."""

        expected_publish_topic = f"{self.group_id}/cc/{self.device_id}/mqttConfig"
        expected_response_topic = f"{self.group_id}/cr/{self.device_id}/mqttConfig"
        expected_state_topic = f"{self.group_id}/state/{self.device_id}/"

        url = "http://example.com/settings.bin"
        expected_payload = {
            "url": url,
        }

        command = commands.MQTTConfig(self.group_id, self.serial)

        self.assertEqual(command.publish_topic, expected_publish_topic)
        self.assertEqual(
            command.response_topic,
            expected_response_topic,
        )
        self.assertEqual(command.state_topic, expected_state_topic)
        self.assertEqual(command.payload(url), expected_payload)

    def test_config_device_options(self):
        # can't use pytest.mark.parametrize with unittest classes
        for model in ["cr6", "cr1000x", "madeup"]:
            expected_publish_topic = f"{self.group_id}/cc/{model}/{self.serial}/mqttConfig"
            expected_response_topic = f"{self.group_id}/cr/{model}/{self.serial}/mqttConfig"
            expected_state_topic = f"{self.group_id}/state/{model}/{self.serial}/"

            command = commands.MQTTConfig(self.group_id, self.serial, model)

            self.assertEqual(command.publish_topic, expected_publish_topic)
            self.assertEqual(
                command.response_topic,
                expected_response_topic,
            )
            self.assertEqual(command.state_topic, expected_state_topic)

    def test_edit_constants_command(self):
        """Test the constants editing command."""
        expected_publish_topic = f"{self.group_id}/cc/{self.device_id}/editConst"
        expected_response_topic = f"{self.group_id}/cr/{self.device_id}/editConst"
        expected_state_topic = f"{self.group_id}/state/{self.device_id}/"
        expected_payload = {
            "const1": "value1",
            "const2": "value2",
            "myconst": "myvalue",
        }

        command = commands.EditConstants(self.group_id, self.serial)

        self.assertEqual(
            command.publish_topic,
            expected_publish_topic,
        )
        self.assertEqual(
            command.response_topic,
            expected_response_topic,
        )
        self.assertEqual(command.state_topic, expected_state_topic)
        self.assertEqual(command.payload(**expected_payload), expected_payload)

        self.assertEqual(
            command.payload({"const1": "value1", "const2": "value2"}, myconst="myvalue"),
            expected_payload,
        )

        with self.assertRaises(TypeError):
            command.payload(5)

    def test_reboot_command(self):
        """Test the reboot command."""
        expected_publish_topic = f"{self.group_id}/cc/{self.device_id}/reboot"
        expected_response_topic = f"{self.group_id}/cr/{self.device_id}/reboot"
        expected_state_topic = f"{self.group_id}/state/{self.device_id}/"
        expected_payload = {"action": "reboot"}

        command = commands.Reboot(self.group_id, self.serial)
        self.assertEqual(command.publish_topic, expected_publish_topic)
        self.assertEqual(command.response_topic, expected_response_topic)
        self.assertEqual(command.state_topic, expected_state_topic)
        self.assertEqual(command.payload(), expected_payload)

    def test_file_list_command(self):
        """Test the file list command"""
        expected_publish_topic = f"{self.group_id}/cc/{self.device_id}/fileControl"
        expected_response_topic = f"{self.group_id}/cr/{self.device_id}/fileControl"
        expected_state_topic = f"{self.group_id}/state/{self.device_id}/"
        command = commands.ListFiles(self.group_id, self.serial)
        drive = "USR"
        expected_payload_no_drive = {"action": "list"}
        expected_payload_with_drive = {"action": "list", "drive": drive}

        self.assertEqual(command.publish_topic, expected_publish_topic)
        self.assertEqual(command.response_topic, expected_response_topic)
        self.assertEqual(command.state_topic, expected_state_topic)

        self.assertDictEqual(command.payload(), expected_payload_no_drive)
        self.assertDictEqual(command.payload(drive=drive), expected_payload_with_drive)

    def test_delete_file_command(self):
        """Tests command for deleting files"""
        command = commands.DeleteFile(self.group_id, self.serial)
        drive = "USR"
        filename = "myfile.crx"
        expected_payload_no_drive = {"action": "delete", "fileName": filename}
        expected_payload_with_drive = {
            "action": "delete",
            "fileName": filename,
            "drive": drive,
        }

        self.assertDictEqual(command.payload(filename), expected_payload_no_drive)
        self.assertDictEqual(command.payload(filename, drive), expected_payload_with_drive)

    def test_run_file_command(self):
        """Tests command for running a program"""
        command = commands.RunProgram(self.group_id, self.serial)
        filename = "myfile.crx"
        expected_payload = {"action": "run", "fileName": filename}

        self.assertDictEqual(command.payload(filename), expected_payload)

    def test_file_stop_command(self):
        """Tests the program stop command"""
        command = commands.StopProgram(self.group_id, self.serial)
        expected_payload = {"action": "stop"}
        self.assertDictEqual(command.payload(), expected_payload)

    def test_setting_set(self):
        expected_publish_topic = f"{self.group_id}/cc/{self.device_id}/setting"
        expected_response_topic = f"{self.group_id}/cr/{self.device_id}/setting"
        expected_state_topic = f"{self.group_id}/state/{self.device_id}/"

        command = commands.SetSetting(self.group_id, self.serial)

        self.assertEqual(command.publish_topic, expected_publish_topic)
        self.assertEqual(command.response_topic, expected_response_topic)
        self.assertEqual(command.state_topic, expected_state_topic)

        setting_name = "PakBusAddress"
        expected_payload_no_apply = {
            "action": "set",
            "name": setting_name,
            "value": "2",
        }
        expected_payload_apply = {
            "action": "set",
            "name": setting_name,
            "value": "2",
            "apply": True,
        }

        self.assertDictEqual(command.payload(setting_name, "2"), expected_payload_no_apply)
        self.assertDictEqual(
            command.payload(setting_name, "2", apply=True),
            expected_payload_apply,
            msg="apply field should be 'true' if argument is given",
        )
        self.assertDictEqual(
            command.payload(setting_name, "2", apply=False),
            expected_payload_no_apply,
            msg="apply field should not be present if set to false",
        )

    def test_setting_publish(self):
        """Test command for publishing settings."""

        name = "MySetting"
        expected_payload = {"action": "publish", "name": name}
        command = commands.PublishSetting(self.group_id, self.serial)

        self.assertDictEqual(command.payload(name), expected_payload)

    def test_setting_apply(self):
        """Test the setting apply command"""

        expected_payload = {"action": "apply", "apply": True}
        command = commands.ApplySettings(self.group_id, self.serial)
        self.assertDictEqual(command.payload(), expected_payload)

    def test_get_variable(self):
        """Test the GetVar command"""

        expected_publish_topic = f"{self.group_id}/cc/{self.device_id}/getVar"
        expected_response_topic = f"{self.group_id}/cr/{self.device_id}/getVar"
        expected_state_topic = f"{self.group_id}/state/{self.device_id}/"

        command = commands.GetVar(self.group_id, self.serial)

        self.assertEqual(command.publish_topic, expected_publish_topic)
        self.assertEqual(command.response_topic, expected_response_topic)
        self.assertEqual(command.state_topic, expected_state_topic)

        expected_payload = {"name": "MyVar"}
        self.assertDictEqual(command.payload("MyVar"), expected_payload)

    def test_set_variable(self):
        """Test the SetVar command"""

        expected_publish_topic = f"{self.group_id}/cc/{self.device_id}/setVar"
        expected_response_topic = f"{self.group_id}/cr/{self.device_id}/setVar"
        expected_state_topic = f"{self.group_id}/state/{self.device_id}/"

        command = commands.SetVar(self.group_id, self.serial)

        self.assertEqual(command.publish_topic, expected_publish_topic)
        self.assertEqual(command.response_topic, expected_response_topic)
        self.assertEqual(command.state_topic, expected_state_topic)

        expected_payload = {"name": "MyVar", "value": "55"}
        self.assertDictEqual(command.payload("MyVar", "55"), expected_payload)

    def test_historic_data(self):
        """Test the historicData command"""

        expected_publish_topic = f"{self.group_id}/cc/{self.device_id}/historicData"
        expected_response_topic = f"{self.group_id}/cr/{self.device_id}/historicData"
        expected_state_topic = f"{self.group_id}/state/{self.device_id}/"
        command = commands.HistoricData(self.group_id, self.serial)

        self.assertEqual(
            command.publish_topic,
            expected_publish_topic,
        )
        self.assertEqual(
            command.response_topic,
            expected_response_topic,
        )
        self.assertEqual(command.state_topic, expected_state_topic)

        start = "2025"
        end = "2026"
        table = "DataTable"
        expected_payload = {"table": table, "start": start, "end": end}
        self.assertDictEqual(command.payload(table, start, end), expected_payload)

    def test_talkthru(self):
        """Test the talkThru command"""

        expected_publish_topic = f"{self.group_id}/cc/{self.device_id}/talkThru"
        expected_response_topic = f"{self.group_id}/cr/{self.device_id}/talkThru"
        expected_state_topic = f"{self.group_id}/state/{self.device_id}/"

        command = commands.TalkThru(self.group_id, self.serial)

        self.assertEqual(
            command.publish_topic,
            expected_publish_topic,
        )
        self.assertEqual(
            command.response_topic,
            expected_response_topic,
        )
        self.assertEqual(command.state_topic, expected_state_topic)

        port = "COM1"
        out_string = "test me"
        num_tries = "3"
        resp_delay = "5"
        abort = True

        expected_payload = {"comPort": port, "outString": out_string}
        expected_payload_with_tries = {**expected_payload, "numberTries": "3"}
        expected_payload_with_delay = {**expected_payload_with_tries, "respDelay": "5"}
        expected_payload_with_abort = {**expected_payload_with_delay, "abort": True}

        self.assertDictEqual(command.payload(port, out_string), expected_payload)
        self.assertDictEqual(
            command.payload(port, out_string, num_tries),
            expected_payload_with_tries,
        )
        self.assertDictEqual(
            command.payload(port, out_string, num_tries, resp_delay),
            expected_payload_with_delay,
        )
        self.assertDictEqual(
            command.payload(port, out_string, num_tries, resp_delay, abort),
            expected_payload_with_abort,
        )


class TestCommand(commands.Command):
    command_name = "test"

    def payload(self):
        return {"default": "payload"}


class TestHandlers(unittest.TestCase):
    def setUp(self) -> None:
        self.group_id = "loggers/cr6"
        self.serial = "ABC#123!"

    def test_base_handler_success(self):
        """Test the base handler payload"""
        payload = b'{"success": "Did a thing"}'
        expected_payload = {"payload": {"success": "Did a thing"}, "success": True}
        command = TestCommand("a", "b")
        self.assertDictEqual(command.handler("topic", payload), expected_payload)

    def test_base_handler_error(self):
        """Test the base handler payload"""
        payload = b'{"error": "Did the wrong thing"}'
        expected_payload = {
            "payload": {"error": "Did the wrong thing"},
            "success": False,
            "error": "Did the wrong thing",
        }
        command = TestCommand("a", "b")
        self.assertDictEqual(command.handler("topic", payload), expected_payload)

    def test_unexpected_payload(self):
        """Test when an unexpected payload is received"""
        payload = b'{"unexpected": "Did something"}'
        expected = None
        command = TestCommand("a", "b")
        self.assertEqual(command.handler("topic", payload), expected)

    def test_list_files_handler(self):
        """Test the list files handler"""
        payload = b'{"fileList": ["file1", "file2"]}'
        expected_payload = {
            "payload": {"fileList": ["file1", "file2"]},
            "success": True,
        }
        self.assertDictEqual(commands.ListFiles.handler("topic", payload), expected_payload)

    def test_list_files_handler_error(self):
        """Test the list files handler"""
        payload = b'{"error": "Did the wrong thing"}'
        expected_payload = {
            "payload": {"error": "Did the wrong thing"},
            "success": False,
            "error": "Did the wrong thing",
        }
        self.assertDictEqual(commands.ListFiles.handler("topic", payload), expected_payload)

    def test_talkthru_handler(self):
        """Test the talkThru handler"""
        payload = b'{"response": "Did a thing"}'
        expected_payload = {"payload": {"response": "Did a thing"}, "success": True}
        self.assertDictEqual(commands.TalkThru.handler("topic", payload), expected_payload)

    def test_talkthru_handler_error(self):
        """Test the talkThru handler"""
        payload = b'{"error": "Did the wrong thing"}'

        with self.assertRaises(RuntimeError):
            commands.TalkThru.handler("topic", payload)


if __name__ == "__main__":
    unittest.main()
