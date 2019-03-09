########################################
Hiveeyes MPY data logger troubleshooting
########################################

We've jumped through some tires that you don't have to.

.. _upgrade your firmware: https://github.com/hiveeyes/hiveeyes-micropython-firmware/blob/master/doc/pycom-firmware-upgrade.rst


************
Introduction
************
You should always run the latest firmware on your device.
There are many chances the upstream developers fixed some
of issues you are running into for quite some time already.

So, please `upgrade your firmware`_ before trying
to debug weird errors on your own behalf.

Example references:

- https://github.com/pycom/pycom-micropython-sigfox/issues/260
- https://github.com/pycom/pycom-micropython-sigfox/issues/265
- https://github.com/pycom/pycom-micropython-sigfox/issues/266


************************
1. Not connected to WiFi
************************
::

    Traceback (most recent call last):
      File "main.py", line 32, in <module>
      File "/flash/lib/telemetry.py", line 209, in transmit
      File "/flash/lib/telemetry.py", line 87, in transmit
      File "/flash/lib/telemetry.py", line 151, in __init__
      File "/flash/lib/mqtt.py", line 19, in __init__
    OSError: Avialable Interfaces are down

There's a typo in this error message. Please `upgrade your firmware`_.


*************************
2. Strange "no nic" error
*************************
https://github.com/pycom/pycom-micropython-sigfox/issues/196

::

    Traceback (most recent call last):
      File "main.py", line 32, in <module>
      File "/flash/lib/telemetry.py", line 209, in transmit
      File "/flash/lib/telemetry.py", line 87, in transmit
      File "/flash/lib/telemetry.py", line 151, in __init__
      File "/flash/lib/mqtt.py", line 19, in __init__
    OSError: no available NIC

This is unacceptable. Please `upgrade your firmware`_.


********************************
3. While trying to build the SDK
********************************

mpy-cross woes
==============
::

    make: *** No rule to make target `build/FIPY/release/frozen_mpy/frozen/Base/_main.mpy', needed by `build/FIPY/release/frozen_mpy.c'.  Stop.
    - https://github.com/pycom/pycom-micropython-sigfox/issues/214
    - https://github.com/pycom/pycom-micropython-sigfox/issues/220

    Solution: https://github.com/pycom/pycom-micropython-sigfox/issues/220#issuecomment-431536064
    ::

        cd pycom-micropython-sigfox
        patch py/mkrules.mk < mkrules.patch

Not! Go away.

ImportError: No module named serial
===================================
::

    python /Users/amo/dev/hiveeyes/tools/pycom/pycom-esp-idf/components/esptool_py/esptool/esptool.py --chip esp32 elf2image --flash_mode dio --flash_freq 80m -o build/FIPY/release/bootloader/bootloader.bin build/FIPY/release/bootloader/bootloader.elf
    Pyserial is not installed for /usr/local/opt/python@2/bin/python2.7. Check the README for installation instructions.
    Traceback (most recent call last):
      File "/Users/amo/dev/hiveeyes/tools/pycom/pycom-esp-idf/components/esptool_py/esptool/esptool.py", line 37, in <module>
        import serial
    ImportError: No module named serial
    make: *** [build/FIPY/release/bootloader/bo

Use Python virtualenv appropriately (ask @amotl) and then let's go shopping.


******************
4. No connectivity
******************
::

    Starting TerkinTelemetry
    Import MQTT client library
    Channel URI:  mqtt://swarm.hiveeyes.org/hiveeyes/testdrive/area-23/node-1
    mqtt connect: swarm.hiveeyes.org 1883
    Traceback (most recent call last):
      File "main.py", line 56, in <module>
      File "/flash/lib/telemetry.py", line 211, in transmit
      File "/flash/lib/telemetry.py", line 89, in transmit
      File "/flash/lib/telemetry.py", line 155, in __init__
      File "/flash/lib/mqtt.py", line 60, in connect
    OSError: Network card not available

Don't forget to use ``station.init()``.


************************************
5. FiPy errors out after a few loops
************************************
Both ``OSError: 23`` and ``OSError: -202`` seem to be popular exceptions
raised by programming errors regarding object lifecycle or when overloading
the networking stack. The errors have been on us, so no worries here.

We just included these in this list for others when running into similar
problems. Please ask @amotl about more details.

::

    [17.20302] Terkin mainloop
    MQTT Topic:   hiveeyes/testdrive/irgendwas/baz/data.json
    Payload:      {"humidity": 83, "temperature": 42.84}
    Telemetry success: True

    [18.33101] Terkin mainloop
    Traceback (most recent call last):
      File "main.py", line 28, in <module>
      File "main.py", line 24, in main
      File "/flash/lib/terkin/datalogger.py", line 33, in start
      File "/flash/lib/terkin/datalogger.py", line 48, in _mainloop
      File "/flash/lib/terkin/datalogger.py", line 57, in loop
      File "/flash/lib/terkin/telemetry.py", line 215, in transmit
      File "/flash/lib/terkin/telemetry.py", line 84, in transmit
      File "/flash/lib/terkin/telemetry.py", line 159, in __init__
      File "/flash/lib/mqtt.py", line 58, in connect
    OSError: 23

::

    [5.704215] Terkin mainloop
    TelemetryTransportMQTT
    Traceback (most recent call last):
      File "main.py", line 28, in <module>
      File "main.py", line 24, in main
      File "/flash/lib/terkin/datalogger.py", line 35, in start
      File "/flash/lib/terkin/datalogger.py", line 50, in _mainloop
      File "main.py", line 18, in loop
      File "/flash/lib/terkin/datalogger.py", line 59, in loop
      File "/flash/lib/terkin/telemetry.py", line 230, in transmit
      File "/flash/lib/terkin/telemetry.py", line 82, in transmit
      File "/flash/lib/terkin/telemetry.py", line 103, in get_handler
      File "/flash/lib/terkin/telemetry.py", line 172, in __init__
      File "/flash/lib/mqtt.py", line 19, in __init__
    OSError: -202


***************************************
6. ``pcre.func`` missing on MicroPython
***************************************

Problem
=======
::

    Traceback (most recent call last):
      File "main.py", line 37, in <module>
      File "main.py", line 33, in main
      File "/flash/lib/terkin/datalogger.py", line 29, in start
      File "/flash/lib/terkin/device.py", line 51, in start_telemetry
      File "/flash/lib/terkin/telemetry.py", line 18, in <module>
      File "dist-packages/urllib/parse.py", line 30, in <module>
      File "dist-packages/re.py", line 11, in <module>
    AttributeError: 'NoneType' object has no attribute 'func'

The ``ure`` module implements a subset of the corresponding CPython module,
as described below. For more information, please refer to the original
CPython ``re`` module documentation.

- http://docs.micropython.org/en/v1.9.3/pyboard/library/ure.html
- https://docs.python.org/3/library/re.html#module-re

Investigation
=============
``pcre.func`` is actually the first thing used after importing ``libpcre``::

    pcre = ffilib.open("libpcre")

    #       pcre *pcre_compile(const char *pattern, int options,
    #            const char **errptr, int *erroffset,
    #            const unsigned char *tableptr);
    pcre_compile = pcre.func("p", "pcre_compile", "sipps")

-- https://github.com/micropython/micropython-lib/blob/v1.9.3/re-pcre/re.py#L6-L11

See also:
- https://github.com/micropython/micropython-lib/issues/25

Conclusion
==========
After asking Pycom about this [1], we will put it aside and come back to it later.
It is currently only required to run a multi-protocol ``TerkinTelemetry`` client
capable of speaking **both** MQTT and HTTP. The current version included here
will only talk MQTT, which is fine for us right now.

However, we **are** aiming to run all of the functionality of `micropython-terkin`_,
so we will probably have to use one of the two ``urllib`` modules **not based on**
``micropython-re-pcre``, either `micropython-urllib.urequest`_ or `micropython-urllib`_.

.. _micropython-terkin: https://github.com/daq-tools/terkin/tree/master/src/micropython
.. _micropython-urllib.urequest: https://github.com/micropython/micropython-lib/tree/master/urllib.urequest
.. _micropython-urllib: https://github.com/micropython/micropython-lib/tree/master/urllib

[1] https://forum.pycom.io/topic/4494/libpcre-missing


*****************************
7. HX711 library not starting
*****************************
Q::

    Traceback (most recent call last):
      File "main.py", line 72, in <module>
      File "main.py", line 67, in main
      File "/flash/lib/terkin/datalogger.py", line 34, in start
      File "main.py", line 34, in register_sensors
      File "main.py", line 55, in __init__
      File "/flash/lib/hx711.py", line 12, in __init__
    ValueError: invalid argument(s) value

A::

    # v1: Does not work on the Pycom, will need strings as pin identifiers.
    #self.loadcell = self.driver(0, 2)

    # v2: Works with Pycom MicroPython.
    # https://docs.pycom.io/firmwareapi/pycom/machine/pin.html
    # https://docs.pycom.io/firmwareapi/pycom/machine/pin.html#attributes
    #self.loadcell = self.driver('P0', 'P2')


***********************************
8. HX711 library freezes the device
***********************************
Q: The device freezes when trying to initialize the HX711 driver::

    [12.22129] Registering Hiveeyes sensors
    [12.22535] Registering BOB sensors
    INFO: Initializing HX711 sensor with DOUT=P0, PD_SCK=P2, GAIN=None, scale=11.02667, offset=130800.0
    INFO: Selected HX711 hardware driver "heisenberg"

A: The HX711 library should be improved.
   See also https://github.com/bogde/HX711/pull/123 and https://github.com/bogde/HX711/issues/125.


******************************
9. HX711 library yields errors
******************************
1. Q: ``Reading sensor "HX711Sensor" failed: 'NoneType' object has no attribute 'read_median'``
   A: Ensure you have select the "heisenberg" hardware driver.


*********************
10. Memory corruption
*********************
Do you get a weird syntax error while your sources are perfectly okay?
You should just power-cycle your controller, it's probably memory corruption only.
::

    [10.5782] Registering Hiveeyes sensors
    [10.58196] Registering BOB sensors
    INFO: Initializing HX711 sensor with DOUT=P0, PD_SCK=P2, GAIN=None, scale=11.02667, offset=130800.0
    Traceback (most recent call last):
      File "main.py", line 79, in <module>
      File "main.py", line 74, in main
      File "/flash/lib/terkin/datalogger.py", line 36, in start
      File "main.py", line 34, in register_sensors
      File "main.py", line 51, in register_hx711
      File "/flash/lib/hiveeyes/sensor_hx711.py", line 43, in select_driver
      File "/flash/lib/hx711_heisenberg.py", line 87
    SyntaxError: invalid syntax


USSL not found
==============

::

    make setup         
    .venv3/bin/pip --quiet install --requirement requirements-dev.txt
    INFO: Please install MicroPython for Unix
    micropython -m upip install -p dist-packages -r requirements-mpy.txt
    Traceback (most recent call last):
      File "upip.py", line 109, in <module>
    ImportError: no module named 'ussl'
    make: *** [Makefile:17: install-requirements] Fehler 1

