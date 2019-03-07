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


********
Synopsis
********
::

    # Setup the development sandbox (once).
    make setup

    # Upload and run sketch.
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

Upload and run your program
===========================
This will upload ``boot.py``, ``main.py`` and ``settings.py`` and then
issue a hard reset, so this will essentially run your program from scratch
as it will likewise happen in the real world::

    make recycle


***************
Getting started
***************
Connect to REPL shell on device::

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


*******
Credits
*******
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


.. _upgrade the Pycom firmware: https://github.com/hiveeyes/hiveeyes-micropython-firmware/blob/master/doc/pycom-firmware-upgrade.rst
.. _General information about the WiPy: https://docs.micropython.org/en/latest/wipy/general.html
.. _getting started with Pycom MicroPython: https://github.com/hiveeyes/hiveeyes-micropython-firmware/blob/master/doc/pycom-getting-started.rst
.. _Hiveeyes MPY data logger troubleshooting: https://github.com/hiveeyes/hiveeyes-micropython-firmware/blob/master/doc/troubleshooting.rst
