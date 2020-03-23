# Monkeypatch the whole machinery to be executable on CPython.

from test.util.micropython import monkeypatch
monkeypatch()

from test.util.terkin import monkeypatch_terkin
monkeypatch_terkin()

# Fixture to capture MQTT messages.
from test.util.mqtt import capmqtt

# Fixture to start Mosquitto within Docker container.
from test.util.mosquitto import mosquitto

# Fixture to emulate Pycom's "pycom.{nvs_get,nvs_set} API".
from test.util.pycom import pycom_nvram
