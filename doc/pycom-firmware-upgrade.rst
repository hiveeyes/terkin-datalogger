######################
Pycom firmware upgrade
######################


Pycom Updater application
=========================
Install the Pycom Updater application for your platform.
See also:

- https://pycom.io/downloads/
- https://docs.pycom.io/gettingstarted/installation/firmwaretool.html
- https://github.com/pycom/pycom-documentation/blob/master/advanced-topics/cli.md

.. todo: Add command for ArchLinux et al.

Prepare
=======
We will be using the CLI Updater Command Line Update Utility here.

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
    Pycom MicroPython 1.20.0.rc7 [v1.9.4-2833cf5] on 2019-02-08; FiPy with ESP32

    # General help
    >>> help()

    # List built-in modules
    >>> help('modules')
