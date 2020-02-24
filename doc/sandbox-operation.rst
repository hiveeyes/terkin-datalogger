#####################################
Operate the Terkin Datalogger sandbox
#####################################


**************
Prepare device
**************

Upgrade firmware
================
Before uploading the user-space MicroPython program, please `upgrade the Pycom firmware`_
on your device. At the time of this writing, we are running
``Pycom MicroPython 1.20.0.rc11`` on the FiPy without any flaws yet.

Switch to LittleFS
==================
LittleFS should be favored over FatFS to prevent
filesystem corruption in brownout conditions.

.. attention::

    **When switching between LittleFS and FatFS, the flash file system
    will be re-formatted thus erasing all content.**

Switch to LittleFS::

    import pycom
    pycom.bootmgr(fs_type=pycom.LittleFS, reset=True)

Background information:

    The option to use LittleFS instead of FAT as the primary filesystem of the internal flash
    will prevent data corruption even in the case of power loss during write operations.

    -- See also `Filesystem corruption on FiPy's FatFS in brownout conditions`_


**************
Upload program
**************
There are different commands to upload all files from the current working tree
to the MicroPython device. After that, some of them will conveniently reset the
device by software (cold start), which essentially will run your program from
scratch as it will likewise happen in the real world.

After resetting the device, they will drop you into the program execution flow
through a REPL shell. Use ``CTRL+C`` to interrupt the program and ``CTRL+X``
to detach from the REPL environment.


Configure serial port
=====================
After connecting the device to your USB port, you should tell the sandbox
about the UART device the MicroPython MCU is now connected to.
Running ``make list-serials`` might help here.

Example::

    export MCU_PORT=/dev/cu.usbmodemPye090a1


From scratch
============
When starting from scratch, these guys will upload the whole bunch of dependency
modules, datalogger framework and sketch to the device.

::

    # Get most recent development sources
    git pull

    # Setup the sandbox environment on your workstation
    make setup

    # Upload framework and datalogger to the device
    make install

    # Upload program sketch and invoke hard reset.
    # This just uploads "boot.py", "main.py" and "settings.py".
    make sketch-and-run

When updating
=============
For updating the firmware to the current development head, these steps
should bring you up to speed.

::

    # Get most recent development sources.
    git pull

    # Upload framework and sketch and invoke hard reset.
    make recycle

Caveats
=======
Framework dependencies are occasionally updated and extended. In this
case, it is appropriate to run the "from scratch" procedure again.

You will most probably recognize this through any error messages
signalling missing package or module dependencies.

If you are having problems updating your device, feel free to `create an issue`_.

Sometimes, you want to erase the filesystem on flash memory holding
the program in order to completely start over from scratch. There's
a shortcut for that::

    make format-flash

AS THIS IS A DESTRUCTIVE OPERATION, THERE'S A CONFIRMATION PROMPT PROTECTING
YOURSELF FROM ACCIDENTALLY DESTROYING DATA. REMEMBER: ALL YOUR DATA WILL BE LOST.


*************
More commands
*************

Attach to serial console
========================
In order to connect to a device which is already running, just execute::

    make console

To detach from the ``miniterm`` environment, just type ``CTRL+]``.

Reset the device
================
In order to run a ``machine.reset()`` on the device, just execute::

    make reset-device

Toggle between maintenance and field mode
=========================================
When the device is pulled into maintenance mode, deep sleep is disabled and
the measurement interval will be decreased to 5 seconds.

Install prerequisites::

    pip install scapy netifaces netaddr

Monitor local networks for devices::

    sudo python3 -m tools.terkin monitor

Enable maintenance mode::

    sudo python3 -m tools.terkin maintain

Release maintenance mode and enable field mode again::

    sudo python3 -m tools.terkin field

In order to restrict these operations to a single device on the network,
you should invoke the program like::

    sudo python3 -m tools.terkin maintain 80:7d:3a:c2:de:44

By default, the list of MAC address prefixes are::

    mac_prefixes_default = [
        # WiPy
        '30:ae:a4',
        # FiPy
        '80:7d:3a'
    ]

Essentially, we would like to be able to match all Espressif/Pycom devices.


***************
Troubleshooting
***************
We have collected some tracebacks with root causes and solutions which might also help
you along, please have a look at `Terkin Datalogger troubleshooting`_.



.. _upgrade the Pycom firmware: https://github.com/hiveeyes/terkin-datalogger/blob/master/doc/pycom-firmware-upgrade.rst
.. _Filesystem corruption on FiPy's FatFS in brownout conditions: https://community.hiveeyes.org/t/fipy-verliert-programm-nach-power-off-durch-leeren-lipo-vermutlich-brownout-filesystem-corruption/2057
.. _Terkin Datalogger troubleshooting: https://github.com/hiveeyes/terkin-datalogger/blob/master/doc/troubleshooting.rst
.. _create an issue: https://github.com/hiveeyes/terkin-datalogger/issues/new
