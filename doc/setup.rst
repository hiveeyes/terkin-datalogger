#####################################
Hiveeyes MicroPython Datalogger setup
#####################################

************
Introduction
************
You mean it. Thanks for listening already and enjoy the ride.

This part of the documentation covers the installation of the
MicroPython firmware development environment and other software
components it relies on.

The first step to using any software package is getting it
properly installed. Please read this section carefully.

*****
Setup
*****

Prerequisites
=============
To perform the next steps, you might want to install Python2,
Python3, the corresponding Python virtualenv packages as well
as MicroPython for Unix on your workstation. YMMV.

Setup development sandbox
=========================
This will install different tools into the local directory which we
consider essentially for efficient MicroPython development.
The programming environment driven through different ``make`` targets
and the accompanying documentation is based on a successful installation
of these tools.
::

    make setup

Independently from running this command once, you might want to install or update
the MicroPython module dependencies through populating the ``dist-packages`` folder::

    make install-requirements


Pre-flight checks
=================
Check serial interface connectivity::

    make list-serials

::

    USB Serial Device 04d8:ef98 with vendor 'Pycom' serial 'Pye090a1' found @/dev/cu.usbmodemPye090a1


*******************
Board configuration
*******************

Configuration
=============
Please adjust the serial port in ``config.mk``, use output from
``make list-serials`` above, here ``/dev/cu.usbmodemPye090a1``.

Pre-flight checks
=================
Check board connectivity::

    make list-boards

::

    pyboard @ pyboard connected Epoch: 1970 Dirs: /flash /pyboard/flash

Connect to the REPL shell on the device::

    make repl
    Pycom MicroPython 1.18.2.r3 [v1.8.6-849-a1641ca] on 2019-02-28; FiPy with ESP32

    # General help
    >>> help()

    # List built-in modules
    >>> help('modules')

MicroPython control commands
============================
At this point, you should take a minute to have a look at
`getting started with Pycom MicroPython`_. It will be worth it as it will walk
you through essential function keys you will need after taking the red pill.
