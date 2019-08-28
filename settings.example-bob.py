"""Datalogger configuration"""

# General settings.
main = {

    # Measurement intervals in seconds.
    # Todo: Please note this is not the _real thing_ yet at it will just use
    #       this value to apply to ``time.sleep()`` after each duty cycle.
    'interval': {

        # Apply this interval if device is in field mode.
        'field': 60.0,

        # Apply this interval if device is in maintenance mode.
        # https://community.hiveeyes.org/t/wartungsmodus-fur-den-terkin-datenlogger/2274
        'maintenance': 15.0,
    },

    # Whether to use deep sleep between measurement cycles.
    'deepsleep': False,

    # Configure logging.
    'logging': {

        # Enable or disable logging completely.
        'enabled': True,

        # Log configuration settings at system startup.
        'configuration': True,
    },

    # Configure Watchdog.
    'watchdog': {

        # Enable or disable Watchdog completely.
        'enabled': False,

        # Watchdog timeout in milliseconds.
        'timeout': 60000,
    },

    # Configure backup.
    'backup': {
        # How many backup files to keep around.
        'file_count': 7,
    },

    # Whether to skip LTE modem deinit on startup. This will save ~6 seconds.
    'fastboot': False,

    # Configure RGB-LED.
    'rgb_led': {

        # Use the builtin heartbeat blink pattern. Default: True.
        'heartbeat': True,

        # Activate the Terkin blink pattern. Will disable the builtin heartbeat pattern when enabled.
        'terkin': False,
    },

}

# Control the services offered by the device.
services = {
    'api': {
        'modeserver': {
            'enabled': True,
        },
        'http': {
            'enabled': True,
        },
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
            #'endpoint': 'mqtt://username:password@swarm.hiveeyes.org',
            'topology': 'mqttkit',
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

    # Whether to prettify sensor log output.
    'prettify_log': True,

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
    'environment': [
        {
            'id': 'scale-1',
            'number': 0,
            'name': 'scale',
            'description': 'Waage 1',
            'type': 'HX711',
            'enabled': True,
            'pin_dout': 'P22',
            'pin_pdsck': 'P21',
            'scale': 4.424242,
            'offset': -73000,
        },
        {
            'id': 'ds18b20-1',
            'name': 'temperature',
            'description': 'Wabengasse 1',
            'type': 'DS18B20',
            'enabled': True,
            'bus': 'onewire:0',
            'devices': [
                {
                    'id': 'ds18b20-w1r1',
                    'address': '1111111111111111',
                    'description': 'Wabengasse 1, Rahmen 1',
                    'enabled': True,
                    #'offset': 0.42,
                },
                {
                    'id': 'ds18b20-w1r2',
                    'address': '2222222222222222',
                    'description': 'Wabengasse 1, Rahmen 2',
                    'enabled': True,
                    #'offset': -0.42,
                },
            ],
        },
        {
            'id': 'bme280-1',
            'description': 'Temperatur und Feuchte außen',
            'type': 'BME280',
            'enabled': True,
            'bus': 'i2c:0',
            'address': 0x77,
        },
    ],
    'busses': [
        {
            "id": "bus-i2c-0",
            "family": "i2c",
            "number": 0,
            "enabled": True,
            "pin_sda": "P9",
            "pin_scl": "P10",
        },
        {
            "id": "bus-onewire-0",
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

    # Waage
    "weight.0": "weight_kg",

    # BME280
    "temperature.0x77.i2c:0": "t",
    "humidity.0x77.i2c:0": "h",
    "pressure.0x77.i2c:0": "p",

    # DS18B20
    "temperature.1111111111111111.onewire:0": "t_i_1",
    "temperature.2222222222222222.onewire:0": "t_i_2",
    "temperature.3333333333333333.onewire:0": "t_i_3",
    "temperature.4444444444444444.onewire:0": "t_i_4",
    "temperature.5555555555555555.onewire:0": "t_i_5",
    "temperature.6666666666666666.onewire:0": "t_o",

    # Signalstärke
    "system.wifi.rssi": "rssi",

    # Sendeleistung
    "system.wifi.max_tx_power": "snr",

    # Batteriespannung
    "system.voltage": "bv",

}
