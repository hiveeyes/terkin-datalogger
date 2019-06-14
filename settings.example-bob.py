"""Datalogger configuration"""

# General settings.
main = {

    # Measurement interval in seconds.
    # TODO: Please note this is not the _real thing_ yet at it will just use
    #       this value to apply to ``time.sleep()`` after each duty cycle.
    'interval': 5.0,

    # Whether to use deep sleep between measurement cycles.
    'deepsleep': True,

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

        # Hiveeyes telemetry: JSON over MQTT
        {
            # Enable/disable this telemetry target.
            'enabled': False,

            # Define telemetry endpoint and address information.
            'endpoint': 'mqtt://swarm.hiveeyes.org',
            'address': {
                "realm": "hiveeyes",
                "network": "testdrive",
                "gateway": "area-42",
                "node": "node-99",
            },
        },

        # Beep telemetry: JSON over HTTP
        {
            # Enable/disable this telemetry target.
            'enabled': False,

            # Define telemetry endpoint and address information.
            'endpoint': 'https://bee-observer.org/api/sensors',
            'topology': 'beep-bob',
            'data': {
                'key': '## BEEP_SENSOR_KEY ##',
            },
        },

    ],
}

# Sensor configuration.
sensors = {
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

# Map sensor field names to telemetry field names.
# Right now, please adapt this according to your sensor configuration by
# looking at the console output of the line
# `[terkin.datalogger] INFO: Sensor data`. Thanks!
#
# Remark:
# This will be replaced by runtime configuration through
# HTTP API and captive portal.
sensor_telemetry_map = {
    "_version": "1.0.0",
    "temperature.0x77.i2c:0": "t",
    "humidity.0x77.i2c:0": "h",
    "pressure.0x77.i2c:0": "p",
    "weight.0": "weight",
    "temperature.28ff641d8fdf18c1.onewire:0": "t_i_1",
    "temperature.28ff641d8fc3944f.onewire:0": "t_i_2",
    "system.temperature": "t_i_5",
}
