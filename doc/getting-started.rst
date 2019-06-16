########################################################
Getting started with the Hiveeyes MicroPython Datalogger
########################################################

.. note::

    Please recognize this is a work in progress. While many things are
    working already, some places might just have been sketched out.
    So, this firmware will be extended over time - you are dearly welcome
    to help closing some gaps.

.. note::

    Todo: Fold and/or refactor parts of ``README.rst``, ``setup.rst``, ``pycom-getting-started.rst``
    and ``pycom-firmware-upgrade.rst`` into this document or link appropriately.


********
Unboxing
********
Check that's everything with your kit that
will be needed to assemble it successfully.

You will make it.


*************
Setup sandbox
*************

As a general introduction, you might want to read the `Pycom Quickstart Guide`_.

- When you are running Linux, the documentation at ``doc/setup-sandbox.rst``
  might be the right place to follow up for details.
- If you are using Windows, the documentation about how to
  `Install and configure the Hiveeyes Datalogger development sandbox on Windows`_
  might be of interest.


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


.. _Pycom Quickstart Guide: https://github.com/pycom/pycom-micropython-sigfox/blob/master/docs/pycom_esp32/getstarted.rst
.. _Install and configure the Hiveeyes Datalogger development sandbox on Windows: https://community.hiveeyes.org/t/einrichten-der-micropython-firmware-unter-win10/2110
.. _upgrade the Pycom firmware: https://github.com/hiveeyes/hiveeyes-micropython-firmware/blob/master/doc/pycom-firmware-upgrade.rst
.. _Filesystem corruption on FiPy's FatFS in brownout conditions: https://community.hiveeyes.org/t/fipy-verliert-programm-nach-power-off-durch-leeren-lipo-vermutlich-brownout-filesystem-corruption/2057
.. _create an issue: https://github.com/hiveeyes/hiveeyes-micropython-firmware/issues/new
