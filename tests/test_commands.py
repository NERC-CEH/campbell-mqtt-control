import unittest
from campbellcontrol.control import OS, Program, MQTTConfig, EditConstants


class TestMQTTCommands(unittest.TestCase):
    def test_os_command(self):
        """Test the OS command."""
        group_id = "loggers/cr6"
        serial = "ABC123"
        expected_publish_topic = f"{group_id}/cc/{serial}/OS"
        expected_response_topic = f"{group_id}/state/{serial}/OS"

        url = "http://example.com/firmware.bin"
        filename = "firmware.bin"
        expected_payload = {"url": url, "filename": filename}

        self.assertEqual(OS.publish_topic(group_id, serial), expected_publish_topic)
        self.assertEqual(OS.response_topic(group_id, serial), expected_response_topic)
        self.assertEqual(OS.payload(url, filename), expected_payload)

    def test_program_command(self):
        """Test the Program command."""
        group_id = "loggers/cr6/v2"
        serial = "ABC#123"
        expected_publish_topic = f"{group_id}/cc/{serial}/program"
        expected_response_topic = f"{group_id}/state/{serial}/program"

        url = "http://example.com/programCR6.crb"
        filename = "testScript.crb"
        expected_payload = {"url": url, "filename": filename}

        self.assertEqual(Program.publish_topic(group_id, serial), expected_publish_topic)
        self.assertEqual(Program.response_topic(group_id, serial), expected_response_topic)
        self.assertEqual(Program.payload(url, filename), expected_payload)

    def test_mqtt_config_command(self):
        """Test the MQTT setting configuration command."""
        group_id = "loggers/cr6/v2"
        serial = "ABC#123"
        expected_publish_topic = f"{group_id}/cc/{serial}/mqttConfig"
        expected_response_topic = f"{group_id}/state/{serial}/mqttConfig"

        url = "http://example.com/settings.bin"
        expected_payload = {
            "url": url,
        }

        self.assertEqual(MQTTConfig.publish_topic(group_id, serial), expected_publish_topic)
        self.assertEqual(MQTTConfig.response_topic(group_id, serial), expected_response_topic)
        self.assertEqual(MQTTConfig.payload(url), expected_payload)

    def test_edit_constants_command(self):
        """Test the MQTT setting configuration command."""
        group_id = "loggers/cr6/v2"
        serial = "ABC#123"
        expected_publish_topic = f"{group_id}/cc/{serial}/editConst"
        expected_response_topic = f"{group_id}/state/{serial}/editConst"

        expected_payload = {"const1": "value1", "const2": "value2", "myconst": "myvalue"}

        self.assertEqual(EditConstants.publish_topic(group_id, serial), expected_publish_topic)
        self.assertEqual(EditConstants.response_topic(group_id, serial), expected_response_topic)
        self.assertEqual(EditConstants.payload(**expected_payload), expected_payload)

        self.assertEqual(
            EditConstants.payload({"const1": "value1", "const2": "value2"}, myconst="myvalue"), expected_payload
        )

        with self.assertRaises(TypeError):
            EditConstants.payload(5)


if __name__ == "__main__":
    unittest.main()
