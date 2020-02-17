##########################################
Getting started with the Terkin Datalogger
##########################################

.. note::

    Please recognize this is a work in progress. While many things are
    working already, some places might just have been sketched out.
    So, this firmware will be extended over time - you are dearly welcome
    to help closing some gaps.


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

- When you are running Linux, the documentation at ``doc/sandbox-setup.rst``
  might be the right place to follow up for details.
- If you are using Windows, the documentation about how to
  `Install and configure the Terkin Datalogger development sandbox on Windows`_
  might be of interest.


**************
Prepare device
**************

Upgrade firmware
================
Before uploading the user-space MicroPython program, please upgrade the Pycom firmware
on your device. At the time of this writing, we are running
``Pycom MicroPython 1.20.0.rc11`` successfully on the FiPy.

When upgrading, please use the ``LittleFS`` filesystem to prevent filesystem corruption
in brownout conditions.


.. _Pycom Quickstart Guide: https://github.com/pycom/pycom-micropython-sigfox/blob/master/docs/pycom_esp32/getstarted.rst
.. _Install and configure the Terkin Datalogger development sandbox on Windows: https://community.hiveeyes.org/t/einrichten-der-micropython-firmware-unter-win10/2110



*******************
Appendix: Resources
*******************
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



.. _General information about the WiPy: https://docs.micropython.org/en/latest/wipy/general.html
.. _MicroPython documentation: https://micropython.readthedocs.io/
.. _MicroPython libraries: https://micropython.readthedocs.io/en/latest/library/
.. _Pycom MicroPython Modules: https://github.com/pycom/pydocs/tree/master/firmwareapi/micropython
.. _Pycom Vendor Modules: https://github.com/pycom/pydocs/tree/master/firmwareapi/pycom
.. _Pycom documentation: https://docs.pycom.io/
.. _Getting started with Pycom MicroPython: https://github.com/hiveeyes/terkin-datalogger/blob/master/doc/pycom-getting-started.rst

.. _Pycom MicroPython for ESP32: https://github.com/pycom/pycom-micropython-sigfox
.. _Pycom Libraries and Examples: https://github.com/pycom/pycom-libraries

.. _Quick reference for the ESP32: https://docs.micropython.org/en/latest/esp32/quickref.html
.. _ESP32 Datasheet: https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf
