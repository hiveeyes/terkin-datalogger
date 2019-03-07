########################
Hiveeyes MPY data logger
########################


************
Introduction
************
Before getting started with this, please `upgrade the Pycom firmware`_
on your device.
After that, be prepared to put ``make recycle``, ``CTRL+C``, ``CTRL+D``
and ``CTRL+X`` into your muscle memory. Otherwise, let's go shopping.

The `General information about the WiPy`_ on the MicroPython documentation
pages is a good start to read more about the things that will follow.

This is a work in progress.


********
Features
********
This is a rough outline and will be extended over time.

Overview
========
- Lightweight unopinionated firmware framework
- Concise, readable and modularized code which is easy to follow
- Convenient development sandbox provides quick iteration cycles
- Based on approved software libraries
- Batteries included

Architecture
============
- Datalogger and Device
  Singletons representing the data logger application and your logging device.

- Sensor and HardwareDriver
  Sensor components wrap hardware drivers to generalize sensor reading.

- Telemetry and TelemetryTransport
  The telemetry subsystem uses different transport adapters for
  different connectivity scenarios.


********
Synopsis
********
::

    # Setup the development sandbox. Once.
    make setup

    # Upload and run the program. Regularly.
    make recycle


*****
Setup
*****
You mean it. Thanks for listening already and enjoy the ride.

Configuration
=============
Please adjust the serial port in ``config.mk``. YMMV.

Setup development sandbox
=========================
This will install different tools into the local directory which we
consider essentially for efficient MicroPython development.
The programming environment driven through different ``make`` targets
and the accompanying documentation is based on a successful installation
of these tools.
::

    make setup


*********
Operation
*********

Configure your program
======================
Make a copy of ``settings.example.py`` into ``settings.py``
and adjust each configuration setting appropriately. The
documentation of all parameters is in the file itself
and should be self-explanatory.


Upload and run your program
===========================
This will upload the files ``boot.py``, ``main.py`` and ``settings.py`` and
then issue a hard reset, so this will essentially run your program from
scratch as it will likewise happen in the real world::

    make recycle


***************
Getting started
***************
Connect to the REPL shell on the device::

    make repl
    Pycom MicroPython 1.18.2.r3 [v1.8.6-849-a1641ca] on 2019-02-28; FiPy with ESP32

    # General help
    >>> help()

    # List built-in modules
    >>> help('modules')


MicroPython control commands
============================
At this point, you should take a minute to have a look at
`getting started with Pycom MicroPython`_. It will be worth it as it will walk
you through essential function keys you will need after taking the red pill.


***************
Troubleshooting
***************
Please have a look at `Hiveeyes MPY data logger troubleshooting`_.


****************
Acknowledgements
****************
Thanks to all the `contributors`_ who got their hands dirty with it
and helped to co-create and conceive it in one way or another.
You know who you are.

This is a reference list of things this program is and will partly be based upon:

- https://github.com/pycom/pycom-libraries
- https://github.com/micropython/micropython-lib
- https://github.com/daq-tools/terkin/tree/master/src/micropython
- The RaTrack firmware (undisclosed yet)
- https://github.com/microhomie/microhomie
- https://github.com/ClemensGruber
- https://github.com/hiveeyes/arduino
- https://github.com/jacobron/EasyHive_Pycom_Shield/tree/master/V1.0/software
- https://github.com/walterheisenberg/hivewatch_esp32
- https://github.com/Quernon/honeypi
- https://github.com/geda/hx711-lopy

Standing on the shoulders of giants. Thank you so much!


.. _contributors: https://github.com/hiveeyes/hiveeyes-micropython-firmware/blob/master/CONTRIBUTORS.rst
.. _upgrade the Pycom firmware: https://github.com/hiveeyes/hiveeyes-micropython-firmware/blob/master/doc/pycom-firmware-upgrade.rst
.. _General information about the WiPy: https://docs.micropython.org/en/latest/wipy/general.html
.. _getting started with Pycom MicroPython: https://github.com/hiveeyes/hiveeyes-micropython-firmware/blob/master/doc/pycom-getting-started.rst
.. _Hiveeyes MPY data logger troubleshooting: https://github.com/hiveeyes/hiveeyes-micropython-firmware/blob/master/doc/troubleshooting.rst
