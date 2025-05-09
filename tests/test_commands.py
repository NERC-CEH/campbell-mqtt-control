import unittest
from campbellcontrol.commands import (
    OS,
    Program,
    MQTTConfig,
    EditConstants,
    Reboot,
    File,
    Settings,
    GetVar,
    SetVar,
    HistoricData,
    TalkThru,
)
from parameterized import parameterized


class TestMQTTCommands(unittest.TestCase):
    def setUp(self) -> None:
        self.group_id = "loggers/cr6"
        self.serial = "ABC#123!"

    def test_os_command(self):
        """Test the OS command."""
        expected_publish_topic = f"{self.group_id}/cc/{self.serial}/OS"
        expected_state_topic = f"{self.group_id}/state/{self.serial}/"
        expected_response_topic = f"{self.group_id}/cr/{self.serial}/OS"

        url = "http://example.com/firmware.bin"
        expected_payload = {"url": url}

        self.assertEqual(OS.publish_topic(self.group_id, self.serial), expected_publish_topic)
        self.assertEqual(OS.response_topic(self.group_id, self.serial), expected_response_topic)
        self.assertEqual(OS.state_topic(self.group_id, self.serial), expected_state_topic)
        self.assertEqual(OS.payload(url), expected_payload)

    def test_program_command(self):
        """Test the Program command."""
        expected_publish_topic = f"{self.group_id}/cc/{self.serial}/program"
        expected_response_topic = f"{self.group_id}/cr/{self.serial}/program"
        expected_state_topic = f"{self.group_id}/state/{self.serial}/"

        url = "http://example.com/programCR6.crb"
        filename = "testScript.crb"
        expected_payload = {"url": url, "fileName": filename}

        self.assertEqual(Program.publish_topic(self.group_id, self.serial), expected_publish_topic)
        self.assertEqual(Program.response_topic(self.group_id, self.serial), expected_response_topic)
        self.assertEqual(Program.state_topic(self.group_id, self.serial), expected_state_topic)
        self.assertEqual(Program.payload(url, filename), expected_payload)

    def test_mqtt_config_command(self):
        """Test the MQTT setting configuration command."""

        expected_publish_topic = f"{self.group_id}/cc/{self.serial}/mqttConfig"
        expected_response_topic = f"{self.group_id}/cr/{self.serial}/mqttConfig"
        expected_state_topic = f"{self.group_id}/state/{self.serial}/"

        url = "http://example.com/settings.bin"
        expected_payload = {
            "url": url,
        }

        self.assertEqual(MQTTConfig.publish_topic(self.group_id, self.serial), expected_publish_topic)
        self.assertEqual(
            MQTTConfig.response_topic(self.group_id, self.serial),
            expected_response_topic,
        )
        self.assertEqual(MQTTConfig.state_topic(self.group_id, self.serial), expected_state_topic)
        self.assertEqual(MQTTConfig.payload(url), expected_payload)

    def test_edit_constants_command(self):
        """Test the constants editing command."""
        expected_publish_topic = f"{self.group_id}/cc/{self.serial}/editConst"
        expected_response_topic = f"{self.group_id}/cr/{self.serial}/editConst"
        expected_state_topic = f"{self.group_id}/state/{self.serial}/"
        expected_payload = {
            "const1": "value1",
            "const2": "value2",
            "myconst": "myvalue",
        }

        self.assertEqual(
            EditConstants.publish_topic(self.group_id, self.serial),
            expected_publish_topic,
        )
        self.assertEqual(
            EditConstants.response_topic(self.group_id, self.serial),
            expected_response_topic,
        )
        self.assertEqual(EditConstants.state_topic(self.group_id, self.serial), expected_state_topic)
        self.assertEqual(EditConstants.payload(**expected_payload), expected_payload)

        self.assertEqual(
            EditConstants.payload({"const1": "value1", "const2": "value2"}, myconst="myvalue"),
            expected_payload,
        )

        with self.assertRaises(TypeError):
            EditConstants.payload(5)

    def test_reboot_command(self):
        """Test the reboot command."""
        expected_publish_topic = f"{self.group_id}/cc/{self.serial}/reboot"
        expected_response_topic = f"{self.group_id}/cr/{self.serial}/reboot"
        expected_state_topic = f"{self.group_id}/state/{self.serial}/"
        expected_payload = {"action": "reboot"}

        self.assertEqual(Reboot.publish_topic(self.group_id, self.serial), expected_publish_topic)
        self.assertEqual(Reboot.response_topic(self.group_id, self.serial), expected_response_topic)
        self.assertEqual(Reboot.state_topic(self.group_id, self.serial), expected_state_topic)
        self.assertEqual(Reboot.payload(), expected_payload)

    def test_file_list_command(self):
        """Test the file list command"""
        expected_publish_topic = f"{self.group_id}/cc/{self.serial}/fileControl"
        expected_response_topic = f"{self.group_id}/cr/{self.serial}/fileControl"
        expected_state_topic = f"{self.group_id}/state/{self.serial}/"

        drive = "USR"
        expected_payload_no_drive = {"action": "list"}
        expected_payload_with_drive = {"action": "list", "drive": drive}

        self.assertEqual(File.publish_topic(self.group_id, self.serial), expected_publish_topic)
        self.assertEqual(File.response_topic(self.group_id, self.serial), expected_response_topic)
        self.assertEqual(File.state_topic(self.group_id, self.serial), expected_state_topic)

        self.assertDictEqual(File.payload("list"), expected_payload_no_drive)
        self.assertDictEqual(File.payload("list", drive=drive), expected_payload_with_drive)
        self.assertDictEqual(
            File.payload("list", filename="fake", drive=drive),
            expected_payload_with_drive,
        )

    @parameterized.expand(["delete", "run"])
    def test_file_action_command(self, action: str):
        """Tests command for deleting files"""

        drive = "USR"
        filename = "myfile.crx"
        expected_payload_no_drive = {"action": action, "fileName": filename}
        expected_payload_with_drive = {
            "action": action,
            "fileName": filename,
            "drive": drive,
        }

        self.assertDictEqual(File.payload(action, filename), expected_payload_no_drive)
        self.assertDictEqual(File.payload(action, filename, drive), expected_payload_with_drive)

        with self.assertRaises(RuntimeError):
            File.payload(action)

    def test_file_stop_command(self):
        """Tests the program stop command"""

        expected_payload = {"action": "stop"}
        self.assertDictEqual(File.payload("stop"), expected_payload)

    def test_setting_set(self):
        expected_publish_topic = f"{self.group_id}/cc/{self.serial}/setting"
        expected_response_topic = f"{self.group_id}/cr/{self.serial}/setting"
        expected_state_topic = f"{self.group_id}/state/{self.serial}/"

        self.assertEqual(Settings.publish_topic(self.group_id, self.serial), expected_publish_topic)
        self.assertEqual(Settings.response_topic(self.group_id, self.serial), expected_response_topic)
        self.assertEqual(Settings.state_topic(self.group_id, self.serial), expected_state_topic)

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

        self.assertDictEqual(Settings.payload("set", setting_name, "2"), expected_payload_no_apply)
        self.assertDictEqual(
            Settings.payload("set", setting_name, "2", apply=True),
            expected_payload_apply,
            msg="apply field should be 'true' if argument is given",
        )
        self.assertDictEqual(
            Settings.payload("set", setting_name, "2", apply=False),
            expected_payload_no_apply,
            msg="apply field should not be present if set to false",
        )

        with self.assertRaises(RuntimeError):
            Settings.payload("set")
        with self.assertRaises(RuntimeError):
            Settings.payload("set", "SettingName")

    def test_setting_publish(self):
        """Test command for publishing settings."""

        name = "MySetting"
        expected_payload = {"action": "publish", "name": name}

        self.assertDictEqual(Settings.payload("publish", name), expected_payload)

        with self.assertRaises(RuntimeError):
            Settings.payload("publish")

    def test_setting_apply(self):
        """Test the setting apply command"""

        expected_payload = {"action": "apply", "apply": True}

        self.assertDictEqual(Settings.payload("apply"), expected_payload)
        self.assertDictEqual(Settings.payload("apply", "name", "value", apply=False), expected_payload)

    def test_get_variable(self):
        """Test the GetVar command"""

        expected_publish_topic = f"{self.group_id}/cc/{self.serial}/GetVar"
        expected_response_topic = f"{self.group_id}/cr/{self.serial}/GetVar"
        expected_state_topic = f"{self.group_id}/state/{self.serial}/"

        self.assertEqual(GetVar.publish_topic(self.group_id, self.serial), expected_publish_topic)
        self.assertEqual(GetVar.response_topic(self.group_id, self.serial), expected_response_topic)
        self.assertEqual(GetVar.state_topic(self.group_id, self.serial), expected_state_topic)

        expected_payload = {"name": "MyVar"}
        self.assertDictEqual(GetVar.payload("MyVar"), expected_payload)

    def test_set_variable(self):
        """Test the SetVar command"""

        expected_publish_topic = f"{self.group_id}/cc/{self.serial}/SetVar"
        expected_response_topic = f"{self.group_id}/cr/{self.serial}/SetVar"
        expected_state_topic = f"{self.group_id}/state/{self.serial}/"

        self.assertEqual(SetVar.publish_topic(self.group_id, self.serial), expected_publish_topic)
        self.assertEqual(SetVar.response_topic(self.group_id, self.serial), expected_response_topic)
        self.assertEqual(SetVar.state_topic(self.group_id, self.serial), expected_state_topic)

        expected_payload = {"name": "MyVar", "value": "55"}
        self.assertDictEqual(SetVar.payload("MyVar", "55"), expected_payload)

    def test_historic_data(self):
        """Test the historicData command"""

        expected_publish_topic = f"{self.group_id}/cc/{self.serial}/historicData"
        expected_response_topic = f"{self.group_id}/cr/{self.serial}/historicData"
        expected_state_topic = f"{self.group_id}/state/{self.serial}/"

        self.assertEqual(
            HistoricData.publish_topic(self.group_id, self.serial),
            expected_publish_topic,
        )
        self.assertEqual(
            HistoricData.response_topic(self.group_id, self.serial),
            expected_response_topic,
        )
        self.assertEqual(HistoricData.state_topic(self.group_id, self.serial), expected_state_topic)

        start = "2025"
        end = "2026"
        table = "DataTable"
        expected_payload = {"table": table, "start": start, "end": end}
        self.assertDictEqual(HistoricData.payload(table, start, end), expected_payload)

    def test_talkthru(self):
        """Test the talkThru command"""

        expected_publish_topic = f"{self.group_id}/cc/{self.serial}/talkThru"
        expected_response_topic = f"{self.group_id}/cr/{self.serial}/talkThru"
        expected_state_topic = f"{self.group_id}/state/{self.serial}/"

        self.assertEqual(
            TalkThru.publish_topic(self.group_id, self.serial),
            expected_publish_topic,
        )
        self.assertEqual(
            TalkThru.response_topic(self.group_id, self.serial),
            expected_response_topic,
        )
        self.assertEqual(TalkThru.state_topic(self.group_id, self.serial), expected_state_topic)

        port = "COM1"
        out_string = "test me"
        num_tries = "3"
        resp_delay = "5"
        abort = True

        expected_payload = {"comPort": port, "outString": out_string}
        expected_payload_with_tries = {**expected_payload, "numberTries": "3"}
        expected_payload_with_delay = {**expected_payload_with_tries, "respDelay": "5"}
        expected_payload_with_abort = {**expected_payload_with_delay, "abort": True}

        self.assertDictEqual(TalkThru.payload(port, out_string), expected_payload)
        self.assertDictEqual(
            TalkThru.payload(port, out_string, num_tries),
            expected_payload_with_tries,
        )
        self.assertDictEqual(
            TalkThru.payload(port, out_string, num_tries, resp_delay),
            expected_payload_with_delay,
        )
        self.assertDictEqual(
            TalkThru.payload(port, out_string, num_tries, resp_delay, abort),
            expected_payload_with_abort,
        )


if __name__ == "__main__":
    unittest.main()
