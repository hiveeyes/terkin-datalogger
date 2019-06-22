"""Datalogger configuration"""

# General settings.
main = {

    # Measurement interval in seconds.
    # TODO: Please note this is not the _real thing_ yet at it will just use
    #       this value to apply to ``time.sleep()`` after each duty cycle.
    'interval': 15.0,

    # Whether to use deep sleep between measurement cycles.
    'deepsleep': True,

    # Configure logging.
    'logging': {

        # Enable or disable logging completely.
        'enabled': True,

        # Log configuration settings at system startup.
        'configuration': True,
    },

    # Configure RGB-LED.
    'rgb_led': {
        'heartbeat': True,
    },

}

# Interface settings.
interfaces = {
    'uart0': {
        'terminal': True,
    }
}

# Networking configuration.
networking = {
    'wifi': {
        # WiFi stations to connect to in STA mode.
        'stations': [

            # Variant 1: Use DHCP.

            # Variant 1a: Straight forward.
            {'ssid': 'FooBar', 'password': 'SECRET'},

            # Variant 1b: Configure timeout (default: 15 seconds).
            # Configure this to decrease or increase the maximum time in
            # seconds to wait for the connection to succeed.
            #{'ssid': 'FooBar', 'password': 'SECRET', 'timeout': 5.0},

            # Variant 2: Using static IP address.
            #{
            #    'ssid': 'FooBar',
            #    'password': 'SECRET',
            #    # Use static network configuration (ip, subnet_mask, gateway, DNS_server).
            #    'ifconfig': ('192.168.42.42', '255.255.255.0', '192.168.42.1', '192.168.42.1'),
            #},
        ],
    },
    'lora': {
        'otaa': {
            'frequency': 868100000,
            'region': 'LoRa.EU868',
            'datarate': 0,
            'device_eui': '<GENERATED_FROM_LORA_MAC>',
            'application_eui': '<REGISTRATION NEEDED>',
            'application_key': '<REGISTRATION NEEDED>',
        },
        'antenna_attached': False,
    }
}

# Telemetry configuration.
telemetry = {
    'targets': [

        # JSON over MQTT: Kotori/MQTTKit
        {
            # Enable/disable this telemetry target.
            'enabled': True,

            # Define telemetry endpoint and address information.
            'endpoint': 'mqtt://daq.example.org',
            'topology': 'mqttkit',
            'address': {
                "realm": "workbench",
                "network": "testdrive",
                "gateway": "area-42",
                "node": "node-01-mqtt-json",
            },
        },

        # JSON over HTTP: Kotori/MQTTKit
        {
            # Enable/disable this telemetry target.
            'enabled': False,

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

        # JSON over HTTP: Basic
        {
            # Enable/disable this telemetry target.
            'enabled': False,

            # Define telemetry endpoint and address information.
            # https://beeceptor.com/
            # https://requestbin.fullcontact.com/
            'endpoint': 'https://test.free.beeceptor.com/api/sensors',
            'data': {
                'key': '## API_KEY ##',
            },
        },

        # CayenneLPP over MQTT, Base64 encoded
        {
            # Enable/disable this telemetry target.
            'enabled': False,

            # Define telemetry endpoint and address information.
            'endpoint': 'mqtt://daq.example.org',
            'address': {
                "realm": "workbench",
                "network": "testdrive",
                "gateway": "area-42",
                "node": "node-01-mqtt-lpp",
            },
            'format': 'lpp',
            'encode': 'base64',
        }
    ],
}

# Sensor configuration.
sensors = {
    'system': {

        # Adjust voltage divider resistor values matching the board.
        #
        # See also
        # - https://forum.pycom.io/topic/3776/adc-use-to-measure-battery-level-vin-level
        # - https://github.com/hiveeyes/hiveeyes-micropython-firmware/issues/5
        # - https://community.hiveeyes.org/t/batterieuberwachung-voltage-divider-und-attenuation-fur-microypthon-firmware/2128
        #
        # As a reference (all readings using 6dB attenuation unless otherwise noted):
        #
        # - Pycom Expansion board v3.0: 115 kΩ / 56 kΩ
        # - Pycom Expansion board v3.1: 1 MΩ / 1 MΩ
        # - Pycom Expansion board v3.2: 1 MΩ / 1 MΩ
        # - BOB-HAT-V5: 1 MΩ / 470 kΩ or 220 kΩ
        # - BOB-SHIELD: 10 MΩ / 2 MΩ
        # - Air Quality monitor: 100kΩ / 47 kΩ, measured with 2.5dB attenuation

        # These settings are matching the resistor values of the Pycom Expansion Board 3.1 and 3.2.
        'vcc': {

            'pin': 'P16',

            # Main resistor value (R1).
            'resistor_r1': 1000,

            # Resistor between input pin and ground (R2).
            'resistor_r2': 1000,
        },

        # Settings for button events, e.g. through touch pads.
        'buttons': {
            'enabled': False,
        },
    },
    'registry': {
        'hx711': {
            'address': 0x00,
            'pin_dout': 'P22',
            'pin_pdsck': 'P21',
            'scale': 4.424242,
            'offset': -73000.0,
        },
        'ds18x20': {
            'bus': 'onewire:0',
        },
        'bme280_1': {
            'bus': 'i2c:0',
        },
        'bme280_2': {
            'bus': 'i2c:1',
            'address': 0x77,
        },
    },
    'busses': [
        {
            "family": "i2c",
            "number": 0,
            "enabled": True,
            "pin_sda": "P9",
            "pin_scl": "P10",
        },
        {
            "family": "i2c",
            "number": 1,
            "enabled": False,
            "pin_sda": "P22",
            "pin_scl": "P21",
        },
        {
            "family": "onewire",
            "number": 0,
            "enabled": True,
            "pin_data": "P11",
        },
    ]
}

