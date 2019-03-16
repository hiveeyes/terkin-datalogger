::

    $ time make recycle
    .venv3/bin/rshell --port /dev/tty.usbmodemPye090a1 --buffer-size 2048 --timing --file tools/upload-requirements.rshell
    Using buffer-size of 2048
    Connecting to /dev/tty.usbmodemPye090a1 (buffer-size 2048)...
    Testing if ubinascii.unhexlify exists ... Y
    Retrieving root directories ... /flash/
    Setting time ... Mar 07, 2019 03:49:38
    Evaluating board_name ... pyboard
    Retrieving time epoch ... Jan 01, 1970
    Unable to create /flash/lib/terkin
    took 0.531 seconds
    took 12.812 seconds
    Unable to create /flash/lib/hiveeyes
    took 0.533 seconds
    took 3.463 seconds
    Unable to create /flash/dist-packages
    took 0.522 seconds
    took 6.568 seconds
    .venv3/bin/rshell --port /dev/tty.usbmodemPye090a1 --buffer-size 2048 --timing --file tools/upload-sketch.rshell
    Using buffer-size of 2048
    Connecting to /dev/tty.usbmodemPye090a1 (buffer-size 2048)...
    Testing if ubinascii.unhexlify exists ... Y
    Retrieving root directories ... /flash/
    Setting time ... Mar 07, 2019 03:50:05
    Evaluating board_name ... pyboard
    Retrieving time epoch ... Jan 01, 1970
    took 3.674 seconds
    took 1.850 seconds
    took 2.018 seconds
    took 1.839 seconds
    Entering REPL. Use Control-X to exit.
    >
    ycom MicroPython 1.20.0.rc7 [v1.9.4-2833cf5] on 2019-02-08; FiPy with ESP32
    Type "help()" for more information.
    >>>
    >>> import machine
    >>> took 1.124 seconds
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
    Initializing filesystem as FatFS!
    INFO: Python module search path is: ['', '/flash', '/flash/lib', 'dist-packages']
    ================================
    BOB MicroPython Datalogger 0.0.0
    ================================
    CPU freq     160.0 MHz
    Device id    807d3ac342bc

    ---------------------------------------------
    System memory info (in bytes)
    ---------------------------------------------
    MPTask stack water mark: 6276
    ServersTask stack water mark: 3204
    LoRaTask stack water mark: 3540
    SigfoxTask stack water mark: 2936
    TimerTask stack water mark: 2008
    IdleTask stack water mark: 592
    System free heap: 333344
    ---------------------------------------------

    lorawan:  1.0.2
    machine:  FiPy with ESP32
    nodename: FiPy
    release:  1.20.0.rc7
    sigfox :  1.0.1
    sysname:  FiPy
    version:  v1.9.4-2833cf5 on 2019-02-08

    [0.06617132] Starting networking
    WiFi STA: Starting connection
    WiFi STA: Connecting to network "BKA Ueberwachungswagen"
    WiFi STA: Succeeded
    Networking status: mac=(sta_mac=b'\x80}:\xc3B\xbc', ap_mac=b'\x80}:\xc3B\xbd'), ifconfig=('192.168.178.172', '255.255.255.0', '192.168.178.1', '192.168.178.1'), status=None
    Networking established
    [6.812766] Starting telemetry
    WARNING: libpcre is not available on this platform. TelemetryClient will talk MQTT only.
    Telemetry channel URI:  mqtt://swarm.hiveeyes.org/hiveeyes/testdrive/area-23/node-1
    Starting Terkin TelemetryClient
    [10.68297] Registering Terkin sensors
    [10.68667] Registering Hiveeyes sensors
    [10.69024] Registering BOB sensors

    [10.69405] BOB loop
    [10.69685] Terkin mainloop
    Reading sensor "DummySensor"
    Telemetry transport: MQTT over TCP over WiFi
    MQTT topic:   hiveeyes/testdrive/irgendwas/baz/data.json
    MQTT payload: {"humidity": 83, "temperature": 42.84}
    [11.58851] Telemetry data successfully transmitted

    [12.59279] BOB loop
    [12.59646] Terkin mainloop
    Reading sensor "DummySensor"
    MQTT topic:   hiveeyes/testdrive/irgendwas/baz/data.json
    MQTT payload: {"humidity": 83, "temperature": 42.84}
    [12.61107] Telemetry data successfully transmitted

    [13.61602] BOB loop
    [13.61977] Terkin mainloop
    Reading sensor "DummySensor"
    MQTT topic:   hiveeyes/testdrive/irgendwas/baz/data.json
    MQTT payload: {"humidity": 83, "temperature": 42.84}
    [13.63415] Telemetry data successfully transmitted
    Traceback (most recent call last):
      File "main.py", line 58, in <module>
      File "main.py", line 53, in main
      File "/flash/lib/terkin/datalogger.py", line 36, in start
      File "/flash/lib/terkin/datalogger.py", line 50, in _mainloop
    KeyboardInterrupt:

    took 26.421 seconds

    real	1m6.792s
    user	0m0.716s
    sys	    0m0.210s
