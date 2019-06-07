::

    Initializing filesystem as FatFS!
    [boot.py] INFO: Python module search path is: ['', '/flash', '/flash/lib', 'dist-packages']

        4.3814 [terkin.configuration     ] INFO   : Configuration settings:
        4.3940 [terkin.configuration     ] INFO   : Section "telemetry": {"targets": [{"address": {"node": "fipy-amo-04", "gateway": "area-38", "realm": "hiveeyes", "network": "testdrive"}, "enabled": true, "endpoint": "mqtt://swarm.hiveeyes.org"}, {"address": {"node": "fipy-amo-04", "gateway": "area-38", "realm": "workbench", "network": "testdrive"}, "enabled": true, "endpoint": "mqtt://weather.hiveeyes.org"}, {"address": {"node": "fipy-amo-02-http-json", "gateway": "area-38", "realm": "workbench", "network": "testdrive"}, "enabled": false, "endpoint": "https://weather.hiveeyes.org/api"}, {"endpoint": "mqtt://weather.hiveeyes.org", "encode": "base64", "enabled": false, "address": {"node": "fipy-amo-02-mqtt-lpp", "gateway": "area-38", "realm": "workbench", "network": "testdrive"}, "format": "lpp"}]}
        4.4652 [terkin.configuration     ] INFO   : Section "sensors": {"registry": {"ds18x20": {"bus": "onewire:0"}, "bme280": {"address": 119, "bus": "i2c:0"}, "hx711": {"offset": -73000.0, "scale": 4.424242, "pin_pdsck": "P21", "pin_dout": "P22"}}, "busses": [{"pin_scl": "P10", "number": 0, "enabled": true, "family": "i2c", "pin_sda": "P9"}, {"enabled": true, "pin_data": "P11", "number": 0, "family": "onewire"}]}
        4.5007 [terkin.configuration     ] INFO   : Section "main": {"interval": 1.0}
        4.5124 [terkin.configuration     ] INFO   : Section "networking": {"wifi": {"stations": [{"ssid": "GartenNetzwerk", "password": "{redacted}"}], "timeout": 15000}, "lora": {"otaa": {"region": "LoRa.EU868", "datarate": 5, "frequency": 868100000, "application_key": "{redacted}", "application_eui": "{redacted}"}, "antenna_attached": false}}
        4.5435 [terkin.datalogger        ] INFO   : Starting BOB MicroPython Datalogger 0.2.1
    ---------------------------------------------
    System memory info (in bytes)
    ---------------------------------------------
    MPTask stack water mark: 4516
    ServersTask stack water mark: 3204
    LoRaTask stack water mark: 3436
    SigfoxTask stack water mark: 2936
    TimerTask stack water mark: 2008
    IdleTask stack water mark: 592
    System free heap: 333344
    ---------------------------------------------
        4.7375 [terkin.device            ] INFO   :

    ================================
    BOB MicroPython Datalogger 0.2.1
    ================================
    CPU freq     160.0 MHz
    Device id    807d3ac342bc


    Python  : 3.4.0
    lorawan : 1.0.2
    machine : FiPy with ESP32
    nodename: FiPy
    release : 1.20.0.rc7
    sigfox  : 1.0.1
    sysname : FiPy
    version : v1.9.4-2833cf5 on 2019-02-08



        4.7663 [terkin.device            ] INFO   : Starting networking
        4.8039 [terkin.radio             ] INFO   : WiFi STA: Networks configured: ['GartenNetzwerk']
        4.8122 [terkin.radio             ] INFO   : WiFi STA: Starting interface
        4.8193 [terkin.radio             ] INFO   : WiFi STA: Scanning for networks
        7.3567 [terkin.radio             ] INFO   : WiFi STA: Networks available: ['KabelBox-0AF0', 'KDG-544EA', 'DIRECT-DA-HP ENVY 4520 series', 'Vodafone Homespot', 'WLAN-MP9KW6', 'gigacube-2CFD', 'GartenNetzwerk', 'hausbuch', 'GALAXY_S4_4699', 'FRITZ!Box Fon WLAN 7170', 'BKA Ueberwachungswagen', 'o2-WLAN66', 'DIRECT-oe-BRAVIA', 'FRITZ!Box 6490 Cable', 'Vodafone Hotspot', 'zrwguests', 'KabelBox-4484', 'HITRON-A6E0', 'DIRECT-51-HP OfficeJet 4650']
        7.3926 [terkin.radio             ] INFO   : WiFi STA: Network candidates: ['GartenNetzwerk']
        7.4033 [terkin.radio             ] INFO   : WiFi STA: Attempting to connect to network "GartenNetzwerk"
        7.4132 [terkin.radio             ] INFO   : WiFi STA: Connecting to "GartenNetzwerk"
        7.4306 [terkin.radio             ] INFO   : WiFi STA: Waiting for network "GartenNetzwerk".
        8.4402 [terkin.radio             ] INFO   : WiFi STA: Waiting for network "GartenNetzwerk".
        9.4517 [terkin.radio             ] INFO   : WiFi STA: Waiting for network "GartenNetzwerk".
       10.4615 [terkin.radio             ] INFO   : WiFi STA: Waiting for network "GartenNetzwerk".
       11.4784 [terkin.radio             ] INFO   : WiFi STA: Connected to "GartenNetzwerk" with IP address "192.168.178.146"
       11.4943 [terkin.radio             ] INFO   : WiFi STA: Networking address: mac=(sta_mac=b'\x80}:\xc3B\xbc', ap_mac=b'\x80}:\xc3B\xbd'), ifconfig=('192.168.178.146', '255.255.255.0', '192.168.178.1', '192.168.178.1')
       11.5105 [terkin.radio             ] INFO   : Network interface ready
       11.5231 [terkin.device            ] INFO   : [LoRa] Disabling LoRa interface as no antenna has been attached. ATTENTION: Running LoRa without antenna will wreck your device.
       11.5342 [terkin.device            ] INFO   : Starting telemetry
       17.6296 [terkin.telemetry         ] INFO   : Telemetry channel URI: mqtt://swarm.hiveeyes.org/hiveeyes/testdrive/area-38/fipy-amo-04
       17.6391 [terkin.telemetry         ] INFO   : Starting Terkin TelemetryClient
       17.6676 [terkin.telemetry         ] INFO   : Telemetry channel URI: mqtt://weather.hiveeyes.org/workbench/testdrive/area-38/fipy-amo-04
       17.6774 [terkin.telemetry         ] INFO   : Starting Terkin TelemetryClient
       17.7044 [terkin.datalogger        ] INFO   : Starting all busses [{'pin_scl': 'P10', 'number': 0, 'enabled': True, 'family': 'i2c', 'pin_sda': 'P9'}, {'enabled': True, 'pin_data': 'P11', 'number': 0, 'family': 'onewire'}]
       17.7497 [terkin.sensor            ] INFO   : Found 1 I2C devices: [119].
       17.7605 [terkin.sensor            ] INFO   : Registering bus "i2c:0"
       19.5470 [terkin.sensor            ] INFO   : Found 2 OneWire (DS18x20) devices: [b'28ff641d8fdf18c1', b'28ff641d8fc3944f'].
       19.5587 [terkin.sensor            ] INFO   : Registering bus "onewire:0"
       19.5691 [terkin.datalogger        ] INFO   : Registering Terkin sensors
       19.5781 [hiveeyes.datalogger      ] INFO   : Registering Hiveeyes sensors
       20.2531 [hiveeyes.sensor_hx711    ] INFO   : Selected HX711 hardware driver "heisenberg"
       20.2697 [hiveeyes.sensor_hx711    ] INFO   : Initializing HX711 sensor with pin_dout=P22, pin_pdsck=P21, gain=128, scale=4.424242, offset=-73000.0
       20.2806 [hx711                    ] INFO   : HX711 initialization started
       20.3826 [hx711                    ] INFO   : HX711 initialization succeeded
       20.6706 [hx711_heisenberg         ] INFO   : Gain & initial value set
       20.6870 [terkin.sensor            ] INFO   : Trying to find bus by name "onewire:0"
       20.6972 [terkin.sensor            ] INFO   : Found bus by name "onewire:0": <OneWireBus object at 3f98bf50>
       20.7684 [terkin.sensor            ] INFO   : Trying to find bus by name "i2c:0"
       20.7777 [terkin.sensor            ] INFO   : Found bus by name "i2c:0": <I2CBus object at 3f98b820>
       20.7968 [terkin.datalogger        ] INFO   : --- loop ---
       20.8085 [terkin.datalogger        ] INFO   : Reading 4 sensor interfaces
       26.2300 [terkin.datalogger        ] INFO   : Sensor data:  {'temperature.0x77.i2c:0': 26.27, 'temperature.28ff641d8fc3944f.onewire:0': 24.5, 'pressure.0x77.i2c:0': 1007.02, 'memfree': 2282096, 'temperature.28ff641d8fdf18c1.onewire:0': 25.5, 'humidity.0x77.i2c:0': 38.24, 'weight': 85691.82}
       26.2592 [terkin.telemetry         ] INFO   : Telemetry transport: MQTT over TCP over WiFi
       26.4068 [terkin.telemetry         ] INFO   : Starting connection to MQTT broker. client_id=terkin.807d3ac342bc, netloc=swarm.hiveeyes.org
       27.1044 [terkin.telemetry         ] INFO   : Connecting to MQTT broker at swarm.hiveeyes.org
       27.5490 [terkin.telemetry         ] INFO   : Connecting to MQTT broker at ('46.4.251.66', 1883) succeeded
       27.6770 [terkin.telemetry         ] INFO   : Telemetry transport: MQTT over TCP over WiFi
       27.8251 [terkin.telemetry         ] INFO   : Starting connection to MQTT broker. client_id=terkin.807d3ac342bc, netloc=weather.hiveeyes.org
       27.8408 [terkin.telemetry         ] INFO   : Connecting to MQTT broker at weather.hiveeyes.org
       27.9661 [terkin.telemetry         ] INFO   : Connecting to MQTT broker at ('46.4.251.67', 1883) succeeded
       28.0859 [terkin.datalogger        ] INFO   : Telemetry status: SUCCESS
       29.2425 [terkin.datalogger        ] INFO   : --- loop ---
       29.2525 [terkin.datalogger        ] INFO   : Reading 4 sensor interfaces
       34.6759 [terkin.datalogger        ] INFO   : Sensor data:  {'temperature.0x77.i2c:0': 25.79, 'temperature.28ff641d8fc3944f.onewire:0': 24.5, 'pressure.0x77.i2c:0': 1007.14, 'memfree': 2423264, 'temperature.28ff641d8fdf18c1.onewire:0': 25.5, 'humidity.0x77.i2c:0': 38.5, 'weight': 85850.17}
       34.9332 [terkin.datalogger        ] INFO   : Telemetry status: SUCCESS
       36.0884 [terkin.datalogger        ] INFO   : --- loop ---
       36.0981 [terkin.datalogger        ] INFO   : Reading 4 sensor interfaces
       41.4930 [terkin.datalogger        ] INFO   : Sensor data:  {'temperature.0x77.i2c:0': 25.75, 'temperature.28ff641d8fc3944f.onewire:0': 24.5, 'pressure.0x77.i2c:0': 1007.11, 'memfree': 2422640, 'temperature.28ff641d8fdf18c1.onewire:0': 25.5, 'humidity.0x77.i2c:0': 38.59, 'weight': 85869.0}
       41.7527 [terkin.datalogger        ] INFO   : Telemetry status: SUCCESS
       42.9075 [terkin.datalogger        ] INFO   : --- loop ---
       42.9180 [terkin.datalogger        ] INFO   : Reading 4 sensor interfaces
       48.3024 [terkin.datalogger        ] INFO   : Sensor data:  {'temperature.0x77.i2c:0': 25.73, 'temperature.28ff641d8fc3944f.onewire:0': 24.5, 'pressure.0x77.i2c:0': 1007.11, 'memfree': 2422640, 'temperature.28ff641d8fdf18c1.onewire:0': 25.5, 'humidity.0x77.i2c:0': 38.63, 'weight': 85842.0}
       48.5849 [terkin.datalogger        ] INFO   : Telemetry status: SUCCESS
