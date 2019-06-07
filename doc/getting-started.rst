########################################################
Getting started with the Hiveeyes MicroPython Datalogger
########################################################

.. note::

    Please recognize this is a work in progress. While many things are
    working already, some places might just have been sketched out.
    So, this firmware will be extended over time - you are dearly welcome
    to help closing some gaps.

.. todo::

    Fold and/or refactor parts of README.rst, setup.rst, pycom-getting-started.rst
    and pycom-firmware-upgrade.rst into this document or link appropriately.


********
Unboxing
********
Check that's everything with your kit that
will be needed to assemble it successfully.

You will make it.


*************
Setup sandbox
*************

.. todo:: Refactor from or link to ``setup.rst``.




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

    When switching between LittleFS and FatFS, the flash file system
    will be re-formatted thus erasing all content.

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
::

    # Get most recent development sources
    git pull

    # Setup sandbox environment
    make setup

    # Upload framework and program to device
    make install

    # Upload program sketch and invoke hard reset
    make sketch-and-run



.. _upgrade the Pycom firmware: https://github.com/hiveeyes/hiveeyes-micropython-firmware/blob/master/doc/pycom-firmware-upgrade.rst
.. _Filesystem corruption on FiPy's FatFS in brownout conditions: https://community.hiveeyes.org/t/fipy-verliert-programm-nach-power-off-durch-leeren-lipo-vermutlich-brownout-filesystem-corruption/2057
