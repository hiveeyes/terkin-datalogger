"""Datalogger configuration"""

# General settings.
main = {
    # Measurement interval in seconds.
    # TODO: Please note this is not the _real thing_ yet at it will just use
    #       this value to apply to ``time.sleep()`` after each duty cycle.
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
}

# Telemetry configuration.
telemetry = {
    'targets': [

        # JSON over MQTT
        {
            # Enable/disable this telemetry target.
            'enabled': True,

            # Define telemetry endpoint and address information.
            'endpoint': 'mqtt://swarm.hiveeyes.org',
            'address': {
                "realm": "hiveeyes",
                "network": "testdrive",
                "gateway": "area-test",
                "node": "terkin-test-01",
            },
        },

    ],
}

# Sensor configuration.
sensors = {
    'registry': {
        'hx711': {
            'pin_dout': 'P22',
            'pin_pdsck': 'P21',
            'scale': 11.424242,
            'offset': 74114.0,
        },
        'ds18x20': {
            'bus': 'onewire:0',
        },
        'bme280': {
            'bus': 'i2c:0',
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
            "family": "onewire",
            "number": 0,
            "enabled": True,
            "pin_data": "P11",
        },
    ]
}
