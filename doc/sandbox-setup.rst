###############################
Setup Terkin Datalogger sandbox
###############################


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
About
*****
The programming environment is driven through different ``make`` targets
and the accompanying documentation is based on a successful installation
of these tools.

We consider these tools essential for efficient MicroPython development.


*****
Setup
*****

Prerequisites
=============
To perform the next steps, please install the following software
packages on your machine::

    apt install make patch wget git python python3 python-virtualenv lftp


Depending on your operating system, add your user to the group ``dialout``
in order to allow access to Serial. On Debian:

    addgroup $USER dialout
    # relogin or run
    # su - $USER

Acquire source code
===================
::

    # Initially, clone the source code repository.
    git clone https://github.com/hiveeyes/terkin-datalogger
    cd terkin-datalogger

    # Later, update the source code.
    git pull


Setup development sandbox
=========================
The MicroPython firmware pulls in some packages and programs like the
``rshell`` utility from the MicroPython standard library and beyond.
The following installation step will create a Python virtualenv and
download the required packages into it.

::

    make setup


Setup desktop notifications
===========================
These steps are optional but offer convenient desktop notifications
which will inform you about what's going on when operating the sandbox.

Linux/Windows::

    .venv3/bin/pip install py-notifier

macOS::

    .venv3/bin/pip install pync

Windows::

    .venv3/bin/pip install zroya


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

    export MCU_PORT=/dev/cu.usbmodemPye090a1

Pre-flight checks
=================
You might want to invoke some commands here in order to check board- and device-connectivity.

List all boards connected to workstation::

    make list-boards
    pyboard @ pyboard connected Epoch: 1970 Dirs: /flash /pyboard/flash

Display device information::

    make device-info

    Pycom MicroPython 1.20.0.rc11 [v1.9.4-0a38f88] on 2019-05-14; FiPy with ESP32
    Type "help()" for more information.
    >>>
    >>> import os ; os.uname()
    (sysname='FiPy', nodename='FiPy', release='1.20.0.rc11', version='v1.9.4-0a38f88 on 2019-05-14', machine='FiPy with ESP32', lorawan='1.0.2', sigfox='1.0.1')
    >>> took 1.079 seconds


Sandbox control commands
========================
At this point, you should take a minute to have a look at
`getting started with Pycom MicroPython`_. It will be worth it as it will walk
you through essential commands and function keys you will definitively need after
taking the red pill.

.. _getting started with Pycom MicroPython: https://github.com/hiveeyes/terkin-datalogger/blob/master/doc/getting-started.rst
