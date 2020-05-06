.. include:: ../_resources.rst


####################
Setup on MicroPython
####################


.. _install-micropython-firmware:

****************
Install firmware
****************

Genuine MicroPython
===================
::

    # Acquire firmware file.
    # http://micropython.org/download/all/
    wget http://micropython.org/resources/firmware/PYBD-SF3-20191220-v1.12.dfu

    # Identify serial number.
    dfu-util --list

    # Install firmware on device.
    dfu-util --serial="355931523037" --download PYBD-SF3-20191220-v1.12.dfu

Pycom MicroPython
=================
See :ref:`pycom-firmware-upgrade`.


**************
Install Terkin
**************

Download release
================
Release artifacts will be published to
https://github.com/hiveeyes/terkin-datalogger/releases.

They are available in three flavors:

- ``terkin-datalogger-x.x.x-source.tar.gz``
  The bare source code.

- ``terkin-datalogger-x.x.x-pycom-mpy-1.11.tar.gz``
  Cross-compiled modules for Pycom MicroPython.

- ``terkin-datalogger-x.x.x-genuine-mpy-1.12.tar.gz``
  Cross-compiled modules for Genuine MicroPython.


Upload to device
================

Genuine MicroPython
===================
The filesystem of the PYBOARD-D device will get mounted
on your workstation. Thus, it is easy to transfer the files.

Pycom MicroPython
=================
The most convenient way to upload the release files to your
device will be by using FTP. We recommend FileZilla_.

.. seealso::

    https://community.hiveeyes.org/t/remote-via-wlan-telnet-ftp-auf-den-wipy-fipy-zugreifen/2124
