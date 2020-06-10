:orphan:

.. _pycom-firmware-upgrade:

######################
Pycom firmware upgrade
######################


************
Introduction
************
As the Pycom firmware is continuously evolving, you might
also like to run their most recent release on your device.

.. note::

    Please take into consideration that we are outlining our best practices here.

    - We always try to run the most recent release available
      either from the Pycom firmware download page or firmware
      images we are creating ourselves.

    - Saying that, you must not hold us accountable for anything that might go
      wrong with your device in any way when following these recommendations.
      There's always a chance that things might go south.

    - At the time of this writing, we are running
      ``Pycom MicroPython 1.20.2.rc6`` successfully on the FiPy.

    - When upgrading, please use the ``LittleFS`` filesystem to prevent
      filesystem corruption in brownout conditions.

.. seealso::

    - https://community.hiveeyes.org/t/squirrel-firmware-for-pycom-esp32/2960
    - https://packages.hiveeyes.org/hiveeyes/foss/pycom/vanilla/


*************
Prerequisites
*************
::

    apt-get install git
    git clone https://github.com/hiveeyes/terkin-datalogger.git
    cd terkin-datalogger

.. attention::

    Please make sure to backup the configuration file ``settings.py`` before.


*************
In a nutshell
*************
Install recent firmware image::

    # Investigate and define serial port.
    make list-serials
    export MCU_PORT=/dev/cu.usbmodemPy001711    # libero

    # Erase device completely.
    # !!! ATTENTION: This will purge all files from the device !!!
    make erase-device

    # Download and install most recent firmware for FiPy.
    export MCU_DEVICE=FiPy
    make install-pycom-firmware

Install specific firmware image::

    make install-pycom-firmware pycom_firmware_file=FiPy-1.20.2.rc6-0.10.1-vanilla-squirrel.tar.gz
