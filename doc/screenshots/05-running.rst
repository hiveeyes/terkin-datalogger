###########################################
Running the Hiveeyes MicroPython Datalogger
###########################################

************
Introduction
************
To get a better idea about how running this firmware will feel like
when watching its log output, we regularly update essentials from
different parts of the runtime lifecycle here.

************
Boot process
************
::

    Initializing filesystem as FatFS!
    [boot.py] INFO: Python module search path is: ['', '/flash', '/flash/lib', 'dist-packages']

        4.5007 [terkin.configuration     ] INFO   : Section "main": {"interval": 1.0}
        4.5124 [terkin.configuration     ] INFO   : Configuration settings:
        4.5417 [terkin.configuration     ] INFO   : Section "telemetry": {"targets": [{"enabled": true, "endpoint": "mqtt://swarm.hiveeyes.org", "address": {"network": "testdrive", "gateway": "area-38", "node": "fipy-workbench-01", "realm": "hiveeyes"}}, {"enabled": true, "endpoint": "mqtt://weather.hiveeyes.org", "address": {"network": "testdrive", "gateway": "area-38", "node": "fipy-workbench-01", "realm": "workbench"}}, {"enabled": false, "endpoint": "https://weather.hiveeyes.org/api", "address": {"network": "testdrive", "gateway": "area-38", "node": "fipy-amo-02-http-json", "realm": "workbench"}}, {"encode": "base64", "format": "lpp", "address": {"network": "testdrive", "gateway": "area-38", "node": "fipy-amo-02-mqtt-lpp", "realm": "workbench"}, "enabled": false, "endpoint": "mqtt://weather.hiveeyes.org"}]}
        4.6267 [terkin.configuration     ] INFO   : Section "sensors": {"registry": {"bme280": {"bus": "i2c:0", "address": 119}, "ds18x20": {"bus": "onewire:0"}, "hx711": {"offset": -73000.0, "scale": 4.424242, "pin_pdsck": "P21", "pin_dout": "P22"}}, "busses": [{"number": 0, "family": "i2c", "pin_sda": "P9", "enabled": true, "pin_scl": "P10"}, {"enabled": true, "pin_data": "P11", "number": 0, "family": "onewire"}]}
        4.6876 [terkin.configuration     ] INFO   : Section "networking": {"wifi": {"stations": [{"ssid": "GartenNetzwerk", "password": "## redacted ##"}], "timeout": 15000}, "lora": {"otaa": {"region": "LoRa.EU868", "frequency": 868100000, "application_key": "## redacted ##", "datarate": 5, "application_eui": "## redacted ##"}, "antenna_attached": false}}
        4.7190 [terkin.datalogger        ] INFO   : Starting BOB MicroPython Datalogger 0.3.0
    ---------------------------------------------
    System memory info (in bytes)
    ---------------------------------------------
    MPTask stack water mark: 4516
    ServersTask stack water mark: 3204
    LoRaTask stack water mark: 3432
    SigfoxTask stack water mark: 2928
    TimerTask stack water mark: 2160
    IdleTask stack water mark: 600
    System free heap: 328140
    ---------------------------------------------
        4.9227 [terkin.device            ] INFO   :

    ================================
    BOB MicroPython Datalogger 0.3.0
    ================================
    CPU freq     160.0 MHz
    Device id    807d3ac342bc


    Python  : 3.4.0
    lorawan : 1.0.2
    machine : FiPy with ESP32
    nodename: FiPy
    release : 1.20.0.rc11
    sigfox  : 1.0.1
    sysname : FiPy
    version : v1.9.4-0a38f88 on 2019-05-14



        4.9535 [terkin.device            ] INFO   : Starting networking
        4.9934 [terkin.radio             ] INFO   : WiFi STA: Networks configured: ['GartenNetzwerk']
        5.0037 [terkin.radio             ] INFO   : WiFi STA: Starting interface
        5.0124 [terkin.radio             ] INFO   : WiFi STA: Scanning for networks
        7.5542 [terkin.radio             ] INFO   : WiFi STA: Networks available: ['KabelBox-0AF0', 'KDG-544EA', 'Telekom_FON', 'DIRECT-DA-HP ENVY 4520 series', 'Vodafone Homespot', 'gigacube-2CFD', 'Leonardo', 'GartenNetzwerk', 'hausbuch', 'WLAN-MP9KW6', 'BKA Ueberwachungswagen', 'FRITZ!Box 7430 WP', 'DIRECT-oe-BRAVIA', 'FRITZ!Box 6490 Cable', 'Vodafone Hotspot', 'zrwguests', 'HITRON-9A60', 'Leonardo2', 'KabelBox-4484', 'DIRECT-51-HP OfficeJet 4650']
        7.5918 [terkin.radio             ] INFO   : WiFi STA: Network candidates: ['GartenNetzwerk']
        7.6036 [terkin.radio             ] INFO   : WiFi STA: Attempting to connect to network "GartenNetzwerk"
        7.6156 [terkin.radio             ] INFO   : WiFi STA: Connecting to "GartenNetzwerk"
        7.6361 [terkin.radio             ] INFO   : WiFi STA: Waiting for network "GartenNetzwerk".
        8.6486 [terkin.radio             ] INFO   : WiFi STA: Waiting for network "GartenNetzwerk".
        9.6620 [terkin.radio             ] INFO   : WiFi STA: Waiting for network "GartenNetzwerk".
       10.6745 [terkin.radio             ] INFO   : WiFi STA: Waiting for network "GartenNetzwerk".
       11.6947 [terkin.radio             ] INFO   : WiFi STA: Connected to "GartenNetzwerk" with IP address "192.168.178.143"
       11.7129 [terkin.radio             ] INFO   : WiFi STA: Networking address: mac=(sta_mac=b'\x80}:\xc3B\xbc', ap_mac=b'\x80}:\xc3B\xbd'), ifconfig=('192.168.178.143', '255.255.255.0', '192.168.178.1', '192.168.178.1')
       11.7308 [terkin.radio             ] INFO   : Network interface ready
       11.7463 [terkin.device            ] INFO   : [LoRa] Disabling LoRa interface as no antenna has been attached. ATTENTION: Running LoRa without antenna will wreck your device.
       11.7600 [terkin.device            ] INFO   : Starting telemetry
       17.1366 [terkin.telemetry         ] INFO   : Telemetry channel URI: mqtt://swarm.hiveeyes.org/hiveeyes/testdrive/area-38/fipy-workbench-01
       17.1472 [terkin.telemetry         ] INFO   : Starting Terkin TelemetryClient
       17.1771 [terkin.telemetry         ] INFO   : Telemetry channel URI: mqtt://weather.hiveeyes.org/workbench/testdrive/area-38/fipy-workbench-01
       17.1881 [terkin.telemetry         ] INFO   : Starting Terkin TelemetryClient
       17.2156 [terkin.datalogger        ] INFO   : Starting all busses [{'pin_scl': 'P10', 'number': 0, 'enabled': True, 'family': 'i2c', 'pin_sda': 'P9'}, {'enabled': True, 'pin_data': 'P11', 'number': 0, 'family': 'onewire'}]
       17.2611 [terkin.sensor            ] INFO   : Found 1 I2C devices: [119].
       17.2728 [terkin.sensor            ] INFO   : Registering bus "i2c:0"
       19.0344 [terkin.sensor            ] INFO   : Found 2 OneWire (DS18x20) devices: [b'28ff641d8fdf18c1', b'28ff641d8fc3944f'].
       19.0472 [terkin.sensor            ] INFO   : Registering bus "onewire:0"
       19.0576 [terkin.datalogger        ] INFO   : Registering Terkin sensors
       19.0673 [hiveeyes.datalogger      ] INFO   : Registering Hiveeyes sensors
       19.7159 [hiveeyes.sensor_hx711    ] INFO   : Selected HX711 hardware driver "heisenberg"
       19.7336 [hiveeyes.sensor_hx711    ] INFO   : Initializing HX711 sensor with pin_dout=P22, pin_pdsck=P21, gain=128, scale=4.424242, offset=-73000.0
       19.7463 [hx711                    ] INFO   : HX711 initialization started
       19.8297 [hx711                    ] INFO   : HX711 initialization succeeded
       20.1178 [hx711_heisenberg         ] INFO   : Gain & initial value set
       20.1356 [terkin.sensor            ] INFO   : Trying to find bus by name "onewire:0"
       20.1464 [terkin.sensor            ] INFO   : Found bus by name "onewire:0": <OneWireBus object at 3f98d620>
       20.2216 [terkin.sensor            ] INFO   : Trying to find bus by name "i2c:0"
       20.2319 [terkin.sensor            ] INFO   : Found bus by name "i2c:0": <I2CBus object at 3f98cee0>
       20.2518 [terkin.datalogger        ] INFO   : --- loop ---
       20.2643 [terkin.datalogger        ] INFO   : Reading 4 sensor ports
       25.6847 [terkin.datalogger        ] INFO   : Sensor data:  {'temperature.0x77.i2c:0': 27.15, 'temperature.28ff641d8fc3944f.onewire:0': 24.75, 'pressure.0x77.i2c:0': 1005.95, 'memfree': 2276320, 'temperature.28ff641d8fdf18c1.onewire:0': 25.8125, 'humidity.0x77.i2c:0': 38.3, 'weight': 85490.32}
       25.7158 [terkin.telemetry         ] INFO   : Telemetry transport: MQTT over TCP over WiFi
       25.8643 [terkin.telemetry         ] INFO   : Starting connection to MQTT broker. client_id=terkin.807d3ac342bc, netloc=swarm.hiveeyes.org
       26.5122 [terkin.telemetry         ] INFO   : Connecting to MQTT broker at swarm.hiveeyes.org
       26.9751 [terkin.telemetry         ] INFO   : Connecting to MQTT broker at ('46.4.251.66', 1883) succeeded
       27.1081 [terkin.telemetry         ] INFO   : Telemetry transport: MQTT over TCP over WiFi
       27.2583 [terkin.telemetry         ] INFO   : Starting connection to MQTT broker. client_id=terkin.807d3ac342bc, netloc=weather.hiveeyes.org
       27.2752 [terkin.telemetry         ] INFO   : Connecting to MQTT broker at weather.hiveeyes.org
       27.4034 [terkin.telemetry         ] INFO   : Connecting to MQTT broker at ('46.4.251.67', 1883) succeeded
       27.5273 [terkin.datalogger        ] INFO   : Telemetry status: SUCCESS
       32.6952 [terkin.datalogger        ] INFO   : --- loop ---
       32.7064 [terkin.datalogger        ] INFO   : Reading 4 sensor ports
       38.0680 [terkin.datalogger        ] INFO   : Sensor data:  {'temperature.0x77.i2c:0': 26.75, 'temperature.28ff641d8fc3944f.onewire:0': 24.75, 'pressure.0x77.i2c:0': 1006.06, 'memfree': 2422512, 'temperature.28ff641d8fdf18c1.onewire:0': 25.8125, 'humidity.0x77.i2c:0': 38.39, 'weight': 85526.49}
       38.3436 [terkin.datalogger        ] INFO   : Telemetry status: SUCCESS
       43.5101 [terkin.datalogger        ] INFO   : --- loop ---
       43.5211 [terkin.datalogger        ] INFO   : Reading 4 sensor ports
       48.9117 [terkin.datalogger        ] INFO   : Sensor data:  {'temperature.0x77.i2c:0': 26.76, 'temperature.28ff641d8fc3944f.onewire:0': 24.75, 'pressure.0x77.i2c:0': 1006.01, 'memfree': 2422064, 'temperature.28ff641d8fdf18c1.onewire:0': 25.8125, 'humidity.0x77.i2c:0': 38.31, 'weight': 85553.67}
       49.1873 [terkin.datalogger        ] INFO   : Telemetry status: SUCCESS
       54.3541 [terkin.datalogger        ] INFO   : --- loop ---
       54.3651 [terkin.datalogger        ] INFO   : Reading 4 sensor ports
       59.7557 [terkin.datalogger        ] INFO   : Sensor data:  {'temperature.0x77.i2c:0': 26.7, 'temperature.28ff641d8fc3944f.onewire:0': 24.75, 'pressure.0x77.i2c:0': 1005.93, 'memfree': 2422080, 'temperature.28ff641d8fdf18c1.onewire:0': 25.875, 'humidity.0x77.i2c:0': 38.41, 'weight': 85574.0}
       60.0387 [terkin.datalogger        ] INFO   : Telemetry status: SUCCESS
