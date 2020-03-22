# -*- coding: utf-8 -*-
# (c) 2020 Richard Pobering <richard@hiveeyes.org>
# (c) 2020 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import time
import pytest
import logging
import threading

logger = logging.getLogger(__name__)


class MQTTClient(threading.Thread):

    def run(self):
        self.buffer = []
        logger.info('[PYTEST] Connecting to MQTT')
        import paho.mqtt.client as mqtt
        client = mqtt.Client("P1")
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.on_socket_open = self.on_socket_open

        client.connect('localhost', port=1883)
        client.loop_start()
        client.subscribe("mqttkit-1/#")

    def on_socket_open(self, client, userdata, sock):
        logger.info('[PYTEST] Opened socket to MQTT')

    def on_connect(self, client, userdata, flags, rc):
        logger.info('[PYTEST] Connected to MQTT broker')

    def on_message(self, client, userdata, message):
        data = str(message.payload.decode("utf-8"))
        self.buffer.append(data)
        logger.info("[PYTEST] MQTT message received: %s", data)


class MqttCaptureFixture:
    """Provides access and control of log capturing."""

    def __init__(self, item) -> None:
        """Creates a new funcarg."""
        self._item = item

        self.mqtt_client = MQTTClient()
        self.mqtt_client.start()
        time.sleep(0.1)

    def _finalize(self) -> None:
        """Finalizes the fixture.
        """
        pass

    def buffer(self):
        return self.mqtt_client.buffer


@pytest.fixture
def capmqtt(request):
    """Access and control MQTT messages.

    """
    result = MqttCaptureFixture(request.node)
    yield result
    result._finalize()
