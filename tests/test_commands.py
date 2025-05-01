import unittest
from campbellcontrol.control import OS

class TestModuleMethods(unittest.TestCase):

    def test_os_command(self):
        """Test the topic method."""
        group_id = "loggers/cr6"
        serial = "ABC123"
        expected_publish_topic = f"{group_id}/cc/{serial}/OS"
        expected_response_topic = f"{group_id}/state/{serial}/OS"
        
        url = "http://example.com/firmware.bin"
        filename = "firmware.bin"
        expected_payload = {
            "url": url,
            "filename": filename
        }

        self.assertEqual(OS.publish_topic(group_id, serial), expected_publish_topic)
        self.assertEqual(OS.response_topic(group_id, serial), expected_response_topic)
        self.assertEqual(OS.payload(url, filename), expected_payload)


if __name__ == "__main__":
    unittest.main()