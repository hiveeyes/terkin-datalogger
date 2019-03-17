::

    Initializing filesystem as FatFS!
    [boot.py] INFO: Python module search path is: ['', '/flash', '/flash/lib', 'dist-packages']

    INFO: Configuration
    Printing configuration settings currently defunct, sorry.
    ================================
    BOB MicroPython Datalogger 0.1.0
    ================================
    CPU freq     160.0 MHz
    Device id    807d3ac342bc

    ---------------------------------------------
    System memory info (in bytes)
    ---------------------------------------------
    MPTask stack water mark: 7012
    ServersTask stack water mark: 3204
    LoRaTask stack water mark: 3516
    SigfoxTask stack water mark: 2936
    TimerTask stack water mark: 2008
    IdleTask stack water mark: 592
    System free heap: 333360
    ---------------------------------------------

    Python  : 3.4.0
    lorawan : 1.0.2
    machine : FiPy with ESP32
    nodename: FiPy
    release : 1.20.0.rc7
    sigfox  : 1.0.1
    sysname : FiPy
    version : v1.9.4-2833cf5 on 2019-02-08

    [0.07144903] Starting networking
    [LoRa] Disabling LoRa interface as no antenna has been attached. ATTENTION: Running LoRa without antenna will wreck your device.
    WiFi STA: Starting connection
    WiFi STA: Scanning for networks
    WiFi STA: Available networks: frozenset({'KabelBox-0AF0', 'Vodafone Homespot', 'WLAN-MP9KW6', 'Leonardo', 'hausbuch', 'GartenNetzwerk', 'FRITZ!Box 7560 UH', 'FRITZ!Box Fon WLAN 7170', 'BKA Ueberwachungswagen', 'FRITZ!Box 6490 Cable 2.4G', 'DIRECT-oe-BRAVIA', 'FRITZ!Box 6490 Cable', 'Vodafone Hotspot', 'zrwguests', 'KabelBox-0288', 'Leonardo2', 'Vodafone-7982', 'HITRON-9A60', 'FRITZ!Box Fon WLAN 7360'})
    WiFi STA: Attempting to connect to network "GartenNetzwerk"
    WiFi STA: Connecting to "GartenNetzwerk"
    WiFi STA: Waiting for network "GartenNetzwerk".
    WiFi STA: Waiting for network "GartenNetzwerk".
    WiFi STA: Waiting for network "GartenNetzwerk".
    WiFi STA: Waiting for network "GartenNetzwerk".
    WiFi STA: Connected to "GartenNetzwerk" with IP address "192.168.178.55"
    WiFi STA: Networking address: mac=(sta_mac=b'\x80}:\xc3B\xbc', ap_mac=b'\x80}:\xc3B\xbd'), ifconfig=('192.168.178.55', '255.255.255.0', '192.168.178.1', '192.168.178.1')
    Networking established
    [7.735586] Starting telemetry
    Telemetry channel URI:  mqtt://weather.hiveeyes.org/workbench/testdrive/area-38/fipy-amo-02-mqtt-json
    Starting Terkin TelemetryClient
    Telemetry channel URI:  mqtt://weather.hiveeyes.org/workbench/testdrive/area-38/fipy-amo-02-mqtt-lpp
    Starting Terkin TelemetryClient
    WARNING: No telemetry target configured.
    [13.2994] Registering Terkin sensors
    [13.3044] Registering Hiveeyes sensors
    INFO:  Initializing HX711 sensor with DOUT=P0, PD_SCK=P2, GAIN=None, scale=11.02667, offset=130800.0
    INFO:  Selected HX711 hardware driver "heisenberg"
    INFO:  HX711 initialization started
    ERROR: HX711 not found, skipping initialization
    ERROR: HX711 hardware driver failed. HX711 not available
    INFO:  Skipping HX711 sensor. HX711 not available
    --- loop ---
    [13.8672] Terkin loop
    INFO:  Reading sensor "MemoryFree"
    Telemetry transport: MQTT over TCP over WiFi
    DEBUG: MQTT topic:   workbench/testdrive/area-38/fipy-amo-02-mqtt-json/data.json
    DEBUG: MQTT payload: {"memfree": 2367776}
    INFO: Connecting to MQTT broker
    INFO: Connecting to MQTT broker at ('46.4.251.67', 1883) succeeded
    Telemetry transport: MQTT over TCP over WiFi
    [CayenneLPP] Sensor type "memfree" not found in CayenneLPP
    DEBUG: MQTT topic:   workbench/testdrive/area-38/fipy-amo-02-mqtt-lpp/data.lpp
    DEBUG: MQTT payload:
    [19.05333] Telemetry transmission: SUCCESS
    --- loop ---
    [20.15762] Terkin loop
    INFO:  Reading sensor "MemoryFree"
    DEBUG: MQTT topic:   workbench/testdrive/area-38/fipy-amo-02-mqtt-json/data.json
    DEBUG: MQTT payload: {"memfree": 2430064}
    [CayenneLPP] Sensor type "memfree" not found in CayenneLPP
    DEBUG: MQTT topic:   workbench/testdrive/area-38/fipy-amo-02-mqtt-lpp/data.lpp
    DEBUG: MQTT payload:
    [20.47757] Telemetry transmission: SUCCESS
    --- loop ---
    [21.58159] Terkin loop
    INFO:  Reading sensor "MemoryFree"
    DEBUG: MQTT topic:   workbench/testdrive/area-38/fipy-amo-02-mqtt-json/data.json
    DEBUG: MQTT payload: {"memfree": 2430096}
    [CayenneLPP] Sensor type "memfree" not found in CayenneLPP
    DEBUG: MQTT topic:   workbench/testdrive/area-38/fipy-amo-02-mqtt-lpp/data.lpp
    DEBUG: MQTT payload:
    [21.91398] Telemetry transmission: SUCCESS
