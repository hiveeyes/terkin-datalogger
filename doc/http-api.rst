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


******************
Settings endpoints
******************

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
Retrieve dynamic runtime settings in JSON format::

    GET /api/v1/settings?format=json

Settings Python
===============
Retrieve global static ``settings.py`` in Python format::

    GET /api/v1/settings?format=python


*********************
Peripherals endpoints
*********************

Request information about busses::

    GET /api/v1/peripherals/busses

Request information about sensors::

    GET /api/v1/peripherals/sensors

Request information about DS18B20 sensors::

    GET /api/v1/sensors/ds18b20


**************
Data endpoints
**************

Get last reading
================
Request::

    GET /api/v1/reading/last


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
