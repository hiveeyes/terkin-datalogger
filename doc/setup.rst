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
Check serial interface connectivity::

    make list-serials

::

    USB Serial Device 04d8:ef98 with vendor 'Pycom' serial 'Pye090a1' found @/dev/cu.usbmodemPye090a1


*******************
Board configuration
*******************

Configure serial port
=====================
After connecting the device to your USB port, you should tell the sandbox
about the UART device the MicroPython MCU is now connected to.
Running ``make list-serials`` might help here.

Example::

    export MCU_SERIAL_PORT=/dev/cu.usbmodemPye090a1

Pre-flight checks
=================
Check board connectivity::

    make list-boards

When board communication could be established, this should yield in the end::

    pyboard @ pyboard connected Epoch: 1970 Dirs: /flash /pyboard/flash


******************
Board provisioning
******************
The MicroPython firmware requires some packages from the MicroPython standard
library and beyond. These steps will acquire the required packages and upload
them to the device.

Acquire packages::

    make install-requirements

Upload packages::

    make upload-requirements

After the dependency definitions in the file ``requirements-mpy.txt``
have been updated, it might become necessary to re-run this command again.


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

MicroPython control commands
============================
At this point, you should take a minute to have a look at
`getting started with Pycom MicroPython`_. It will be worth it as it will walk
you through essential function keys you will need after taking the red pill.

.. _getting started with Pycom MicroPython: https://github.com/hiveeyes/hiveeyes-micropython-firmware/blob/master/doc/pycom-getting-started.rst
