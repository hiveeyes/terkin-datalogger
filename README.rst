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
`Running the Hiveeyes MicroPython Datalogger`_.


***************
Getting started
***************

Introduction
============
See `Getting started with the Hiveeyes MicroPython Datalogger`_.

Download
========
On the `release page`_ , bundles of the most recent software versions
are available through ``.tar.gz`` and ``.zip`` archives.
These are suitable for uploading through Pymakr or similar
development environments / file synchronization tools.

Sandbox setup
=============
If you would like to contribute to the development or want to setup
a development environment for running the head version of this
software, please follow up at `Setup Hiveeyes MicroPython Datalogger sandbox`_
to read about how to install the MicroPython firmware development environment
and other software components it relies on and how to configure it properly.


*************
Configuration
*************
Copy the ``settings.example.py`` blueprint into ``settings.py``
and adjust each configuration setting appropriately. The
documentation of all parameters is in the file itself
and should be reasonably self-explanatory.

If you feel you have questions about the semantics of the
configuration settings or if you even have suggestions to
improve things, feel free to get back to us by creating
an issue on the GitHub repository.


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
spelling mistake and then send us a pull request or `create an issue`_.

Thanks in advance for your efforts, we really appreciate any help or feedback.

Licenses
========
This software is copyright © 2017-2019 The Hiveeyes Developers and contributors. All rights reserved.

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


.. _Setup Hiveeyes MicroPython Datalogger sandbox: https://github.com/hiveeyes/hiveeyes-micropython-firmware/blob/master/doc/sandbox-setup.rst
.. _contributors: https://github.com/hiveeyes/hiveeyes-micropython-firmware/blob/master/CONTRIBUTORS.rst
.. _create an issue: https://github.com/hiveeyes/hiveeyes-micropython-firmware/issues/new
.. _Getting started with the Hiveeyes MicroPython Datalogger: https://github.com/hiveeyes/hiveeyes-micropython-firmware/blob/master/doc/getting-started.rst
.. _Running the Hiveeyes MicroPython Datalogger: https://github.com/hiveeyes/hiveeyes-micropython-firmware/blob/0.4.0/doc/screenshots/05-running.rst
.. _release page: https://github.com/hiveeyes/hiveeyes-micropython-firmware/releases

.. _Pycom FiPy: https://pycom.io/product/fipy/
.. _Pycom LoPy4: https://pycom.io/product/lopy4/
.. _Pycom WiPy3: https://pycom.io/product/wipy-3-0/

.. _LTE Cat M1: https://docs.pycom.io/tutorials/lte/cat-m1.html
.. _LTE Cat NB1: https://docs.pycom.io/tutorials/lte/nb-iot.html

.. _GNU-GPL-3.0: https://opensource.org/licenses/GPL-3.0
.. _EUPL-1.2: https://opensource.org/licenses/EUPL-1.2
