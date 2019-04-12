#####################################
Hiveeyes MicroPython Datalogger setup
#####################################

************
Introduction
************
You mean it. Thanks for listening already and enjoy the ride.

This part of the documentation covers the installation of the
MicroPython firmware development environment and other software
components it relies on.

The setup process has been confirmed to work on Linux, macOS and the
Windows Subsystem for Linux (Win10).

The first step to using any software package is getting it
properly installed. Please read this section carefully.


*****
Setup
*****

Prerequisites
=============
To perform the next steps, please install the following software
packages on your machine::

    apt install make patch wget git python python3 python-virtualenv


Acquire source code
===================
::

    git clone https://github.com/hiveeyes/hiveeyes-micropython-firmware
    cd hiveeyes-micropython-firmware


Setup development sandbox
=========================
This will create a Python virtualenv and install all Python packages
listed in ``requirements-dev.txt``, e.g. the ``rshell`` utility::

    make setup-environment

The programming environment driven through different ``make`` targets
and the accompanying documentation is based on a successful installation
of these tools.

We consider these tools essential for efficient MicroPython development.

Pre-flight checks
=================
Check serial interface connectivity. Example::

    make list-serials
    USB Serial Device 04d8:ef98 with vendor 'Pycom' serial 'Pye090a1' found @/dev/cu.usbmodemPye090a1

Configure serial port
=====================
After connecting the device to your USB port, you should tell the sandbox
about the UART device the MicroPython MCU is now connected to.
Running ``make list-serials`` might help here.

Example::

    export MCU_SERIAL_PORT=/dev/cu.usbmodemPye090a1

Check board and device
======================
As pre-flight checks, you might want to execute::

    make list-boards
    pyboard @ pyboard connected Epoch: 1970 Dirs: /flash /pyboard/flash

::

    make device-info

    Pycom MicroPython 1.20.0.rc8 [v1.9.4-7b83c6d] on 2019-03-06; FiPy with ESP32
    Type "help()" for more information.
    >>>
    >>> import os ; os.uname()
    (sysname='FiPy', nodename='FiPy', release='1.20.0.rc8', version='v1.9.4-7b83c6d on 2019-03-06', machine='FiPy with ESP32', lorawan='1.0.2', sigfox='1.0.1')
    >>> took 1.104 seconds


******************
Board provisioning
******************
You might want to run these command after each successful ``git pull``,
as this might bring in adjustments to the package dependency list.

Install required packages
=========================
The MicroPython firmware pulls in some packages from the MicroPython standard
library and beyond. These steps will acquire the required packages and upload
them to the device.
::

    make install-requirements

This will download all required packages listed in ``requirements-mpy.txt``
and ``Makefile`` to your workstation, apply some modifications to this tree
and then upload it to the device using ``rshell rsync``.

Install framework
=================
This will install the Terkin datalogger framework by uploading all files
from the ``terkin`` and ``hiveeyes`` folders::

    make install-framework

Install sketch
==============
Upload the files ``boot.py``, ``main.py`` and ``settings.py`` from
the root directory::

    make install-sketch


******************
Further guidelines
******************

Access command shell
====================
::

    make rshell

Access REPL shell
=================
Connect to the REPL shell on the device::

    make repl
    Pycom MicroPython 1.20.0.rc8 [v1.9.4-7b83c6d] on 2019-03-06; FiPy with ESP32

    # General help
    >>> help()

    # List built-in modules
    >>> help('modules')


Reset the device
================
::

    make reset-device

Format ``/flash``
=================
This will reformat the ``/flash`` filesystem, thus destroying all data there::

    make purge-device


MicroPython control commands
============================
At this point, you should take a minute to have a look at
`getting started with Pycom MicroPython`_. It will be worth it as it will walk
you through essential function keys you will need after taking the red pill.

.. _getting started with Pycom MicroPython: https://github.com/hiveeyes/hiveeyes-micropython-firmware/blob/master/doc/pycom-getting-started.rst
