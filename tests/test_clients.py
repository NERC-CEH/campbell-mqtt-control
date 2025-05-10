from unittest import TestCase
from unittest.mock import patch, MagicMock
from campbellcontrol.connection.generic import PahoConnection
from campbellcontrol.connection.interface import Connection
import paho.mqtt.client
from paho.mqtt.client import MQTTMessage
from typing import Callable


class TestPahoClient(TestCase):
    """Test the Paho MQTT client"""

    def test_instantiation(self):
        client = PahoConnection("endpoint", 1883)

        self.assertIsInstance(client.client, paho.mqtt.client.Client)

        self.assertEqual(client.client.on_message, client._on_message)
        self.assertEqual(client.client.on_connect, client._on_connect)
        self.assertEqual(client.client.on_disconnect, client._on_disconnect)
        self.assertEqual(client.client.on_subscribe, client._on_subscribe)
        self.assertEqual(client.client.on_unsubscribe, client._on_unsubscribe)

    @patch("campbellcontrol.connection.generic.logger.info")
    def test_on_message(self, mock):
        client = PahoConnection("endpoint", 1883)
        msg = MQTTMessage(topic=b"topic")
        client._on_message(client, "userdata", msg)
        self.assertTrue(mock.called)

    @patch("campbellcontrol.connection.generic.logger.info")
    def test_on_connect(self, mock):
        PahoConnection._on_connect(1, 2, 3, 4, 5)
        self.assertTrue(mock.called)

    @patch("campbellcontrol.connection.generic.logger.info")
    @patch("campbellcontrol.connection.generic.logger.error")
    def test_on_disconnect(self, mock_error, mock_info):
        # non-zero reason code should log an error
        PahoConnection._on_disconnect("client", "userdata", "flags", 1, "properties")
        self.assertTrue(mock_error.called)

        PahoConnection._on_disconnect("client", "userdata", "flags", 0, "properties")
        self.assertTrue(mock_info.called)

    @patch("campbellcontrol.connection.generic.logger.info")
    def test_on_subscribe(self, mock):
        PahoConnection._on_subscribe(1, 2, 3, 4, 5)
        self.assertTrue(mock.called)

    @patch("campbellcontrol.connection.generic.logger.info")
    def test_on_unsubscribe(self, mock):
        PahoConnection._on_unsubscribe(1, 2, 3, 4, 5)
        self.assertTrue(mock.called)

    def test_methods_passed_to_client(self):
        endpoint = "endpoint"
        port = 1883
        with patch.object(PahoConnection, "get_client", MagicMock) as mock:
            conn = PahoConnection(endpoint, port)
            conn.connect()
            conn.client.connect.assert_called_once_with(endpoint, port)

            conn.disconnect()
            conn.client.disconnect.assert_called_once()

            conn.subscribe("sub_topic")
            conn.client.subscribe.assert_called_once_with("sub_topic")

            conn.unsubscribe("sub_topic")
            conn.client.unsubscribe.assert_called_once_with("sub_topic")

            conn.publish("sub_topic", "payload", extra_arg=1)
            conn.client.publish.assert_called_once_with("sub_topic", "payload", extra_arg=1)
