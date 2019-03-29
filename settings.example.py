"""Datalogger configuration"""

# General settings.
main = {
    # Measurement interval.
    'interval': 1.0,
}

# Networking configuration.
networking = {
    'wifi': {
        # WiFi stations to connect to in STA mode.
        'stations': [

            # Variant 1: Using DHCP.
            {'ssid': 'FooBar', 'password': 'SECRET'},

            # Variant 2: Using static IP address.
            #{
            #    'ssid': 'FooBar',
            #    'password': 'SECRET',
            #    # Use static network configuration (ip, subnet_mask, gateway, DNS_server).
            #    'ifconfig': ('192.168.42.42', '255.255.255.0', '192.168.42.1', '192.168.42.1'),
            #},
        ],

        # The maximum time in milliseconds to wait for the connection to succeed.
        'timeout': 15000,
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

        # JSON over MQTT
        {
            # Enable/disable this telemetry target.
            'enabled': True,

            # Define telemetry endpoint and address information.
            'endpoint': 'mqtt://daq.example.org',
            'address': {
                "realm": "workbench",
                "network": "testdrive",
                "gateway": "area-42",
                "node": "node-01-mqtt-json",
            },
        },

        # JSON over HTTP
        {
            # Enable/disable this telemetry target.
            'enabled': False,

            # Define telemetry endpoint and address information.
            'endpoint': 'https://daq.example.org/api',
            'address': {
                "realm": "workbench",
                "network": "testdrive",
                "gateway": "area-42",
                "node": "node-01-http-json",
            },

            # Use alternative, non-HTTPS endpoint.
            # 'endpoint': 'http://daq.example.org/api-notls',

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
    'registry': {
        'hx711': {
            'pin_dout': 'P21',
            'pin_pdsck': 'P22',
            'scale': 11.026667,
            'offset': 130800.0,
        },
        'ds18x20': {
            'bus': 'onewire:0',
        },
        'bme280': {
            'bus': 'i2c:0',
            # TODO: make sensor be initialized with address
            # 'address': 0x77,
        },
        'bme280_1': {
            'bus': 'i2c:1',
        },
        'pytrack': {
            'bus': 'i2c:1',
        },
        'moisture': {
            'pin_adc_in': 'P15',
            'scaling': 4.096,
        },
        'waterlevel': {
            'pin_adc_in': 'P18'
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

