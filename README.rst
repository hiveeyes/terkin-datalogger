.. image:: https://img.shields.io/badge/MicroPython-3.4-green.svg
    :target: https://github.com/hiveeyes/terkin-datalogger

.. image:: https://img.shields.io/badge/CPython-3.x-green.svg
    :target: https://github.com/hiveeyes/terkin-datalogger

.. image:: https://img.shields.io/github/tag/hiveeyes/terkin-datalogger.svg
    :target: https://github.com/hiveeyes/terkin-datalogger

|

#################
Terkin Datalogger
#################

Data logging for humans, written in MicroPython.


*****
About
*****
The Terkin Datalogger is a flexible data logger application
for MicroPython and CPython environments.

It has been conceived for the Bee Observer (BOB) project and was funded by the BMBF.

- https://bee-observer.hiveeyes.org/bmbf-verbundprojekt
- https://community.hiveeyes.org/c/bee-observer


********
Features
********
Batteries included.

Overview
========
- Modular firmware framework
- Flexible configuration settings subsystem
- Compatible with MicroPython and CPython
- Concise, readable and modularized code which is easy to follow
- Decoupled code domains and data models for sensors vs. telemetry
- Based on approved modules from the MicroPython standard library
- Convenient development sandbox and test suite for quick iteration cycles

Architecture
============
- ``Datalogger`` and ``Device``
  are singleton objects representing the data logger application and your logging device.

- Components of the sensor subsystem wrap hardware drivers to generalize sensor reading.

- The telemetry subsystem uses different transport adapters to
  implement various connectivity scenarios.


****************
Hardware support
****************

Architectures
=============
- x86_64, ARM, ESP32, STM32

Platforms
=========
- Genuine MicroPython: PYBOARD-D, TTGO T-Call, TTGO T-Beam
- Pycom MicroPython: WiPy, LoPy4, FiPy
- CPython: RaspberryPi, `Dragino LoRa/GPS HAT`_
- Connectivity: WiFi, SIM800 for GPRS, SX127x for LoRa, Sequans Monarch for `LTE Cat M1`_ or `LTE Cat NB1`_

Peripherals
===========
- Sensors: 1-Wire, I2C, ADC, System, WiFi
- Drivers: DS18B20, BME280, SI7021, HX711, MAX17043, DS3231, AT24C32
- Telemetry: WiFi/MQTT, WiFi/HTTP, SIM800/HTTP, LoRaWAN/TTN


***********
Screenshots
***********

Sensorkit and board
===================
.. figure:: https://ptrace.hiveeyes.org/2019-06-17_bob-sensorkit-small.jpeg
    :target: https://ptrace.hiveeyes.org/2019-06-17_bob-sensorkit-large.jpeg

    Bee Observer Sensorkit, assembled.

.. figure:: https://ptrace.hiveeyes.org/2019-06-17_bob-board-small.jpeg
    :target: https://ptrace.hiveeyes.org/2019-06-17_bob-board-large.jpeg

    Bee Observer Board, assembled.


Console output
==============
To get a better idea about how running this firmware will feel like when
watching its log output, we collected some excerpts at
`Running the Terkin Datalogger`_.


***************
Getting started
***************

Introduction
============
See `Getting started with the Terkin Datalogger`_.

The documentation covers the main features of the MicroPython datalogger firmware
and walks you through the setup process of the development sandbox environment
in detail.

If you feel you have questions about anything you might 
encounter during the setup and installation process or 
if you even have suggestions to improve things, feel free
to get back to us by creating an issue on the GitHub repository.

Download
========
On the `release page`_ , bundles of the most recent software versions
are available through ``.tar.gz`` and ``.zip`` archives.
These are suitable for uploading through Pymakr or similar
development environments / file synchronization tools.

Configuration
=============
Copy the ``settings.example.py`` blueprint into ``settings.py``
and adjust each configuration setting appropriately. The
documentation of all parameters is in the file itself
and should be reasonably self-explanatory.
For using Terkin with TTN/LoRaWAN find some more details
`here <https://github.com/hiveeyes/terkin-datalogger/blob/master/client/TTN/README.rst>`_.

Sandbox setup
=============
If you would like to contribute to the development or want to setup
a development environment for running the head version of this
software, please follow up at `Setup Terkin Datalogger sandbox`_
to read about how to install the MicroPython firmware development environment
and other software components it relies on and how to configure it properly.

The programming environment is command line based and has been tested
successfully on **Linux**, **macOS** and the Windows Subsystem for Linux (WSL)
shipped with **Windows 10**.


*******************
Project information
*******************

About
=====
These links will guide you to the source code of the
»Terkin Datalogger« and its documentation.

- `Terkin Datalogger on GitHub <https://github.com/hiveeyes/terkin-datalogger>`_

Contributing
============
We are always happy to receive code contributions, ideas, suggestions
and problem reports from the community.

So, if you'd like to contribute you're most welcome.
Spend some time taking a look around, locate a bug, design issue or
spelling mistake and then send us a pull request or `create an issue`_.

Thanks in advance for your efforts, we really appreciate any help or feedback.

Licenses
========
This software is copyright © 2017-2020 The Hiveeyes Developers and contributors. All rights reserved.

It is and will always be **free and open source software**.

Use of the source code included here is governed by the GNU General Public License
`GNU-GPL-3.0`_ and the European Union Public License `EUPL-1.2`_.
Please also have a look at the notices about licenses of third-party components.


****************
Acknowledgements
****************
This firmware is an effort of many people. So, thanks to all
the `contributors`_ who got their hands dirty and helped to
co-create and conceive it in one way or another.

You know who you are.


----

Have fun!


.. _Setup Terkin Datalogger sandbox: https://github.com/hiveeyes/terkin-datalogger/blob/master/doc/sandbox-setup.rst
.. _contributors: https://github.com/hiveeyes/terkin-datalogger/blob/master/CONTRIBUTORS.rst
.. _create an issue: https://github.com/hiveeyes/terkin-datalogger/issues/new
.. _Getting started with the Terkin Datalogger: https://github.com/hiveeyes/terkin-datalogger/blob/master/doc/getting-started.rst
.. _Running the Terkin Datalogger: https://github.com/hiveeyes/terkin-datalogger/blob/0.4.0/doc/screenshots/05-running.rst
.. _release page: https://github.com/hiveeyes/terkin-datalogger/releases

.. _Pycom FiPy: https://pycom.io/product/fipy/
.. _Pycom LoPy4: https://pycom.io/product/lopy4/
.. _Pycom WiPy3: https://pycom.io/product/wipy-3-0/

.. _LTE Cat M1: https://docs.pycom.io/tutorials/lte/cat-m1.html
.. _LTE Cat NB1: https://docs.pycom.io/tutorials/lte/nb-iot.html

.. _GNU-GPL-3.0: https://opensource.org/licenses/GPL-3.0
.. _EUPL-1.2: https://opensource.org/licenses/EUPL-1.2

.. _Dragino LoRa/GPS HAT: https://wiki.dragino.com/index.php?title=Lora/GPS_HAT
