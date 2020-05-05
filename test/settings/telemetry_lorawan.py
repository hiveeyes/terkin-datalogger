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
        'region': 'EU868',
        'adr': False,
        'antenna_attached': True,
        'activation': 'otaa',
        'otaa': {
            # No worries, these are not real values.
            'device_eui': '80B3D549904B5FD0',
            'application_eui': '80B3D57ED0018E9D',
            'application_key': '830A4A65419E669393C0ED4DDB32372D',
        },
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
            'format': 'lpp-hiveeyes',
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
            'enabled': True,
        },
        {
            # Sensor which reports system temperature.
            'type': 'system.temperature',
            'enabled': True,
        },
        {
            # Sensor which reports system uptime metrics.
            'type': 'system.uptime',
            'enabled': True,
        },
        {
            # Sensor which reports system WiFi metrics.
            'type': 'system.wifi',
            'enabled': True,
        },

    ],
}
