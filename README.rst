###############################
Hiveeyes MicroPython Datalogger
###############################

Data logging for humans.


************
Introduction
************
This document covers the main features of the MicroPython datalogger firmware
and walks you through the setup process of the development sandbox environment
in detail.

This programming environment has been tested successfully on Linux, macOS and
WSL, the Windows Subsystem for Linux (Win10).


********
Features
********

Overview
========
- Lightweight unopinionated firmware framework
- Flexible configuration settings subsystem
- Concise, readable and modularized code which is easy to follow
- Decoupled code domains and data models for sensors vs. telemetry
- Based on approved modules from the MicroPython standard library
- Convenient development sandbox for quick iteration cycles

Batteries included.

Architecture
============
- Datalogger and Device

  Singleton objects representing the data logger application and your logging device.

- Sensor and HardwareDriver

  Sensor components wrap hardware drivers to generalize sensor reading.

- Telemetry and TelemetryTransport

  The telemetry subsystem uses different transport adapters for different
  connectivity scenarios. MQTT and HTTP over TCP over WiFi is implemented
  already and TTN over LoRaWAN is almost there (thanks, Jan and Richard!).
  We are still waiting for confirmation of LTE `CAT-M1`_ or `NB-IoT`_
  connectivity in Germany (thanks, Ron and Jan!).

.. _CAT-M1: https://docs.pycom.io/tutorials/lte/cat-m1.html
.. _NB-IoT: https://docs.pycom.io/tutorials/lte/nb-iot.html


****************
Acknowledgements
****************
This firmware program is an effort of many people. So, thanks to all
the `contributors`_ who got their hands dirty and helped to co-create
and conceive it in one way or another. You know who you are.


***************
Getting started
***************
Before getting started with this, please `upgrade the Pycom firmware`_
on your device.
After that, be prepared to put ``make recycle``, ``CTRL+C``, ``CTRL+D``
and ``CTRL+X`` into your muscle memory. Otherwise, let's go shopping.

We collected some resources which offer a good start to read more about
MicroPython development in general as well as the specific details of
the Pycom MicroPython implementation.

- `MicroPython documentation`_
- `MicroPython libraries`_

- `General information about the WiPy`_ on the MicroPython documentation pages
- `Pycom documentation`_
- `Getting started with Pycom MicroPython`_
- `Pycom MicroPython Modules`_
- `Pycom Vendor Modules`_

.. note::

    Please recognize this is a work in progress. Many places are just sketched
    out and many gaps will have to be closed. So, this will be extended over time.


*************
Sandbox setup
*************
Please follow up at `Hiveeyes MicroPython Datalogger setup`_ to read about how to
install the MicroPython firmware development environment and other software
components it relies on and how to configure it properly.


*****************
Sandbox operation
*****************

Configure serial port
=====================
After connecting the device to your USB port, you should tell the sandbox
about the UART device the MicroPython MCU is now connected to.
Running ``make list-serials`` might help here.

Example::

    export MCU_SERIAL_PORT=/dev/cu.usbmodemPye090a1

Configure your program
======================
Copy the ``settings.example.py`` blueprint into ``settings.py``
and adjust each configuration setting appropriately. The
documentation of all parameters is in the file itself
and should be self-explanatory.

If you feel you have questions about the semantics of the
configuration settings or if you even have suggestions to
improve things, feel free to get back to us by creating
an issue on the GitHub repository.

Upload and run your program
===========================
There's a one-step command to upload all files from the current working tree
to the MicroPython device. After that, it will reset the device by software
(cold start), which essentially will run your program from scratch as it will
likewise happen in the real world::

    make recycle

This will upload the files ``boot.py``, ``main.py`` and ``settings.py`` from
the root directory as well as all files from the ``lib``, ``hiveeyes`` and
``terkin`` folders.

Update required packages
========================
This software pulls in some Python packages from different sources. In case
something will be updated here from upstream, you will likely find some
packages missing when running your firmware.

In order to flush and update the whole set of Python packages both on your
workstation and on your device, just run::

    make refresh-requirements

This will download all required packages to the local ``dist-packages``,
apply some modifications to this tree and then upload it to the device.


***************
Troubleshooting
***************
Please have a look at `Hiveeyes MicroPython Datalogger troubleshooting`_.


******************
Reference hardware
******************
This software has been designed on a `Pycom FiPy`_. However, it might also
work on MicroPython hardware from different vendors. If not, corresponding
feature requests are welcome, but pull requests are even better!

.. image:: https://i0.wp.com/pycom.io/wp-content/uploads/2018/08/fipyTop.png?fit=300%2C300&ssl=1


Please followup on the `Reference hardware`_ page for different hardware
configurations based on devices like these.


----

Have fun!

.. _Hiveeyes MicroPython Datalogger setup: https://github.com/hiveeyes/hiveeyes-micropython-firmware/blob/master/doc/setup.rst
.. _contributors: https://github.com/hiveeyes/hiveeyes-micropython-firmware/blob/master/CONTRIBUTORS.rst

.. _upgrade the Pycom firmware: https://github.com/hiveeyes/hiveeyes-micropython-firmware/blob/master/doc/pycom-firmware-upgrade.rst
.. _General information about the WiPy: https://docs.micropython.org/en/latest/wipy/general.html
.. _MicroPython documentation: https://micropython.readthedocs.io/
.. _MicroPython libraries: https://micropython.readthedocs.io/en/latest/library/
.. _Pycom MicroPython Modules: https://github.com/pycom/pydocs/tree/master/firmwareapi/micropython
.. _Pycom Vendor Modules: https://github.com/pycom/pydocs/tree/master/firmwareapi/pycom
.. _Pycom documentation: https://docs.pycom.io/
.. _Getting started with Pycom MicroPython: https://github.com/hiveeyes/hiveeyes-micropython-firmware/blob/master/doc/pycom-getting-started.rst

.. _Hiveeyes MicroPython Datalogger troubleshooting: https://github.com/hiveeyes/hiveeyes-micropython-firmware/blob/master/doc/troubleshooting.rst
.. _Reference hardware: https://github.com/hiveeyes/hiveeyes-micropython-firmware/blob/master/README-HARDWARE.md
.. _Pycom FiPy: https://pycom.io/product/fipy/
