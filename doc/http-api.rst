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
::

    http "http://espressif/status"
    OK

About
=====
::

    http "http://espressif/about"

::

    HTTP/1.1 200 OK
    Access-Control-Allow-Origin: *
    Application-Name: Bee Observer Datalogger
    Application-Version: 0.5.1
    Connection: close
    Content-Length: 29
    Content-Type: text/plain; charset=utf-8
    Server: MicroWebSrv by JC`zic

    Bee Observer Datalogger 0.5.1

Restart
=======
::

    http POST "http://espressif/restart"


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
