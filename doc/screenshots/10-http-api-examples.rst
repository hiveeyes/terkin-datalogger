###########################################
Terkin HTTP API request / response examples
###########################################


**********************
Configuration settings
**********************

Get individual configuration setting
====================================
::

    http GET "http://$(cat .terkin/floatip)/api/v1/setting?name=main.testdrive"
    "Franz jagt im komplett verwahrlosten Taxi quer durch Bayern"


Set individual configuration setting
====================================
::

    $ echo '"Franz jagt im komplett verwahrlosten Taxi quer durch Bayern"' | http PUT "http://$(cat .terkin/floatip)/api/v1/setting?name=main.testdrive" --print hHbB
    PUT /api/v1/setting?name=main.testdrive HTTP/1.1
    Content-Length: 62
    Content-Type: application/json

    "Franz jagt im komplett verwahrlosten Taxi quer durch Bayern"

    HTTP/1.1 200 OK
    Connection: close
    Content-Length: 61
    Content-Type: application/json; charset=UTF-8

    "Franz jagt im komplett verwahrlosten Taxi quer durch Bayern"

Whole bunch of settings
=======================

Get runtime settings in JSON format
-----------------------------------
::

    http GET "http://$(cat .terkin/floatip)/api/v1/settings?format=json"

    HTTP/1.1 200 OK
    Content-Length: 2627
    Content-Type: application/json; charset=UTF-8

    {
        "main": {
            "deepsleep": false,
            "interval": {
                "field": 15.0,
                "maintenance": 10.0
            },
            "logging": {
                "configuration": false,
                "enabled": true
            },
            "rgb_led": {
                "heartbeat": true
            },
            "watchdog": {
                "enabled": false,
                "timeout": 10000
            }
        },

        [...]
    }

Get runtime settings in Python format
-------------------------------------
::

    http GET "http://$(cat .terkin/floatip)/api/v1/settings?format=python"

    HTTP/1.1 200 OK
    Content-Disposition: attachment; filename="settings.py"
    Content-Length: 8997
    Content-Type: application/octet-stream

    """Datalogger configuration"""

    # General settings.
    main = {

        # Measurement intervals in seconds.
        # Todo: Please note this is not the _real thing_ yet at it will just use
        #       this value to apply to ``time.sleep()`` after each duty cycle.
        'interval': {

            # Use this interval if device is in field mode.
            'field': 15.0,

            # Apply this interval if device is in maintenance mode.
            # https://community.hiveeyes.org/t/wartungsmodus-fur-den-terkin-datenlogger/2274
            'maintenance': 10.0,
        },

        [...]

    }


********
Readings
********

Get last reading
================
::

    http GET "http://$(cat .terkin/floatip)/api/v1/reading/last"

    HTTP/1.1 200 OK
    Content-Type: application/json; charset=UTF-8
    Content-Length: 610

    {
        "humidity.0x77.i2c:0": 53.38,
        "pressure.0x77.i2c:0": 1013.92,
        "scale.0.kg": 0.715,
        "scale.0.offset": 87448.65,
        "scale.0.raw": 71191.33,
        "scale.0.scale": -22742.99,
        "system.memfree": 2325744,
        "system.runtime": 1786,
        "system.temperature": 39.3913,
        "system.time": 1806,
        "system.uptime": 1806.707,
        "system.voltage": 3.822,
        "system.wifi.bandwidth": 2,
        "system.wifi.channel": 8,
        "system.wifi.country": "DE",
        "system.wifi.max_tx_power": 78,
        "system.wifi.rssi": -47,
        "temperature.0x77.i2c:0": 24.23,
        "temperature.28ff641d8fc3944f.onewire:0": 25.58,
        "temperature.28ff641d8fdf18c1.onewire:0": 28.295,
        "weight.0": 0.715
    }


***********
Peripherals
***********

Busses
======
::

    $ http GET "http://$(cat .terkin/floatip)/api/v1/peripherals/busses"

    {
        "i2c:0": {
            "adapter": "I2C(0, I2C.MASTER, baudrate=100000)",
            "devices": [
                119
            ],
            "name": "i2c:0",
            "number": 0,
            "pins": {
                "scl": "P10",
                "sda": "P9"
            },
            "settings": {
                "enabled": true,
                "family": "i2c",
                "id": "i2c:0",
                "number": 0,
                "pin_scl": "P10",
                "pin_sda": "P9"
            },
            "type": "i2c"
        },
        "onewire:0": {
            "adapter": "<OneWire object at 3f9abb30>",
            "devices": [
                "28ff641d8fdf18c1",
                "28ff641d8fc3944f"
            ],
            "name": "onewire:0",
            "number": 0,
            "pins": {
                "data": "P11"
            },
            "settings": {
                "enabled": true,
                "family": "onewire",
                "id": "onewire:0",
                "number": 0,
                "pin_data": "P11"
            },
            "type": "onewire"
        }
    }

Sensors
=======
::

    $ http GET "http://$(cat .terkin/floatip)/api/v1/peripherals/sensors"

    [
        "<SystemMemoryFree object at 3f9abc50>",
        "<SystemTemperature object at 3f9abc60>",
        "<SystemBatteryLevel object at 3f9abc70>",
        "<SystemUptime object at 3f9ac650>",
        "<SystemWiFiMetrics object at 3f9ac660>",
        {
            "address": 0,
            "bus": "None",
            "driver": null,
            "driver_class": "<class 'HX711Heisenberg'>",
            "family": null,
            "loadcell": "<HX711Heisenberg object at 3f9afb00>",
            "name": null,
            "parameter": {
                "gain": 128,
                "offset": 87448.65,
                "scale": -22742.99
            },
            "pins": {
                "dout": "P22",
                "pdsck": "P21"
            },
            "settings": {
                "description": "Waage 1",
                "enabled": true,
                "id": "scale-1",
                "name": "scale",
                "number": 0,
                "offset": 87448.65,
                "pin_dout": "P22",
                "pin_pdsck": "P21",
                "scale": -22742.99,
                "type": "HX711"
            }
        },
        {
            "address": null,
            "bus": "<OneWireBus object at 3f9aa920>",
            "driver": "<DS18X20 object at 3f9b01c0>",
            "family": null,
            "name": null,
            "parameter": {},
            "pins": {},
            "settings": {
                "bus": "onewire:0",
                "description": "Wabengasse 1",
                "devices": [
                    {
                        "address": "28ff641d8fdf18c1",
                        "description": "Wabengasse 1, Rahmen 1",
                        "enabled": true,
                        "id": "ds18b20-w1r1",
                        "offset": 0.42
                    },
                    {
                        "address": "28ff641d8fc3944f",
                        "description": "Wabengasse 1, Rahmen 2",
                        "enabled": true,
                        "id": "ds18b20-w1r2",
                        "offset": -0.42
                    }
                ],
                "enabled": true,
                "id": "ds18b20-1",
                "name": "temperature",
                "type": "DS18B20"
            }
        },
        {
            "address": 119,
            "bus": "<I2CBus object at 3f9aa430>",
            "driver": "<BME280 object at 3f9b1ab0>",
            "family": null,
            "name": null,
            "parameter": {},
            "pins": {},
            "settings": {
                "address": 119,
                "bus": "i2c:0",
                "description": "Temperatur und Feuchte außen",
                "enabled": true,
                "id": "bme280-1",
                "type": "BME280"
            }
        }
    ]


DS18B20 Sensors
===============
::

    http GET "http://$(cat .terkin/floatip)/api/v1/sensors/ds18b20"

    [
        {
            "address": "28ff641d8fdf18c1",
            "bus": "onewire:0",
            "description": "Wabengasse 1, Rahmen 1",
            "pin": "P11"
        },
        {
            "address": "28ff641d8fc3944f",
            "bus": "onewire:0",
            "description": "Wabengasse 1, Rahmen 2",
            "pin": "P11"
        }
    ]


**************
Demo endpoints
**************

Echo service » Form
===================
::

    http --form "http://espressif/echo/def?foo=bar" baz=qux

::

    HTTP/1.1 200 OK
    Access-Control-Allow-Origin: *
    Connection: close
    Content-Length: 147
    Content-Type: application/json; charset=UTF-8
    Server: MicroWebSrv by JC`zic

    {
        "content_type": "application/x-www-form-urlencoded; charset=utf-8",
        "data": {
            "baz": "qux"
        },
        "path": {
            "slot": "def"
        },
        "query": {
            "foo": "bar"
        }
    }


Echo service » JSON
===================
::

    http --json "http://espressif/echo/def?foo=bar" baz=qux

::

    {
        "content_type": "application/json",
        "data": {
            "baz": "qux"
        },
        "path": {
            "slot": "def"
        },
        "query": {
            "foo": "bar"
        }
    }

