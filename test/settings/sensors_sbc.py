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
    ],

    'environment': [
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
            "pin_sda": "board.SDA",
            "pin_scl": "board.SCL",
        },
        {
            "id": "bus-onewire-0",
            "family": "onewire",
            "number": 0,
            "enabled": True,
            "driver": "sysfs",
            "sysfs": "/sys/bus/w1/devices/w1_bus_master1/",
        },
    ]
}
