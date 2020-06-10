.. include:: ../../_resources.rst


.. _pycom-info:

###############################
Information about Pycom devices
###############################

As a general introduction, you might want to read the `Pycom Quickstart Guide`_.


******************
Upstream resources
******************

Documentation
=============
- https://pycom.io/downloads/
- https://docs.pycom.io/gettingstarted/installation/firmwaretool.html
- https://github.com/pycom/pycom-documentation/blob/master/advanced-topics/cli.md
- https://docs.pycom.io/advance/downgrade.html

Firmware downloads
==================
- https://software.pycom.io/downloads/WiPy.html
- https://software.pycom.io/downloads/LoPy.html
- https://software.pycom.io/downloads/FiPy.html

Development branches
====================
If you feel you want to follow Pycom's development more closely, you
might find these pointers convenient.

- 1.20.x: https://github.com/pycom/pycom-micropython-sigfox/commits/release-candidate
- 1.19.x: https://github.com/pycom/pycom-micropython-sigfox/commits/development
- 1.18.x: https://github.com/pycom/pycom-micropython-sigfox/commits/master

More resources
==============
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

- `Quick reference for the ESP32`_
- `ESP32 Datasheet`_


*****************
Download firmware
*****************
Acquire recent Pycom MicroPython firmware binaries::

    # https://software.pycom.io/downloads/FiPy.html
    wget https://software.pycom.io/downloads/FiPy-1.20.0.rc11.tar.gz


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

    # Define serial port.
    export MCU_PORT=/dev/cu.usbmodemPye090a1

    # Define serial port for "pycom-fwtool-cli"
    export ESPPORT=$MCU_PORT

    # Upload Pycom firmware.
    pycom-fwtool-cli --verbose flash --tar FiPy-1.20.0.rc11.tar.gz

2. Reset device

You can reset the device either by

- running ``import machine; machine.reset()`` on the MicroPython REPL shell prompt
- pressing the reset button once
- power-cycling the device

3. Connect to REPL shell on device::

    make repl
    Pycom MicroPython 1.20.0.rc11 [v1.9.4-0a38f88] on 2019-05-14; FiPy with ESP32

    # General help
    >>> help()

    # List built-in modules
    >>> help('modules')


*****************
Board information
*****************
In order to get board information, you might want to check out some commands like::

    # Read chip identifier
    pycom-fwtool-cli --verbose chip_id
    ESP32D0WDQ6 (revision (unknown 0xa))

    # Read MAC address of WiFi NIC
    pycom-fwtool-cli --verbose wmac
    WMAC=807D3AC2DE44

    # Read SMAC
    pycom-fwtool-cli --verbose smac
    SMAC=70B3D54992DBE31D

By watching the preamble, you might be able to deduce the
firmware version of the expansion board::

    Running in PIC mode
    Product ID: 152 HW Version: 7 FW Version: 0.0.11
    Connecting....
    Uploading stub...
    Running stub...
    Stub running...
    Changing baud rate to 921600
    Changed.
