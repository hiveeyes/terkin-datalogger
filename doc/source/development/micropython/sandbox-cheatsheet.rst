####################################
Terkin Datalogger sandbox cheatsheet
####################################


***************
Setup your mind
***************
Be prepared to put ``make recycle``, ``CTRL+C``, ``CTRL+D``
and ``CTRL+X`` into your muscle memory. Otherwise, let's go shopping.


****************
Control commands
****************

Reset the device
================
::

    make reset-device


Format ``/flash``
=================
This will re-format the ``/flash`` filesystem using LittleFS.

.. attention::

    This will destroy all data on the ``/flash`` filesystem of the device.
    You have been warned!

::

    make format-flash


************
Control keys
************

The most popular ones
=====================
::

    CTRL-D: Invoke soft reboot
    CTRL-X: Exit REPL and rshell

The whole story
===============
::

    CTRL-A        -- on a blank line, enter raw REPL mode
    CTRL-B        -- on a blank line, enter normal REPL mode
    CTRL-C        -- interrupt a running program
    CTRL-D        -- on a blank line, do a soft reset of the board
    CTRL-E        -- on a blank line, enter paste mode
    CTRL-F        -- on a blank line, do a hard reset of the board and enter safe boot


**********
The rshell
**********

Access command shell
====================
::

    make rshell

::

    > help

    Documented commands (type help <topic>):
    ========================================
    args    cat  connect  echo  exit      filetype  ls     repl  rsync
    boards  cd   cp       edit  filesize  help      mkdir  rm    shell

    Use Control-D (or the exit command) to exit rshell.


Inspect device filesystem
=========================
::

    make rshell
    cd /flash
    ls


********
The REPL
********

Access REPL shell
=================
Connect to the REPL shell on the device::

    make repl
    Pycom MicroPython 1.20.0.rc11 [v1.9.4-0a38f88] on 2019-05-14; FiPy with ESP32

    # General help
    >>> help()

    # List built-in modules
    >>> help('modules')
