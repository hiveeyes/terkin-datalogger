"""Datalogger configuration"""

# General settings.
main = {

    # Configure logging.
    'logging': {

        # Enable or disable logging completely.
        'enabled': True,

    },

}

# Networking configuration.
networking = {

    'wifi': {

        # Enable/disable WiFi completely.
        'enabled': False,

    },

    # LoRaWAN/TTN
    'lora': {
        'enabled': True,
        'otaa': {
            'region': 'EU868',
            'adr': False,
            'device_eui': '80B3D549904B5FD0',
            'application_eui': '80B3D57ED0018E9D',
            'application_key': '830A4A65419E669393C0ED4DDB32372D',
        },
        'antenna_attached': True,
    },

}

# Telemetry configuration.
telemetry = {
    'targets': [

        # CayenneLPP over TTN-LoRa
        {
            # Enable/disable this telemetry target.
            'enabled': True,

            'endpoint': 'lora://',
            'format': 'lpp',
            'settings': {
                'size': 12,
                'datarate': 0,
            },
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
