#################################
Terkin Datalogger troubleshooting
#################################

We've jumped through some tires that you don't have to.

.. _upgrade your firmware: https://github.com/hiveeyes/terkin-datalogger/blob/master/doc/pycom-firmware-upgrade.rst

When experiencing problems, please also visit
https://docs.pycom.io/gettingstarted/troubleshooting-guide.html.

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


Connection to MQTT broker failed
================================
::

    --- loop ---
    [6.029771] BOB loop
    [6.032591] Terkin loop
    INFO:  Reading sensor "MemoryFree"
    Telemetry transport: MQTT over TCP over WiFi
    INFO: Connecting to MQTT broker
    ERROR: Connecting to MQTT broker failed. [Errno 113] ECONNABORTED


Connection to MQTT broker lost
==============================
::

    --- loop ---
    [136.7459] BOB loop
    [136.7558] Terkin loop
    INFO:  Reading sensor "MemoryFree"
    MQTT topic:   hiveeyes/testdrive/area-23/fipy-one/data.json
    MQTT payload: {"memfree": 2459616}
    Traceback (most recent call last):
      File "main.py", line 97, in <module>
      File "main.py", line 92, in main
      File "/flash/lib/terkin/datalogger.py", line 42, in start
      File "/flash/lib/terkin/datalogger.py", line 73, in start_mainloop
      File "main.py", line 86, in loop
      File "/flash/lib/terkin/datalogger.py", line 102, in loop
      File "/flash/lib/terkin/telemetry.py", line 298, in transmit
      File "/flash/lib/terkin/telemetry.py", line 97, in transmit
      File "/flash/lib/terkin/telemetry.py", line 238, in send
      File "/flash/lib/mqtt.py", line 114, in publish
      File "/flash/lib/mqtt.py", line 34, in _send_str
    OSError: [Errno 113] ECONNABORTED


MQTT connection establishment fails again
==========================================
Variant A::

    ERROR: Connecting to MQTT broker failed. -202

Variant B::

    ERROR: MQTT publishing failed. [Errno -1] ERR_MEM


Windows console crasher bug
===========================
When running on the Linux subsystem for Windows, outputting binary data on the console might crash it
and render the runtime environment defunct, so you will have to power-cycle the ESP32.

It might look like this::

    Exception in thread: REPL_serial_to_stdout

Solution: Just don't output binary characters over the Serial interface,
which is usually implicitly done by just running ``print()``.


Connecting to board fails I
===========================
Problem
-------
::

      File "/Users/amo/dev/hiveeyes/sources/hiveeyes-micropython-firmware/.venv3/lib/python3.7/site-packages/rshell/main.py", line 1249, in connect
        ip_address = socket.gethostbyname(port)
    socket.gaierror: [Errno 8] nodename nor servname provided, or not known

    During handling of the above exception, another exception occurred:

    Traceback (most recent call last):
      File ".venv3/bin/rshell", line 10, in <module>
        sys.exit(main())
      File "/Users/amo/dev/hiveeyes/sources/hiveeyes-micropython-firmware/.venv3/lib/python3.7/site-packages/rshell/command_line.py", line 4, in main
        rshell.main.main()

    [...]

      File "/Users/amo/dev/hiveeyes/sources/hiveeyes-micropython-firmware/.venv3/lib/python3.7/site-packages/rshell/main.py", line 1453, in remote_eval
        return eval(self.remote(func, *args, **kwargs))
      File "<string>", line 0

        ^
    SyntaxError: unexpected EOF while parsing
    make: *** [rshell] Error 1

Root cause
----------
I caused this by syncing an invalid ``os.__init__.py`` to device.


Solution
--------
Start device in safe boot to skip execution of ``boot.py`` and ``main.py``,
see also https://docs.pycom.io/gettingstarted/programming/safeboot.html

::

    make rshell
    rm -r /flash/dist-packages/os

::

    make reset


"logging" package missing
=========================
::

    Traceback (most recent call last):
      File "main.py", line 11, in <module>
      File "/flash/lib/ratrack/datalogger.py", line 10, in <module>
      File "/flash/lib/terkin/logging.py", line 5, in <module>
    ImportError: no module named 'logging'

Solution
--------
::

    make setup

ImportError: no module named 'urllib.parse'
===========================================


Problem
-------
::

    Traceback (most recent call last):
      File "main.py", line 45, in <module>
      File "main.py", line 40, in main
      File "/flash/lib/terkin/datalogger.py", line 41, in start
      File "/flash/lib/terkin/device.py", line 101, in start_telemetry
      File "/flash/lib/terkin/telemetry.py", line 25, in <module>
    ImportError: no module named 'urllib.parse'


Solution
--------
Uploading the ``dist-packages`` folder probably failed.
::

    make upload-requirements


Missing _onewire package
========================
::

    Traceback (most recent call last):
      File "main.py", line 14, in <module>
      File "/flash/lib/hiveeyes/datalogger.py", line 13, in <module>
      File "/flash/lib/terkin/datalogger.py", line 11, in <module>
      File "/flash/lib/terkin/sensor.py", line 6, in <module>
      File "dist-packages/onewire/onewire.py", line 5, in <module>
    ImportError: no module named '_onewire'
    Pycom MicroPython 1.18.1.r10 [v1.8.6-849-d53c7f3] on 2019-01-10; FiPy with ESP32


Error on lora_send
==================
::

    Traceback (most recent call last):
      File "main.py", line 22, in <module>
      File "main.py", line 17, in main
      File "/flash/lib/terkin/datalogger.py", line 58, in start
      File "/flash/lib/terkin/datalogger.py", line 115, in start_mainloop
      File "/flash/lib/ratrack/datalogger.py", line 181, in loop
      File "/flash/lib/ratrack/datalogger.py", line 194, in lorapayload
      File "/flash/lib/terkin/radio.py", line 265, in lora_send
    OSError: [Errno 11] EAGAIN


rshell error
============
Issue when running things like ``rshell cat settings.py``::

    Traceback (most recent call last):
      File ".venv3/bin/rshell", line 10, in <module>
        sys.exit(main())
      File "/Users/amo/dev/hiveeyes/sources/hiveeyes-micropython-firmware/.venv3/lib/python3.7/site-packages/rshell/main.py", line 652, in cp
        filesize, xfer_func=recv_file_from_remote)
      File "/Users/amo/dev/hiveeyes/sources/hiveeyes-micropython-firmware/.venv3/lib/python3.7/site-packages/rshell/main.py", line 1435, in remote
        xfer_func(self, *args, **kwargs)
      File "/Users/amo/dev/hiveeyes/sources/hiveeyes-micropython-firmware/.venv3/lib/python3.7/site-packages/rshell/main.py", line 1050, in recv_file_from_remote
        dst_file.write(binascii.unhexlify(write_buf[0:read_size]))
    binascii.Error: Non-hexadecimal digit found
    make: *** [rshell] Error 1


Connecting to MQTT broker fails
===============================
::

    28.3149 [terkin.telemetry         ] ERROR  : Connecting to MQTT broker at swarm.hiveeyes.org failed
    Traceback (most recent call last):
      File "/flash/lib/terkin/telemetry.py", line 417, in connect
      File "dist-packages/mqtt.py", line 16, in __init__
    OSError: [Errno 202] EAI_FAIL

::

    Traceback (most recent call last):
      File "/flash/lib/terkin/telemetry.py", line 421, in connect
      File "dist-packages/mqtt.py", line 85, in connect
    IndexError: bytes index out of range

~~Issue could be resolved by bouncing the WiFi router.~~

FiPy might be broken.


Publishing to MQTT fails
========================
::

      531.1269 [terkin.datalogger        ] INFO   : Telemetry data: {'memfree': 2428656, 'temperature.28ff641d8fd7c022.onewire:0': 24.0, 'pressure.0x77.i2c:0': 1019.1, 'temperature.0x77.i2c:0': 22.33, 'humidity.0x77.i2c:0': 33.97}
      937.0599 [terkin.telemetry         ] ERROR  : MQTT publishing failed
    Traceback (most recent call last):
      File "/flash/lib/terkin/telemetry.py", line 438, in publish
      File "dist-packages/mqtt.py", line 121, in publish
      File "dist-packages/mqtt.py", line 161, in wait_msg
    OSError: [Errno -1] ERR_MEM

      939.9525 [terkin.telemetry         ] ERROR  : MQTT publishing failed
    Traceback (most recent call last):
      File "/flash/lib/terkin/telemetry.py", line 438, in publish
      File "dist-packages/mqtt.py", line 111, in publish
    OSError: [Errno 113] ECONNABORTED

Will get resumed automatically. No need to worry about. Might be suppressed in the future.



Spurious "syntax error" / Filesystem corruption
===============================================

Background
----------
https://community.hiveeyes.org/t/fipy-verliert-programm-nach-power-off-durch-leeren-lipo-vermutlich-brownout-filesystem-corruption/2057

Solution
--------
Use LittleFS, see https://github.com/hiveeyes/terkin-datalogger/blob/master/doc/getting-started.rst


Network stack overload
======================

STGTFO
------
::

       35.9258 [terkin.telemetry         ] ERROR  : MQTT publishing failed
    Traceback (most recent call last):
      File "/flash/lib/terkin/telemetry.py", line 477, in publish
      File "dist-packages/mqtt.py", line 110, in publish
    OSError: [Errno 118] EHOSTUNREACH

       35.9677 [terkin.telemetry         ] ERROR  : Telemetry to mqtt://weather.hiveeyes.org/workbench/testdrive/area-38/fipy-workbench-01 failed
    Traceback (most recent call last):
      File "/flash/lib/terkin/telemetry.py", line 96, in transmit
      File "/flash/lib/terkin/telemetry.py", line 233, in transmit
      File "/flash/lib/terkin/telemetry.py", line 399, in send
      File "/flash/lib/terkin/telemetry.py", line 399, in send
    TelemetryTransportError: Protocol adapter not connected: TelemetryAdapterError: MQTT publishing failed: [Errno 118] EHOSTUNREACH

Observation
-----------
We found this to happen if the sleep time between cycles is too short or even zero,
so the program is just looping too fast and seems to overload the network or socket stack.


Access ADC after shutting down
==============================
After shutting down the ADC used for measuring the battery level,
the system might attempt to read it again. This might happen if
all peripherals has been shut down in order to prepare for
deepsleep but the device won't actually go to deepsleep then,
e.g. caused by downstream errors like ``ERROR: Failed to special-sleep``.

::

     1752.4836 [terkin.datalogger        ] ERROR  : Reading sensor "SystemBatteryLevel" failed
    Traceback (most recent call last):
      File "/flash/lib/terkin/datalogger.py", line 167, in read_sensors
      File "/flash/lib/terkin/sensor.py", line 260, in read
    OSError: the requested operation is not possible

Solution
--------
Just initialize it again, like::

    adc.init()


- https://forum.pycom.io/topic/4493/trouble-uploading-to-fipy
- https://forum.pycom.io/topic/4479/fipy-upload-failed


NVRAM maximum key length
========================
::

    >>> pycom.nvs_set('0123456789012345', 42)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ValueError: Key is invalid

    >>> len('0123456789012345')
    16

Conclusion: Use a maximum length of 15 characters as NVRAM key.


Only one hash operation at once
===============================
Otherwise...
::

    >>> hashlib.sha1('abc')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    OSError: only one active hash operation is permitted at a time


When webserver is started twice
===============================
::

       22.0515 [terkin.api.http          ] INFO   : Setting up HTTP API
       22.1503 [terkin.api.http          ] INFO   : Starting HTTP server
    Traceback (most recent call last):
      File "main.py", line 65, in <module>
      File "main.py", line 60, in main
      File "/flash/lib/terkin/datalogger.py", line 116, in start
      File "/flash/lib/terkin/device.py", line 206, in start_network_services
      File "/flash/lib/terkin/network/core.py", line 71, in start_httpserver
      File "/flash/lib/terkin/api/http.py", line 42, in start
      File "dist-packages/microWebSrv.py", line 224, in Start
    OSError: [Errno 12] ENOMEM


Core dump when handling more than 4000something characters within a single string
=================================================================================
::

    rename: /flash/backup/settings.py
    ***ERROR*** A stack overflow in task MPThread has been detected.
    abort() was called at PC 0x40099324 on core 1

    Backtrace: 0x400991b3:0x3fff07c0 0x4009930b:0x3fff07e0 0x40099324:0x3fff0800 0x40095a33:0x3fff0820 0x400976a4:0x3fff0850 0x4009765a:0x00000000
    Backtrace: 0x40098864:0x3fff0460 0x40097116:0x3fff0480 0x4009982f:0x3fff04b0 0x40099b6e:0x3fff0680 0x4009946f:0x3fff06c0 0x400996aa:0x3fff06e0 0x40083882:0x3fff0700 0x400991b0:0x3fff07c0 0x4009930b:0x3fff07e0 0x40099324:0x3fff0800 0x40095a33:0x3fff0820 0x400976a4:0x3fff0850 0x4009765a:0x00000000

    Re-entered core dump! Exception happened during core dump!
    Rebooting...
    ets Jun  8 2016 00:22:57

    rst:0xc (SW_CPU_RESET),boot:0x12 (SPI_FAST_FLASH_BOOT)
    configsip: 0, SPIWP:0xee
    clk_drv:0x00,q_drv:0x00,d_drv:0x00,cs0_drv:0x00,hd_drv:0x00,wp_drv:0x00
    mode:DIO, clock div:1
    load:0x3fff8028,len:8
    load:0x3fff8030,len:2156
    ho 0 tail 12 room 4
    load:0x4009fa00,len:19208
    entry 0x400a05f4
    Initializing filesystem as LittleFS!
    Traceback (most recent call last):
      File "main.py", line 29, in <module>
      File "settings.py", line 157
    SyntaxError: invalid syntax


When invoking ``os.stat`` from a threaded MicroWebSrv::

    ***ERROR*** A stack overflow in task MPThread has been detected.
    abort() was called at PC 0x40099324 on core 1

    Backtrace: 0x400991b3:0x3fff0840 0x4009930b:0x3fff0860 0x40099324:0x3fff0880 0x40095a5d:0x3fff08a0 0x400976a4:0x3fff08d0 0x4009765a:0xa5a5a5a5

    ================= CORE DUMP START =================
    dE4AABMAAABsAQAA
    KKL9P8Cg/T8gov0/
    wKD9P8Ch/T+xR2vHAFn8PwBZ/D8oov0/+Fj8PwEAAADc1P0/3NT9Pyii/T8AAAAA
    GAAAACSe/T9pcGMwAJPi3UASjflpzu0AAAAAACCi/T8AAAAAIAoGABgAAAAAAAAA
    AAAAAAAAAAAAAAAAAAAAAAAAAAAo0f0/kNH9P/jR/T8AAAAAAAAAAAEAAAAAAAAA
    p3xAPwAAAAC84glAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACfqcA==


Core dump when accessing network, filesystem and UART
=====================================================
::

    os.stat: /flash/backup
    ***ERROR*** A stack overflow in task MPThread has been detected.
    abort() was called at PC 0x40099324 on core 1

    Backtrace: 0x400991b3:0x3fff0870 0x4009930b:0x3fff0890 0x40099324:0x3fff08b0 0x40095a5d:0x3fff08d0 0x400976a4:0x3fff0900 0x4009765a:0x3ffdd458


Sometimes, WiFi is not up
=========================
::

       28.3683 [terkin.datalogger        ] ERROR  : Reading sensor "SystemWiFiMetrics" failed
    Traceback (most recent call last):
      File "/flash/lib/terkin/datalogger.py", line 293, in read_sensors
      File "/flash/lib/terkin/util.py", line 179, in __exit__
      File "/flash/lib/terkin/datalogger.py", line 293, in read_sensors
      File "/flash/lib/terkin/network/wifi.py", line 327, in read
    OSError: the requested operation is not possible

       29.6547 [terkin.telemetry         ] ERROR  : MQTT publishing failed
    Traceback (most recent call last):
      File "/flash/lib/terkin/telemetry.py", line 542, in publish
      File "dist-packages/mqtt.py", line 120, in publish
    OSError: [Errno 118] EHOSTUNREACH

       29.7129 [terkin.telemetry         ] ERROR  : Telemetry to mqtt://swarm.hiveeyes.org/hiveeyes/testdrive/area-38/fipy-workbench-01 failed
    Traceback (most recent call last):
      File "/flash/lib/terkin/telemetry.py", line 119, in transmit
      File "/flash/lib/terkin/telemetry.py", line 279, in transmit
      File "/flash/lib/terkin/telemetry.py", line 460, in send
      File "/flash/lib/terkin/telemetry.py", line 460, in send
    TelemetryTransportError: Protocol adapter not connected: TelemetryAdapterError: MQTT publishing failed: [Errno 118] EHOSTUNREACH


Sometimes, not all files get transferred using FTP
==================================================
This leaves the system in a broken state.
::

    $ time make recycle-ng
    Device port: ip => 192.168.178.123
    Uploading MicroPython code to device
    time lftp -u micro,python 192.168.178.123 < tools/upload-all.lftprc
    mirror: Access failed: 550  (__init__.py)
    mirror: Access failed: 550  (core.py)
    mirror: Access failed: 550  (ip.py)
    mirror: Access failed: 550  (lora.py)

    Traceback (most recent call last):
      File "main.py", line 31, in <module>
      File "/flash/lib/hiveeyes/datalogger.py", line 14, in <module>
      File "/flash/lib/terkin/datalogger.py", line 13, in <module>
      File "/flash/lib/terkin/network/__init__.py", line 1, in <module>
    ImportError: cannot import name NetworkManager


Sometimes, the Web server runs out of memory, crashing the system
=================================================================
This happens on soft reboots.
::

       22.3080 [terkin.api.http          ] INFO   : Setting up HTTP API
       22.4902 [terkin.api.http          ] INFO   : Starting HTTP server
    Traceback (most recent call last):
      File "main.py", line 65, in <module>
      File "main.py", line 60, in main
      File "/flash/lib/terkin/datalogger.py", line 130, in start
      File "/flash/lib/terkin/device.py", line 211, in start_network_services
      File "/flash/lib/terkin/network/core.py", line 70, in start_httpserver
      File "/flash/lib/terkin/api/http.py", line 54, in start
      File "dist-packages/microWebSrv.py", line 224, in Start
    OSError: [Errno 12] ENOMEM


Setting invalid runtime configuration setting
=============================================
Here: Setting ``main.interval.field`` to ``None``.
::

      224.3915 [terkin.device            ] INFO   : Waiting for None seconds
      224.4166 [terkin.datalogger        ] ERROR  : Failed to hibernate, falling back to regular sleep
    Traceback (most recent call last):
      File "/flash/lib/terkin/datalogger.py", line 214, in sleep
      File "/flash/lib/terkin/device.py", line 334, in hibernate
    TypeError: can't convert NoneType to float

      224.4534 [terkin.datalogger        ] INFO   : Sleeping for None seconds
    Traceback (most recent call last):
      File "main.py", line 65, in <module>
      File "main.py", line 60, in main
      File "/flash/lib/terkin/datalogger.py", line 145, in start
      File "/flash/lib/terkin/datalogger.py", line 162, in start_mainloop
      File "main.py", line 53, in loop
      File "/flash/lib/hiveeyes/datalogger.py", line 141, in loop
      File "/flash/lib/terkin/datalogger.py", line 187, in loop
      File "/flash/lib/terkin/datalogger.py", line 221, in sleep
    TypeError: can't convert NoneType to float
