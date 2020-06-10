=============================
Setup on MicroPython for Unix
=============================
::

    export MICROPYPATH=`pwd`/dist-packages

    # "json" and "copy" modules
    micropython -m upip install micropython-json micropython-copy

    # HTTP client modules
    micropython -m upip install micropython-http.client micropython-io micropython-time

    # MQTT client modules
    micropython -m upip install micropython-umqtt.robust micropython-umqtt.simple


    # Use "http.client" for unencrypted HTTP connections
    # micropython -m upip install micropython-http.client micropython-io micropython-time
    #from http.client import HTTPConnection
    #self.connection = HTTPConnection(self.netloc)

    # TODO: Make HTTPS work
    #from http.client import HTTPSConnection
    ##self.connection = HTTPSConnection(self.netloc)
