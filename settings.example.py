"""Datalogger configuration"""

# General settings.
MAINLOOP_INTERVAL = 1.0

# Known WiFi credentials.
WIFI_NETWORKS = [
    ('<YOUR_WIFI_SSID_1>', '<WIFI_PASS_1>'),
    ('<YOUR_WIFI_SSID_2>', '<WIFI_PASS_2>'),
]

# Telemetry configuration.
TELEMETRY_ENDPOINT = 'mqtt://daq.example.org'
TELEMETRY_ADDRESS = {
    "realm": "acme",
    "network": "testdrive",
    "gateway": "area-42",
    "node": "node-1",
}
