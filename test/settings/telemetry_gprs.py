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
        'enabled': False,

    },

    # GPRS/SIM800
    # https://github.com/hiveeyes/pythings-sim800
    'gprs': {

        # General settings.
        'enabled': True,
        'driver': 'pythings-sim800',

        # Network settings.
        'apn': 'apn.example.net',

        # Main power switch, connected to a SY8089 step-down converter on a TTGO T-Call SIM800.
        # https://github.com/Xinyuan-LilyGO/TTGO-T-Call
        # https://datasheet.lcsc.com/szlcsc/Silergy-Corp-SY8089AAAC_C78988.pdf
        # https://community.hiveeyes.org/t/minimal-hardware-design-gsm-stockwaage-mit-ttgo-t-call/2906/19
        'pin_power': 'P23',

        # Modem action and communication pins.
        # https://simcom.ee/documents/SIM800/SIM800_Hardware%20Design_V1.09.pdf
        'pin_pwrkey': 'P4',
        'pin_reset': 'P5',
        'pin_txd': 'P26',
        'pin_rxd': 'P27',
    },
}

# Telemetry configuration.
telemetry = {
    'targets': [

        # JSON over HTTP over GPRS: Kotori/MQTTKit
        {
            # Enable/disable this telemetry target.
            'enabled': True,

            # Define outbound interface.
            'interface': 'gprs',

            # Define telemetry endpoint and address information.
            'endpoint': 'https://daq.example.org/api',
            'topology': 'mqttkit',
            'address': {
                "realm": "workbench",
                "network": "testdrive",
                "gateway": "area-42",
                "node": "node-01-http-json",
            },

            # Use alternative, non-HTTPS endpoint.
            # 'endpoint': 'http://daq.example.org/api-notls',

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
