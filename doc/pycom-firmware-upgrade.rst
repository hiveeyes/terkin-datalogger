######################
Pycom firmware upgrade
######################


************
Introduction
************
As the Pycom firmware is continuously evolving, you might
also like to run their most recent release on your device.

We have been running this firmware successfully with::

    Pycom MicroPython 1.20.0.rc8 [v1.9.4-7b83c6d] on 2019-03-06; FiPy with ESP32, published on 07 Mar 2019
    Pycom MicroPython 1.20.0.rc11 [v1.9.4-0a38f88] on 2019-05-14; FiPy with ESP32, published on 14 May 2019

The most current firmwares as of 07 Jun 2019 are::

    Pycom MicroPython 1.18.2.r7, published on 14 May 2019
    Pycom MicroPython 1.20.0.rc11, published on 14 May 2019

Originally, the Pycom FiPy arrived with::

    Pycom MicroPython 1.18.2.r3 [v1.8.6-849-a1641ca] on 2019-02-28; FiPy with ESP32, published on 15 Mar 2019

.. note::

    Please take into consideration that we are outlining our best practices here.

    - We always try to run the most recent release available from the Pycom
      firmware download page.
    - While in this context we are only using official firmware releases
      from Pycom, there's always a chance that things might go south.
    - Saying that, you must not hold us accountable for anything that might go
      wrong with your device in any way when following these recommendations.


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


*********************************
Install and acquire prerequisites
*********************************

Pycom Updater application
=========================
Install the Pycom Updater application for your platform.

.. Todo: Add command for ArchLinux and beyond.


Download firmware
=================
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

    # Upload Pycom firmware.
    pycom-fwtool-cli --verbose --port $MCU_PORT flash --tar FiPy-1.20.0.rc11.tar.gz

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
    pycom-fwtool-cli --verbose --port $MCU_PORT chip_id
    ESP32D0WDQ6 (revision (unknown 0xa))

    # Read MAC address of WiFi NIC
    pycom-fwtool-cli --verbose --port $MCU_PORT wmac
    WMAC=807D3AC2DE44

    # Read SMAC
    pycom-fwtool-cli --verbose --port $MCU_PORT smac
    SMAC=70B3D54992DBE31D

By watching the preamble, you might be able to deduce the
firmware version of the expansion board.

::

    Running in PIC mode
    Product ID: 152 HW Version: 7 FW Version: 0.0.11
    Connecting....
    Uploading stub...
    Running stub...
    Stub running...
    Changing baud rate to 921600
    Changed.
