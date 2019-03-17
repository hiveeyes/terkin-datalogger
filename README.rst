.. image:: https://img.shields.io/badge/MicroPython-3.4-green.svg
    :target: https://github.com/hiveeyes/hiveeyes-micropython-firmware

.. image:: https://img.shields.io/github/tag/hiveeyes/hiveeyes-micropython-firmware.svg
    :target: https://github.com/hiveeyes/hiveeyes-micropython-firmware

|

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

The programming environment is command line based and has been tested
successfully on **Linux**, **macOS** and the Windows Subsystem for Linux (WSL)
shipped with **Windows 10**.


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
  We are still waiting for confirmation of `LTE Cat M1`_ or `LTE Cat NB1`_
  connectivity in Germany (thanks, Ron and Jan!).



****************
Acknowledgements
****************
This firmware is an effort of many people. So, thanks to all
the `contributors`_ who got their hands dirty and helped to co-create
and conceive it in one way or another. You know who you are.


***************
Getting started
***************
Before getting started with this, please `upgrade the Pycom firmware`_
on your device. At the time of this writing, we are running
``Pycom MicroPython 1.20.0.rc8`` without any flaws yet.
After that, be prepared to put ``make recycle``, ``CTRL+C``, ``CTRL+D``
and ``CTRL+X`` into your muscle memory. Otherwise, let's go shopping.

.. note::

    Please recognize this is a work in progress. While many things are
    working already, some places might just have been sketched out.
    So, this firmware will be extended over time - you are dearly welcome
    to help closing some gaps.


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
The software pulls in some Python packages from different sources. In case
something will be updated from upstream which happens when adding new
packages, you might find some missing when running the firmware.

In order to flush and update the whole set of Python packages both on your
workstation and on your device, just run::

    make refresh-requirements

This will download all required packages to your workstation, apply some
modifications to this tree and then upload it to the device.

While operating on the respective ``dist-packages`` folders, it will first
purge the folder completely before populating it again.


******************
Reference hardware
******************
This software has been designed to run primarily on a `Pycom FiPy`_.
However, it might also work on MicroPython hardware from different vendors.
If you will find the firmware will not work on your MicroPython device,
corresponding reports are very welcome and pull requests are even better!

.. image:: https://ptrace.hiveeyes.org/2019_03-17_EasyHive%20Datalogger%20v1.jpg


Please follow up on the `Reference hardware`_ page for different hardware
configurations based on devices like these:

- `EasyHive Pycom-Shield`_
- `Hiverize Funktionsmuster`_
- `Hiveeyes Buerger`_


***************
Troubleshooting
***************
We have collected some tracebacks with root causes and solutions which might also help
you along, please have a look at `Hiveeyes MicroPython Datalogger troubleshooting`_.


*******************
Project information
*******************

About
=====
These links will guide you to the source code of the
»Hiveeyes MicroPython Datalogger« and its documentation.

- `Hiveeyes MicroPython Datalogger on GitHub <https://github.com/hiveeyes/hiveeyes-micropython-firmware>`_

Contributing
============
We are always happy to receive code contributions, ideas, suggestions
and problem reports from the community.

So, if you'd like to contribute you're most welcome.
Spend some time taking a look around, locate a bug, design issue or
spelling mistake and then send us a pull request or create an issue_.

Thanks in advance for your efforts, we really appreciate any help or feedback.

Licenses
========
This software is copyright © 2017-2019 The Hiveeyes Developers and contributors. All rights reserved.

It is and will always be **free and open source software**.

Use of the source code included here is governed by the GNU General Public License
`GNU-GPL-3.0`_ and the European Union Public License `EUPL-1.2`_.
Please also have a look at the notices about licenses of third-party components.

.. _issue: https://github.com/hiveeyes/hiveeyes-micropython-firmware/issues/new
.. _GNU-GPL-3.0: https://opensource.org/licenses/GPL-3.0
.. _EUPL-1.2: https://opensource.org/licenses/EUPL-1.2


----

Have fun!



*******************
Appendix: Resources
*******************
We collected some resources which offer a good start to read more about
MicroPython development in general as well as the specific details of
the Pycom MicroPython implementation.

- `MicroPython documentation`_
- `MicroPython libraries`_
- `Pycom MicroPython for ESP32`_

- `General information about the WiPy`_ on the MicroPython documentation pages
- `Pycom documentation`_
- `Getting started with Pycom MicroPython`_
- `Pycom MicroPython Modules`_
- `Pycom Vendor Modules`_
- `Pycom Libraries and Examples`_




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

.. _Pycom MicroPython for ESP32: https://github.com/pycom/pycom-micropython-sigfox
.. _Pycom Libraries and Examples: https://github.com/pycom/pycom-libraries

.. _Hiveeyes MicroPython Datalogger troubleshooting: https://github.com/hiveeyes/hiveeyes-micropython-firmware/blob/master/doc/troubleshooting.rst
.. _Pycom FiPy: https://pycom.io/product/fipy/

.. _Reference hardware: https://github.com/hiveeyes/hiveeyes-micropython-firmware/blob/master/README-HARDWARE.md
.. _EasyHive Pycom-Shield: https://github.com/hiveeyes/hiveeyes-micropython-firmware/blob/master/README-HARDWARE.md#easyhive-pycom-shield
.. _Hiverize Funktionsmuster: https://github.com/hiveeyes/hiveeyes-micropython-firmware/blob/master/README-HARDWARE.md#hiverize-funktionsmuster
.. _Hiveeyes Buerger: https://github.com/hiveeyes/hiveeyes-micropython-firmware/blob/master/README-HARDWARE.md#hiveeyes-buerger

.. _LTE Cat M1: https://docs.pycom.io/tutorials/lte/cat-m1.html
.. _LTE Cat NB1: https://docs.pycom.io/tutorials/lte/nb-iot.html
