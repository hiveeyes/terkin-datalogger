###############
Terkin HTTP API
###############


*****
About
*****
The Terkin HTTP API provides a HTTP-based interface to
parts of the datalogger machinery.

It can be used to

- inquire important system information
- read sensor observations
- manage the device


*************
Configuration
*************
The HTTP API can be enabled by using this in``settings.py``::

    # General settings.
    main = {

        # Control the service APIs offered by the device.
        'api': {
            'http': {
                'enabled': True,
            }
        }

    }


****************
System endpoints
****************

Status/alive
============
Request::

    GET /status

Response::

    HTTP/1.1 200 OK
    Application-Name: Bee Observer Datalogger
    Application-Version: 0.5.1
    Content-Type: text/plain; charset=utf-8

    OK

About
=====
Request::

    GET /about

Response::

    HTTP/1.1 200 OK
    Content-Type: text/plain; charset=utf-8

    Bee Observer Datalogger 0.5.1

Restart
=======
::

    POST /restart



*********************
Application endpoints
*********************


Get single setting
==================
Request::

    GET /api/v1/setting?name=<name>

Set single setting
==================
Request::

    PUT /api/v1/setting?name=<name>
    Content-Type: application/json

Settings JSON
=============
Retrieve runtime settings in JSON format.

Request::

    GET /api/v1/settings

Response::

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


Settings Python
===============
Retrieve global static ``settings.py`` in Python format.

Request::

    GET /api/v1/settings?format=python


Response::

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


**************
Basic examples
**************
::

    # Get measurement interval
    http GET "http://$(cat .terkin/floatip)/api/v1/setting?name=main.interval.field"
    15.0

    # Get sensor configuration
    http GET "http://$(cat .terkin/floatip)/api/v1/setting?name=sensors"

    # Set measurement interval
    echo 42.42 | http PUT "http://$(cat .terkin/floatip)/api/v1/setting?name=main.interval.field"


Upload ``settings.py``::

    cat settings.py | http PUT "http://$(cat .terkin/floatip)/api/v1/settings" Content-Type:text/plain

Upload ``settings.json``::

    cat settings.json | http PUT "http://$(cat .terkin/floatip)/api/v1/settings" Content-Type:application/json


*************************
Request/response examples
*************************
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
