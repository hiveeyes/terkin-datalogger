######################
Pycom firmware upgrade
######################


************
Introduction
************
By default, the Pycom FiPy arrived with::

    Pycom MicroPython 1.18.2.r3 [v1.8.6-849-a1641ca] on 2019-02-28; FiPy with ESP32

This document outlines the upgrade to::

    Pycom MicroPython 1.20.0.rc8 [v1.9.4-7b83c6d] on 2019-03-06; FiPy with ESP32

.. note::

    Please take into consideration that we are outlining our best practices here.
    While in this context we are only using official firmware releases from Pycom,
    there's always a chance that things might go south.
    Saying that, please don't hold us accountable for anything that might go wrong
    with your device.


*********************************
Install and acquire prerequisites
*********************************

Pycom Updater application
=========================
Install the Pycom Updater application for your platform.
See also:

- https://pycom.io/downloads/
- https://docs.pycom.io/gettingstarted/installation/firmwaretool.html
- https://github.com/pycom/pycom-documentation/blob/master/advanced-topics/cli.md

.. todo: Add command for ArchLinux et al.


Download firmware
=================
Acquire recent Pycom MicroPython firmware binaries::

    # https://software.pycom.io/downloads/FiPy.html
    wget https://software.pycom.io/downloads/FiPy-1.20.0.rc8.tar.gz


*******************
Prepare environment
*******************
We will be using the CLI Updater Command Line Update Utility here.

Conveniency::

    alias pycom-fwtool-cli='/Applications/Pycom\ Firmware\ Update.app/Contents/Resources/pycom-fwtool-cli'

Check board connectivity::

    pycom-fwtool-cli list
    /dev/cu.usbmodemPye090a1  [Expansion3] [USB VID:PID=04D8:EF98 SER=Pye090a1 LOCATION=20-2]
    /dev/cu.usbmodemPydb06d1  [Expansion3] [USB VID:PID=04D8:EF98 SER=Pydb06db LOCATION=20-2]


***************
Upload firmware
***************
1. Upload firmware::

    pycom-fwtool-cli --verbose --port /dev/tty.usbmodemPye090a1 flash --tar FiPy-1.20.0.rc8.tar.gz

2. Reset device

You can reset the device either by

- running ``import machine; machine.reset()`` on the MicroPython REPL shell prompt
- pressing the reset button once
- power-cycling the device

3. Connect to REPL shell on device::

    make repl
    Pycom MicroPython 1.20.0.rc8 [v1.9.4-7b83c6d] on 2019-03-06; FiPy with ESP32

    # General help
    >>> help()

    # List built-in modules
    >>> help('modules')


See also: https://docs.pycom.io/advance/downgrade.html
