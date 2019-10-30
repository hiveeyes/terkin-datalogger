::

    $ time make recycle
    .venv3/bin/rshell --port /dev/cu.usbmodemPye090a1 --buffer-size 2048 --timing --file tools/upload-requirements.rshell
    Using buffer-size of 2048
    Connecting to /dev/cu.usbmodemPye090a1 (buffer-size 2048)...
    Testing if ubinascii.unhexlify exists ... Y
    Retrieving root directories ... /flash/
    Setting time ... Mar 17, 2019 12:36:03
    Evaluating board_name ... pyboard
    Retrieving time epoch ... Jan 01, 1970
    Unable to create /flash/lib/terkin
    took 0.539 seconds
    took 20.476 seconds
    .venv3/bin/rshell --port /dev/cu.usbmodemPye090a1 --buffer-size 2048 --timing --file tools/upload-sketch.rshell
    Using buffer-size of 2048
    Connecting to /dev/cu.usbmodemPye090a1 (buffer-size 2048)...
    Testing if ubinascii.unhexlify exists ... Y
    Retrieving root directories ... /flash/
    Setting time ... Mar 17, 2019 12:36:33
    Evaluating board_name ... pyboard
    Retrieving time epoch ... Jan 01, 1970
    took 5.375 seconds
    took 2.160 seconds
    took 2.104 seconds
    took 2.516 seconds
    Entering REPL. Use Control-X to exit.
    >
    Pyco MicroPython 1.20.0.rc7 [v1.9.4-2833cf5] on 2019-02-08; FiPy with ESP32
    Type "help()" for more information.
    >>>
    >>> import machine
    >>> took 1.129 seconds
    Entering REPL. Use Control-X to exit.

    >>> machine.reset()
    ets Jun  8 2016 00:22:57

    rst:0x7 (TG0WDT_SYS_RESET),boot:0x13 (SPI_FAST_FLASH_BOOT)
    configsip: 0, SPIWP:0xee
    clk_drv:0x00,q_drv:0x00,d_drv:0x00,cs0_drv:0x00,hd_drv:0x00,wp_drv:0x00
    mode:DIO, clock div:1
    load:0x3fff8028,len:8
    load:0x3fff8030,len:2064
    load:0x4009fa00,len:0
    load:0x4009fa00,len:19208
    entry 0x400a05f8
