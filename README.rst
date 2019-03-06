########################
Hiveeyes MPY data logger
########################


***************
Getting started
***************

Configure environment
=====================
Adjust the serial port in the ``Makefile``.

First steps
===========
Install some tooling::

    make setup-environment

Connect to REPL shell on device::

    make repl
    Pycom MicroPython 1.18.2.r3 [v1.8.6-849-a1641ca] on 2019-02-28; FiPy with ESP32

    # General help
    >>> help()

    # List built-in modules
    >>> help('modules')


Control commands
================

Cheatsheet
----------
::

    CTRL-D: PYB: soft reboot
    CTRL-X: Exit REPL and rshell

Details
-------
::

    CTRL-A        -- on a blank line, enter raw REPL mode
    CTRL-B        -- on a blank line, enter normal REPL mode
    CTRL-C        -- interrupt a running program
    CTRL-D        -- on a blank line, do a soft reset of the board
    CTRL-E        -- on a blank line, enter paste mode
    CTRL-F        -- on a blank line, do a hard reset of the board and enter safe boot


rshell
======
::

    make rshell
    cd /flash
    ls

::

    rshell --port /dev/tty.usbmodemPye090a1 rsync . /flash

::

    make rshell

    ~/hiveeyes-micropython-firmware> boards
    pyboard @ pyboard connected Epoch: 1970 Dirs: /flash /pyboard/flash
    took 0.001 seconds

::

    ~/hiveeyes-micropython-firmware> ls /flash/lib
    mqtt.py   urllib.py


Upload MicroPython firmware
===========================
::

    make sync-all
    took 40.170 seconds


****************
Firmware upgrade
****************

Pycom Upgrader application
==========================
Install the Pycom Upgrader application for your platform.
See also:

- https://pycom.io/downloads/
- https://docs.pycom.io/gettingstarted/installation/firmwaretool.html

.. todo:: Add command for ArchLinux et al.

Prepare
=======

Conveniency::

    alias pycom-fwtool-cli='/Applications/Pycom\ Firmware\ Update.app/Contents/Resources/pycom-fwtool-cli'

Check board connectivity::

    pycom-fwtool-cli list
    /dev/cu.usbmodemPye090a1  [Expansion3] [USB VID:PID=04D8:EF98 SER=Pye090a1 LOCATION=20-2]

Acquire recent firmware binaries::

    # https://software.pycom.io/downloads/FiPy.html
    wget https://software.pycom.io/downloads/FiPy-1.20.0.rc7.tar.gz

Flash firmware
==============
See also: https://docs.pycom.io/advance/downgrade.html

1. Get device into programming mode by holding down the button while powering the device.
2. Upload firmware::

    pycom-fwtool-cli --verbose --port /dev/tty.usbmodemPye090a1 flash --tar FiPy-1.20.0.rc7.tar.gz

3. Power-cycle the device

4. Connect to REPL shell on device::

    make repl
    PyomMiroPython 1.20.0.rc7 [v1.9.4-2833cf5] on 2019-02-08; FiPy with ESP32

    # General help
    >>> help()

    # List built-in modules
    >>> help('modules')


*******
Credits
*******
- micropython-lib
- Microhomie
