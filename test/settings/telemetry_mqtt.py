"""Datalogger configuration"""

# General settings.
main = {

    # Measurement intervals in seconds.
    'interval': {

        # Apply this interval if device is in field mode.
        'field': 0.0,

    },

    # Configure logging.
    'logging': {

        # Enable or disable logging completely.
        'enabled': True,

        # Log configuration settings at system startup.
        'configuration': False,

    },

}

# Networking configuration.
networking = {
    'wifi': {

        # Enable/disable WiFi completely.
        'enabled': True,

        # WiFi stations to connect to in STA mode.
        'stations': [
            {'ssid': 'FooBarWiFi', 'password': 'secret', 'timeout': 15.0},
        ],
    },
}

# Telemetry configuration.
telemetry = {
    'targets': [

        # JSON over MQTT: Kotori/MqttKit
        {
            # Enable/disable this telemetry target.
            'enabled': True,

            # Define telemetry endpoint and address information.
            'endpoint': 'mqtt://127.0.0.1',
            'topology': 'mqttkit',
            'address': {
                "realm": "mqttkit-1",
                "network": "testdrive",
                "gateway": "area-42",
                "node": "node-01",
            },

            # Whether to prettify telemetry payload on log output.
            'prettify_log': True,

        },

    ],
}

# Sensor configuration.
sensors = {

    # Whether to prettify sensor log output.
    'prettify_log': True,

    'system': [

        {
            # Sensor which reports free system memory.
            'type': 'system.memfree',
        },
        {
            # Sensor which reports system temperature.
            'type': 'system.temperature',
        },
        {
            # Sensor which reports system uptime metrics.
            'type': 'system.uptime',
        },
        {
            # Sensor which reports system WiFi metrics.
            'type': 'system.wifi',
        },

    ],
}
