"""Datalogger configuration"""

# General settings.
main = {

    # Measurement intervals in seconds.
    'interval': {

        # Apply this interval if device is in field mode.
        'field': 40.0,

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
        'configuration': False,
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
            'enabled': False,
        },
        'http': {
            'enabled': False,
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

        # Enable/disable WiFi completely.
        'enabled': False,

        # WiFi interface configuration.
        'phy': {
            'antenna_external': False,
            'antenna_pin': 'P12',
        },

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

    # LoRaWAN/TTN
    'lora': {
        'enabled': True,
        'antenna_attached': True,
        'region': 'EU868',
        'adr': False,

        # Over-the-Air Activation (OTAA) vs. Activation by Personalization (ABP)
        # https://www.thethingsnetwork.org/forum/t/what-is-the-difference-between-otaa-and-abp-devices/2723
        'activation': 'otaa',   # abp
        'otaa': {
            'device_eui': '<GENERATED_FROM_LORA_MAC_OR_TTN>',
            'application_eui': '<REGISTRATION NEEDED>',
            'application_key': '<REGISTRATION NEEDED>',
        },
        'abp': {
            'device_address': '<FROM TTN CONSOLE>',
            'network_session_key': '<FROM TTN CONSOLE>',
            'app_session_key': '<FROM TTN CONSOLE>',
        },
    },

    # GPRS/SIM800
    # https://github.com/hiveeyes/pythings-sim800
    'gprs': {

        # General settings.
        'enabled': False,
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

        # JSON over MQTT: Kotori/MQTTKit
        {
            # Enable/disable this telemetry target.
            'enabled': True,

            # Define telemetry endpoint and address information.
            'endpoint': 'mqtt://127.0.0.1',
            #'endpoint': 'mqtt://username:password@daq.example.org',
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

        # JSON over HTTP over GPRS: Kotori/MQTTKit
        {
            # Enable/disable this telemetry target.
            'enabled': False,

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
            'content_encoding': 'base64',
        },

        # CayenneLPP over LoRaWAN/TTN
        {
            # Enable/disable this telemetry target.
            'enabled': True,

            'endpoint': 'lora://',
            'format': 'lpp-ratrack',
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
            'enabled': False,
        },
        {
            # Sensor which reports system temperature.
            'type': 'system.temperature',
            'enabled': False,
        },
        {
            # Sensor which reports system uptime metrics.
            'type': 'system.uptime',
            'enabled': False,
        },
        {
            # Sensor which reports system WiFi metrics.
            'type': 'system.wifi',
            'enabled': False,
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

            # The sensor description.
            'description': 'Battery',

            # Enable/disable sensor.
            'enabled': False,

            # On which Pin to schnuckle this.
            'pin': 'P16',

            # Main resistor value (R1).
            'resistor_r1': 1000,

            # Resistor between input pin and ground (R2).
            'resistor_r2': 1000,

            # ADC attenuation. Possible values are 0.0, 2.5, 6.0 or 11.0.
            'adc_attenuation_db': 6.0,
        },

        {
            # Sensor which reports solar panel voltage.
            # See description in system.battery-voltage sensor

            # The sensor type identifier.
            'type': 'system.voltage.solar',

            # The sensor description.
            'description': 'Solar Panel',

            # Enable/disable sensor.
            'enabled': False,

            # On which Pin to schnuckle this.
            'pin': 'P17',

            # Main resistor value (R1).
            'resistor_r1': 1000,

            # Resistor between input pin and ground (R2).
            'resistor_r2': 100,

            # ADC attenuation. possbible values: 0.0, 2.5, 6.0 or 11.0
            'adc_attenuation_db': 11.0,
        },

    ],

    'environment': [
        {
            'id': 'scale-1',
            'number': 0,
            'name': 'scale',
            'description': 'Waage 1',
            'type': 'HX711',
            'enabled': False,
            'pin_dout': 'P22',
            'pin_pdsck': 'P21',
            'scale': 4.424242,
            'offset': -73000,
            'decimals': 3,
        },
        {
            'id': 'ds18b20-1',
            'name': 'temperature',
            'description': '',
            'type': 'DS18B20',
            'enabled': True,
            'bus': 'onewire:0',
            'devices': [
                {
                    'id': 'ds18b20-r1c1',
                    'address': '0517c482cfff',
                    'description': 'DS18B20:0517c482cfff on onewire:0',
                    'enabled': True,
                    #'offset': 0.42,

                    'telemetry_name': 'inside.temperature.frame_1',
                    'realm': 'inside',
                    'type': 'temperature',
                    'name': 'frame_1',
                },
                {
                    'id': 'ds18b20-r1c2',
                    'address': '2222222222222222',
                    'description': 'DS18B20:2222222222222222 on onewire:0',
                    'enabled': False,
                    #'offset': -0.42,

                    'telemetry_name': 'inside.temperature.frame_2',
                    'realm': 'inside',
                    'type': 'temperature',
                    'name': 'frame_2',
                },
            ],
        },
        {
            'id': 'bme280-1',
            'description': 'Bme280 on ic2:1 0x76',
            'type': 'BME280',
            'enabled': True,
            'bus': 'i2c:1',
            'address': 0x76,
        },
        {
            'id': 'bme280-2',
            'description': 'Bme280 on ic2:3 0x76',
            'type': 'BME280',
            'enabled': True,
            'bus': 'i2c:3',
            'address': 0x76,
        },
        {
            'id': 'bmp280-1',
            'description': 'BMP280 on ic2:1 0x77',
            'type': 'BMP280',
            'enabled': False,
            'bus': 'i2c:1',
            'address': 0x77,
        },
        {
            'id': 'ads1x15-1',
            'description': 'ads1115 P0',
            'type': 'ads1x15',
            'enabled': True,
            'bus': 'i2c:1',
            'model': 'ads1115',
            'multiplicator': 22.37,
            'channel': 'P0',
            'address': 0x48,
        },
        {
            'id': 'ads1x15-1',
            'description': 'ads1115 P1',
            'type': 'ads1x15',
            'enabled': True,
            'bus': 'i2c:1',
            'model': 'ads1115',
            'multiplicator': 22.37,
            'channel': 'P1',
            'address': 0x48,
        },
        {
            'id': 'epsolar-1',
            'description': 'EPSolar VS1024N Charge Controller',
            'type': 'epsolar',
            'enabled': True,
            # 'bus': 'serial:0',
            'device': '/dev/ttyUSB1',
        },
        {
            'id': 'vedirect-1',
            'description': 'Victron Energy SmartSolar Charge Controller MPPT 75|15',
            'type': 'vedirect',
            'enabled': False,
            # 'bus': 'serial:0',
            'device': '/dev/ttyUSB0',
        },
        {
            'id': 'gpsd-1',
            'description': 'Gpsd Daemon',
            'type': 'gpsd',
            'enabled': True,
        },
        {
            'id': 'gpiozero',
            'description': 'gpiozero',
            'type': 'gpiozero',
            'enabled': True,
        },
        {
            'id': 'ina219-1',
            'description': 'INA219 on ic2:1 0x40',
            'type': 'INA219',
            'enabled': False,
            'bus': 'i2c:1',
            'address': 0x40,
        },
        {
            'id': 'ina219-2',
            'description': 'INA219 on ic2:1 0x44',
            'type': 'INA219',
            'enabled': False,
            'bus': 'i2c:1',
            'address': 0x44,
        },
        {
            'id': 'max17043-1',
            'description': 'Akkuspannung und -prozent (MAX17043)',
            'type': 'MAX17043',
            'enabled': False,
            'bus': 'i2c:0',
            'address': 0x36,
        },                
    ],
    'buses': [
        {
            "id": "bus-i2c-1",
            "family": "i2c",
            "number": 1,
            "enabled": True,
            "pin_sda": 'board.SDA',
            "pin_scl": 'board.SCL',
        },

        # Register more I2C buses with Adafruit Blinka.
        #
        # Make Adafruit Blinka learn another I2C bus.
        # Please make sure you define it within /boot/config.txt like::
        #
        # dtoverlay=i2c-gpio,bus=5,i2c_gpio_delay_us=1,i2c_gpio_sda=26,i2c_gpio_scl=20
        {
            "id": "bus-i2c-5",
            "family": "i2c",
            "number": 5,
            "enabled": True,
            "pin_sda": 37,
            "pin_scl": 38,
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

