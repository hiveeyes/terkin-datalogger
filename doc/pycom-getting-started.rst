############################
Pycom MicroPython cheatsheet
############################


****************
Control commands
****************


The most popular ones
=====================
::

    CTRL-D: PYB: soft reboot
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


******
rshell
******
Inspect the filesystem on the device::

    make rshell
    cd /flash
    ls

Check board connectivity::

    make rshell

    ~/hiveeyes-micropython-firmware> boards
    pyboard @ pyboard connected Epoch: 1970 Dirs: /flash /pyboard/flash
    took 0.001 seconds
