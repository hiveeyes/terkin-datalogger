"""Datalogger configuration"""

# General settings.
main = {

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
        {
            # Settings for button events, e.g. through ESP32 touch pads.
            'type': 'system.touch-buttons',

            # Enable/disable sensor.
            'enabled': False,
        },

        {
            # Sensor which reports battery voltage.

            # Adjust voltage divider resistor values matching the board.
            #
            # See also
            # - https://forum.pycom.io/topic/3776/adc-use-to-measure-battery-level-vin-level
            # - https://github.com/hiveeyes/terkin-datalogger/issues/5
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

            # The sensor type identifier.
            'type': 'system.voltage.battery',

            # Enable/disable sensor.
            'enabled': True,

            # On which Pin to schnuckle this.
            'pin': 'P16',

            # Main resistor value (R1).
            'resistor_r1': 1000,

            # Resistor between input pin and ground (R2).
            'resistor_r2': 1000,

        },

    ],

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
            'scale': -22742.99,
            'offset': 87448.66,
        },
        {
            'id': 'ds18b20-1',
            'name': 'temperature',
            'type': 'DS18B20',
            'enabled': True,
            'bus': 'onewire:0',
            'devices': [
                {
                    'enabled': True,
                    'id': 'ds18b20-w1r1',
                    'address': '28FF641D8FDF18C1',
                    'telemetry_name': 'inside.temperature.brood_1',
                    'realm': 'inside',
                    'type': 'temperature',
                    'name': 'brood_1',
                    #'offset': 0.42,
                },
                {
                    'id': 'ds18b20-w1r2',
                    'address': '28ff641d8fc3944f',
                    'enabled': True,
                    #'offset': -0.42,
                },
            ],
        },
        {
            'id': 'bme280-1',
            'description': 'Temperatur und Feuchte',
            'type': 'BME280',
            'enabled': True,
            'bus': 'i2c:0',
            'address': 0x77,
        }
    ],
    'buses': [
        {
            "id": "i2c:0",
            "family": "i2c",
            "number": 0,
            "enabled": True,
            "pin_sda": "P9",
            "pin_scl": "P10",
        },
        {
            "id": "onewire:0",
            "family": "onewire",
            "number": 0,
            "enabled": True,
            "pin_data": "P11",
            "driver": "native",
        },
    ]
}
