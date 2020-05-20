.. _terkin-backlog:

#########################
Terkin Datalogger backlog
#########################


***************
Datalogger 2020
***************

S1
==
- Optional Zeitstempel in MQTT/JSON-Nachricht einfügen.
- Verschiedene Sendezyklen pro Telemetrie-Eumel ermöglichen.
- "LoRaDriverDragino.ensure_connectivity()" non-blocking gestalten.
- Sensor-Wrapper für PyTrack, Gpsd und 2xSolarlader erschließen.

S2
==
- Cayenne-Mapping: Use dataframe.readings.
- Sensor-Gruppen per Tags definieren.
- Sensor-Metadaten einführen. Beispiel: Timestamp pro Sensor-Reading.
- data_in => data_out

S3
==
- /backup-Verzeichnis optional ansprechen
- Exceptions auf CPython abfangen
- Installation von mpy-cross auf RaspberryPi aussparen
- Sensors: Observation einführen, SensorReading => Reading umbenennen
- Telemetry: Sequans Modem erschließen
- Telemetry: ``settings.telemetry_name`` honorieren
- Improve formatting of "Sensor data" output
- Setup: Tracer-MT5 code auslagern
- Setup: gpsd code auslagern
- Setup: Debian-Paket bauen?
- Setup: Abhängigkeiten klären: python-spidev python3-spidev + pip spidev!?
- Setup: /boot/config.txt overlay und /etc/default/gpsd-Konfiguration automatisieren
- Setup: dpkg-reconfigure UI?
- Doku bei
  https://community.hiveeyes.org/t/uberarbeitung-des-terkin-readme-im-repository/3152/5
  bzw.
  https://github.com/hiveeyes/terkin-datalogger/blob/master/doc/cpython.rst
  aktualisieren und veröffentlichen
- Update credits

S4
==
- Telemetry: Uplink messages to Dragino.
- Telemetry: Pure-LoRa w/o LoRaWAN
- Telemetry: Improve handling for "no-lora-connectivity" (by @Thias)
- Sensors: Add more sensors for standard CPython
    - Standard Linux
        - free -m
    - https://github.com/giampaolo/psutil
    - https://pypi.org/project/PySensors/
    - https://elinux.org/RPI_vcgencmd_usage
        - vcgencmd measure_temp
- Infra: Starting TerkinConfiguration on path "/"

S5
==
- I2C-Busse auf rasi12bplus
- raspi-config nonint
- Support Odroid XU4 within Adafruit Blinka adafruit_platformdetect
- Resolve https://github.com/hiveeyes/terkin-datalogger/commit/a945518845b9fb0f5a97dafde90ab4d60de0ed14
- ``terkin --sensor=bme280`` vs. ``terkin --no-sensors``
- Plattformweiche für Makefile re. mpy-cross
- When EPSolar is enabled, improve log message "AttributeError: 'NoneType' object has no attribute 'read_serial'"
- 2x "Reading sensor port "ADS1x15Sensor"" without further classification
- LoRa wiederherstellen
- Adafruit PureIO fails to access ADS1x15 sensor attached to I2C bus using smbus when run as non-root.
- "Reading sensor GPSD" takes ages when it has no Fix.
- Improve GPSD configuration re. "with PPS" and with or without "-n" option
- C-UTF8 Fehler auf Odroid::

    RuntimeError: Click will abort further execution because Python 3 was configured to use ASCII as encoding for the environment. Consult https://click.palletsprojects.com/python3/ for mitigation steps.

    This system supports the C.UTF-8 locale which is recommended. You might be able to resolve your issue by exporting the following environment variables:

        export LC_ALL=C.UTF-8
        export LANG=C.UTF-8
    tools/cpython.mk:35: recipe for target 'run-cpython' failed
- Wait for "[Dragino                       ] DEBUG  : TX Complete" before confirming TX on Dragino
- Transmit timestamps over LoRa
  https://github.com/smlng/pycayennelpp/pull/42

S6
==
- Improve platform_info.MICROPYTHON.RaspberryPi: Not everything is specific to RaspberryPi here,
  e.g. pyserial-based drivers like EPSolar or VEDirect
- Besseres Abfangen von Fehlern in der LoRaWAN/TTN config
- Umbau der dragino.py-Bibliothek auf Basis von https://pypi.org/project/pyLoRa/
  - Ask Rui Silva upfront about his interest to make it compatible with Dragino.
- LoRa: Improve timeout behaviour, see https://community.hiveeyes.org/t/lora-joins-dauern-teilweise-seeeeeeeehr-lange/3186
- Bootzeit wieder reduzieren (dist-packages aufräumen)
  - Publish Terkin MicroPython Assets to GitHub w/o Dragino stuff
- Captive Portal (@clemens, @flower4bees)
- Statemachine via pysm (@poesel)
- Unlock ADS1x15 from @robert-hh, see https://github.com/robert-hh/ads1x15
- Unlock INA219, see https://github.com/hiveeyes/terkin-datalogger/issues/39

S7
==
- Make "settings-user.json" work
- Update Annapurna firmware images
- Send annotations
- Improve tests using
    - https://pypi.org/project/fake-rpi/
    - https://pypi.org/project/serial_mock/
- Detect and mitigate connection-loss with LTE-connectivity
- Add reading ``/sys/class/thermal/thermal_zone0/temp``
- Tweak MQTT configuration to publish just to designated MQTT topic
- neocon in "make console" einbauen
- Set system time from NTP or GPS


Documentation
=============
- README header
- Pictures
- LICENSE => AGPL
- setup.py => Link to documentation and download
- https://www.sphinx-doc.org/en/master/usage/extensions/coverage.html
- https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html
- Document "make run-cpython-callgraph"
- Improve documentation structure re. MicroPython sandbox



***************
Datalogger 2019
***************

Prio 0.7
========
- Sensor-Mapping for @clemens, @wtf and @mko
- Use WLAN power_save, see https://docs.pycom.io/firmwareapi/pycom/network/wlan/
- Investigate if re-reading ``settings.py`` works
  https://forum.pycom.io/topic/5296/reread-setting-py-while-the-program-is-running
- Build custom firmware
  https://forum.pycom.io/topic/3902/frozen-modules-for-my-sipy-solved/9
  pycom-micropython-sigfox/esp32/pycom_version.h
- Ping @rdagger
    - https://github.com/rdagger
    - https://github.com/jczic/MicroWebSrv/issues/7
    - https://www.youtube.com/playlist?list=PLKGiH5V9SS1hUz5Jh_35oTFM4wPZYA4sT
- Try WiFi power saving.
- Include uPing and others into annapurna
    - https://gist.github.com/shawwwn/91cc8979e33e82af6d99ec34c38195fb
    - https://forum.pycom.io/topic/5348/gpy-full-flash-erase/40
- Maybe use ``machine.rng()``
- Implement ``reboot`` via UDP mode server
- Maybe just send ``lte.send_at_cmd('AT!="powerOff"')`` for shutting down the LTE modem?
- When the network goes away while in live mode, the MQTT submission hangs forever::

    231.9092 [terkin.telemetry         ] INFO   : MQTT payload: {"system.voltage": 3.732, "system.wifi.country": "DE", "system.wifi.max_tx_power": 78, "system.time": 230, "system.temperature": 22.17392, "system.wifi.channel": 6, "system.uptime": 230.707, "system.wifi.bandwidth": 2, "system.memfree": 2324320, "system.runtime": 224, "system.wifi.rssi": -48}



Prio 0.8
========
- wget ftp.exe
- [o] Leave maintenance mode after 10 minutes
- [o] Configure ARP-ping timeout for "terkin.py"
  https://community.hiveeyes.org/t/running-terkin-py-on-windows/2273/31
- [o] Add more information to ``make help``
- Output network config on each cycle in non-deepsleep mode
- Client wrapper for Terkin HTTP API. e.g. sync files, upload config, restart
  What about ``terkinctl``?
- When putting files on the device, maybe halt the program!?
- Check out switching to
    - https://github.com/peterhinch/micropython-mqtt
    - https://github.com/yutter/micropython-mqtt
- How to catch and report bad things like::

    Traceback (most recent call last):
      File "main.py", line 31, in <module>
      File "/flash/lib/hiveeyes/datalogger.py", line 14, in <module>
      File "/flash/lib/terkin/datalogger.py", line 12, in <module>
      File "/flash/lib/terkin/configuration.py", line 12, in <module>
      File "/flash/lib/terkin/util.py", line 151, in <module>
    NameError: name 'contextmanager' is not defined
- Pull modeserver into MiniNet. Add reboot functionality to modeserver.
- Implicitly connect to network on ``make recycle-ng``
- Automatically connect to console if device is discovered
- https://github.com/Bucknalla/balena-pycom-ota
- Detect file transfer errors::

    time lftp -u micro,python 192.168.178.143 < tools/upload-all.lftprc
    mirror: Access failed: 550  (telemetry.py)
- ``?overwrite=true`` option or ``DELETE`` action for purging configuration files
- Curate FTP upload by prewarming the device for transfer to mitigate the 550 errors references above
- Prevent invalid runtime configuration settings like ``main.interval.field=None``
- When halting the datalogger using ``CTRL+C``, another ``datalogger.start()`` will register all sensors again ;[
- Notify user about pulling into maintenance mode
- Enumerate all DS18B20 sensors and provide over HTTP
- Write description to prettified sensor output
- Install from::

    pycopy-collections==0.1.3
    pycopy-collections.defaultdict==0.3

- MQTT authentication with URI parameter and email address as username does not work
- Build release packages like https://github.com/adafruit/Adafruit_CircuitPython_BusDevice/releases
- Windows bundle containing mpy-mk, make.exe, wget.exe, lftp.exe, pycom-fwtool-cli.exe
- Implement soft-reset using sys.exit(), see https://docs.pycom.io/gettingstarted/programming/safeboot/
- Add https://forum.pycom.io/topic/3926/ble-att-wrapper
- Write a characteristic user descriptor
    - https://stackoverflow.com/questions/33328272/adding-characteristic-user-description-to-custom-c-ble-gatt-service
    - https://github.com/moovel/gatt-server/blob/master/README.md#implementing-services-with-ggk
    - https://github.com/adafruit/Adafruit_nRF52_Arduino/blob/68400a76662af268829e3c6c66ae62ac02eaae76/libraries/Bluefruit52Lib/src/BLECharacteristic.cpp#L316-L344
    - https://github.com/pycom/pycom-micropython-sigfox/blob/master/esp32/mods/modbt.c#L1276-L1290

- Use "hupper" for watching files
- Remark about "LTE only with antenna"
  https://forum.pycom.io/topic/4721/working-lte-connection-in-germany/13
- [o] Move UDP mode server to mininet already
- http://docs.micropython.org/en/v1.9.3/esp8266/library/btree.html
- Use wait_for_nic from MicroWifi
- Investigate crashes on Pycom from using ``time.ticks_ms()`` when running multithreaded


Prio 0.9
========
::

    [main.py] INFO: Starting Terkin Datalogger
       18.3435 [terkin.configuration     ] INFO   : Starting TerkinConfiguration on path "/flash"
       18.3644 [terkin.configuration     ] INFO   : Ensuring existence of backup directory at "/flash/backup"
    Unhandled exception in thread started by <bound_method>
    Traceback (most recent call last):
      File "network/ip.py", line 24, in start_real
    OSError: Network card not available

- [o] When multiple networks of the same name exist, use the one with the better RSSI::

    INFO:  WiFi STA: Scanning for networks
    INFO:  WiFi STA: Networks found ['GartenNetzwerk', 'GartenNetzwerk', 'Vodafone-7982', 'hausbuch', 'zrwguests', 'HITRON-9A60']
    INFO:  WiFi STA: Connecting to "GartenNetzwerk"
    INFO:  WiFi STA: Connected to "GartenNetzwerk"
    INFO:  WiFi STA: Connecting to "GartenNetzwerk"
    INFO:  WiFi STA: Connected to "GartenNetzwerk"

- [o] Enable logging when in maintenance mode
- [o] If logging is disabled, either log nothing at all or
    Ensuring existence of backup directory at "/flash/backup"
- [o] https://forum.pycom.io/topic/3425/new-beta-firmware-updater-1-15-2-b0

- [o] https://community.hiveeyes.org/t/backlog-terkin-datenlogger-fur-bob/2277
- [o] https://community.hiveeyes.org/t/remote-logging-zur-ferndiagnose-fur-den-terkin-datenlogger/2280
- [o] https://community.hiveeyes.org/t/loggen-von-daten-und-error-warning-events-auf-sd/2279
- [o] https://community.hiveeyes.org/t/http-und-webbasierte-konfiguration-fur-terkin-datenlogger-captive-portal/2270
- [o] https://community.hiveeyes.org/t/kontinuierliche-verbesserungen-des-terkin-datenloggers-600er/2121

Prio 1
======
- [o] More power saving
    - [o] Low-voltage cutoff
          https://github.com/opensourcebeehives/DataLogger/commit/39b45433dc54ce60419429fc6e6c114c7c3fa4a2
    - [o] Turn off LED-RGB completely
- [o] WiFi STA: Support connecting to BSSIDs
- [o] Exponential backoff for WiFi STA, MQTT broker and general connectivity
- [o] Time-based timeout behavior for everything, not just based on retries
- [o] Interpolate Device-ID into telemetry node name or better derive humanized name from it.
      See also https://github.com/HowManyOliversAreThere/six-nibble-name
- [o] Revisit smoothing of HX711 value
- [o] Improve HX711 timeout
- [o] Call name support
- [o] Release names: Murmeltier, Mordillo
- [o] Release pics
    - https://commons.wikimedia.org/wiki/File:Agc_view.jpg
- [o] Current firmware 1.20.0.rc12
- [o] Build complete firmware, see
  https://github.com/pycom/pycom-libraries/tree/master/pycom-docker-fw-build
- [o] Make WiFi-timeout configurable, see ``wifi.py`` at ``network.get('timeout', 15.0)``


Prio 1.1
========
- [o] Publish system events to MQTT
- [o] Subscribe to MQTT downlink channel
- [o] Unlock NVRAM storage as ConfigurationSettings overlay
- [o] Add named fields based on NVRAM overlay
- [o] OneWire sensor enumeration - display lexographically sorted?
- [o] DEBUG mode

Prio 1.2
========
- [o] Introduce and wire maintenance mode
    - Increase measurement frequency
    - Start access point
    - Start webserver
- [o] How to find individual espressif nodes on a LAN network?
- [o] Add README and docs to download bundle.
- [o] Resistor values for BOB-Board
  https://community.hiveeyes.org/t/pycom-mpy-verbesserung-des-systembatterylevel-systemsensors-energiehaushalt/2128/10
- [o] Tiefentladungsschutz
- [o] Buttons:
    - Improve configuration
    - Wire to actions
    - Wake up from deepsleep, see https://docs.pycom.io/firmwareapi/pycom/machine/#machinepindeepsleepwakeuppins-mode-enablepull
- [o] Bundle and upload package to GitHub always when invoking ``make release``
- [o] Improve LED signalling
- [o] Map Chip-ID to specific configuration file
- [o] Gracefully set time using NTP
  https://docs.pycom.io/firmwareapi/micropython/utime.html#maintaining-actual-calendar-datetime
- [o] AP mode
- [o] Make retry interval / WiFi timeout configurable
- [o] Sensor enabled/disabled for configuration settings
- [o] Aggregate errors and submit using MQTT
- [o] Enable/disable sensors
- [o] Transmit system states via MQTT
- [o] settings: Rename "sensors.registry" to "sensors.environment".

Prio 1.3
========
- [o] Check appropriate interrupt handling of lowlevel sensor drivers
- [o] Generic "median" function
- [o] BT-OFF and BT-Proximity
- [o] Set DNS servers: https://forum.pycom.io/topic/4361/new-stable-firmware-release-v1-18-2
- [o] https://appelsiini.net/2017/wipy-esp32-firmware-cli/
- [o] Is ``LTE.deinit()`` required?
    - https://community.hiveeyes.org/t/deep-sleep-with-fipy-esp32-on-micropython/1792/10
- [o] Debug level!
- [o] Deactivate all peripherals
- [o] Deactivate LDO
    - https://community.hiveeyes.org/t/low-power-esp32-hardware-and-software/538/9
- [o] Log filesystem type
- [o] Measure and transmit WiFi RSSI, and voltage from ADC
- [o] Add duty cycle counter
- [o] Improve logging: Report about available telemetry targets upfront
- [o] Telemetry payload v2
    - meta: version, time, device=807d3ac342bc
    - system: rssi, cycles
    - observations: all the data
- [o] Report about to how many telemetry targets data will be sent
- [o] Follow up with
    - https://community.hiveeyes.org/t/terkin-for-micropython/233/10
    - https://community.hiveeyes.org/t/fipy-verliert-programm-nach-power-off-durch-leeren-lipo-vermutlich-brownout-filesystem-corruption/2057
- [o] Documentation 140mm. Getting started, Pictures, Sphinx.
- [o] Write about Terkin Telemetry.
- [o] New target ``make format-flash``.
- [o] Selectively enable/disable logging per module from configuration settings
- [o] Disable interrupts when reading sensors
  https://docs.pycom.io/firmwareapi/pycom/machine/#interrupt-functions
- [o] Measure battery level
  https://forum.pycom.io/topic/3776/adc-use-to-measure-battery-level-vin-level
- [o] Improve accuracy for ``system.uptime``
- [o] How would we work through a predefined schedule when starting with WiFi off?
- [o] MQTT Hello Beacon
- [o] Debug/trace mode should send all kinds of information through
      the Hello Beacon or alongside each reading.
- [o] Go to https://github.com/ayoy/upython-aq-monitor/blob/lora/main.py for more cherry picking.
    - Asynchronous measurements
    - Add PMS5003 sensor
    - Add ``alive_timer`` based on ``Timer.Chrono()``
    - Battery low warning & shutdown: if voltage < 4.0 / < 3.7 (normal: 4.3)
    - MOSFET gate
- [x] ESP32 Mock for testing: https://github.com/hiveeyes/terkin-datalogger/tree/master/test
- [o] Scan Bluetooth neighbourhood for proximity applications
  https://docs.pycom.io/firmwareapi/pycom/network/bluetooth/
- [o] Add Device ID as HTTP header
- [o] Why does HX711 not yield an error when not connected?
- [o] Inquire modem firmware version
  https://forum.pycom.io/topic/4727/how-to-determine-modem-firmware-version
- [o] https://forum.pycom.io/topic/4818/efficient-firmware-app-update
- [o] Not connecting a HX711 yields ``"weight": 0.0``
- Power: {'reset_cause': {'code': 0, 'message': 'PWRON'}, 'wakeup_reason': {'code': 0, 'message': 'PWRON'}}
- Reset: {'reset_cause': {'code': 0, 'message': 'PWRON'}, 'wakeup_reason': {'code': 0, 'message': 'PWRON'}}
- Check "Espressif-specific" Long Range mode, see
  https://github.com/pycom/pycom-micropython-sigfox/pull/281

Prio 1.4
========
- [o] Looks like the HX711 does not grok the ``offset`` parameter?
- [o] Appropriate control for turning on DEBUG logging
- [o] Guard against running without (valid?) ``settings.py``
- [o] Use non-u-name imports, see also https://micropython.readthedocs.io/en/latest/library/#python-standard-libraries-and-micro-libraries
- [x] Add software tests
- [o] Control the board through https://github.com/dhylands/rshell/blob/master/rshell/pyboard.py
- [o] Makefile: Check for "wget"
- [o] Migrate settings.py to settings.json
- [o] Add webserver to framework
- [o] First MQTT downlink message
- [o] https://community.grafana.com/t/mqtt-data-in-html-panel/14120

Prio 1.5
========
- [o] Store-and-forward when no connectivity
- [o] Add AP mode and webserver
- [o] Better BME/BMP libraries
- [o] Bli, bla, blubb
- [o] Propagate last error message from telemetry subsystem
      into intermediary status outcome and display to user.
- [o] Save from ``radio.py``::

    # Todo: What about when coming back from sleep?
    # Needed to avoid losing connection after a soft reboot
    # if True or machine.reset_cause() != machine.SOFT_RESET:
    import pycom


Prio 2
======
- [o] Don't upload the "terkin" library each time.
- [o] Improve tooling by adding file watcher or even delta patching
- [o] Improve display of "Networking address" by decoding mac address values
- [o] Add configuration variant based on JSON file
- [o] Sensor data model: Introduce Measurement (single) and Reading (bunch) objects
- [o] Status and sensor announcement
- [o] Reconnect to WiFi and MQTT when dropping off, use exp. backoff?
- [o] Periodic servicing tasks for NetworkManager
- [o] Add MQTT-based runtime configuration like ``mqtt://daq.example.org/.../settings.json`` or
  ``.../rpc/request`` vs. ``.../rpc/response``
- [o] Is ``utime`` actually the same as ``time``?
- [o] Publish sensor configuration at first time telemetry contact
- [o] Implement access to Switches: https://micropython.readthedocs.io/en/latest/pyboard/tutorial/switch.html
- [o] Use Timers: https://micropython.readthedocs.io/en/latest/pyboard/tutorial/timer.html
- [o] Put ``dotty_dict`` into ``dist-packages``
- [o] Don't submit data when null::

    workbench/testdrive/area-38/fipy-amo-02-mqtt-lpp/data.lpp (null)


Prio 3
======
- [o] Timekeeping, use RTC and NTP
- [o] Add Watchdog timer
- [o] Basic telemetry: Battery, Temperature, Hall-Sensor
- [o] Add "wait_for_network", "check_network"
- [o] Better ordering for ``os.uname()`` attributes
- [o] Should we better use `hx711_spi.py <https://github.com/geda/hx711-lopy/blob/master/hx711_spi.py>`_?
- [o] Print stacktraces on (sensor) exceptions
- [o] Check driver correctness
    - https://github.com/geda/hx711-lopy/blob/9cc6de8d/hx711.py#L35-L37
    - https://github.com/geda/hx711-lopy/blob/9cc6de8d/hx711.py#L42-L45
    - Should ``self.pSCK.value(False)`` really run inside the constructor?
- [o] Use ``asbool`` for having string-based truthy values in configuration settings
- [o] Check what can be done using ``esptool`` already.
  See also https://randomnerdtutorials.com/flashing-micropython-firmware-esptool-py-esp32-esp8266/
- [o] Optionally use "mpy-cross" before uploading
- [o] Wired Ethernet? https://github.com/micropython/micropython-esp32/pull/187


Prio 4
======
- [o] Unlock frozen modules: Upload .mpy code through mpy-cross
- [o] Upload watcher
- [o] Add DS18B20: https://github.com/pycom/pycom-libraries/tree/master/examples/DS18X20
- [o] WiFi soft reset re. ``if machine.reset_cause() != machine.SOFT_RESET:``
- [o] Improve the AP mode::

    [0.06439157] Starting networking
    WiFi STA: Starting connection
    WiFi STA: Connect failed: list index out of range. Switching to AP mode.
    2 fipy-wlan-42bc (3, 'www.pycom.io') 0
    Networking established
    [3.663849] Starting telemetry

- [o] Publish retained status message to MQTT like ``beradio-python``::

    hiveeyes/fe344422-05bf-40f2-a299-fbf4df5d7e2b/vay55/gateway/status.json {"status": "online", "program": "beradio 0.12.3", "date": "2019-03-07T19:38:28.462900"}

- [o] Reenable WiFi AP mode
- [o] How to use uPy module "urequests"?::

    # Problem: "urequests" does not work with SSL, e.g. https://httpbin.org/ip
    # micropython -m upip install micropython-urequests
    #import urequests

- [o] Check out "Firmware over the air update":
    https://github.com/pycom/pycom-libraries/blob/master/examples/OTA/OTA_server.py
- [o] Add network name to "Already connected"
- [o] Automate cayennelpp installation https://github.com/smlng/pycayennelpp
- [o] Assistant for configuring ``serial_port`` in ``config.mk``. Optionally use environment variable!?
- [o] Use more information from WiFi station::

    'antenna', 'ap_sta_list', 'auth', 'bandwidth', 'bssid', 'callback', 'channel', 'connect', 'country', 'ctrl_pkt_filter', 'deinit', 'disconnect', 'events', 'hostname', 'ifconfig', 'init', 'isconnected', 'joined_ap_info', 'mac', 'max_tx_power', 'mode', 'promiscuous', 'scan', 'send_raw', 'ssid', 'wifi_packet', 'wifi_protocol']



Done
====
- [x] Solid configuration system
- [/] Unlock NVRAM storage::

    > Set the value of the specified key in the NVRAM memory area of the external flash.
    > Data stored here is preserved across resets and power cycles.
    > Value can only take 32-bit integers at the moment.

  - https://github.com/pycom/pydocs/blob/master/firmwareapi/pycom/pycom.md#pycomnvs_setkey-value
  - https://docs.espressif.com/projects/esp-idf/en/latest/api-reference/storage/nvs_flash.html
- [/] class NvsStore: https://forum.pycom.io/topic/2775/keeping-state-when-awaking-from-sleep
- [x] Use pure-Python "urllib" without dependency to "libpcre"
- [x] Handle "Connection to MQTT broker failed or lost"
- [x] Multi-network WiFi
- [x] Fix console crasher when running on Windows
- [x] Release version 0.1.0
- [x] Real sensors already
- [x] Add release tooling
- [x] Add snapshot of ``dist-packages`` folder as asset to each release on GitHub
- [x] Add appropriate logging
- [x] Improve logging by adding stacktrace printer
- [x] Add some examples
- [x] Report about which telemetry targets did actually work when submitting data (True / False)
- [x] Improve logging: Suppress logging of sensible information like password, application_key, application_eui, mac or ifconfig
- [x] Switch to LittleFS
- [x] Add deep sleep
- [x] Log wakeup type
- [x] Improve formatting of mac addresses
- [x] Power saving
    - [x] Turn off logging
    - [x] Turn off heartbeat of RGB-LED
    - [x] Speed-up WiFi connection by not scanning at all.
          In order to achieve that, scan once and remember auth-mode in NVRAM.
    - [x] Fix HX711 power down re. spec
    - [x] Activate internal pull-up for HX711 PD_SCK in deep sleep mode with "pin hold".
      https://docs.pycom.io/firmwareapi/pycom/machine/pin.html#pinholdhold
    - [x] Turn off serial interface completely
    - [x] Tame LED-RGB
- [x] Activate Watchdog Timer
- [x] ``make recycle-ng`` needs network!?
- [x] WiFi.is_connected would also return True when AP is up!!!
- [x] Make "make help" point to "Operate the ..."
- [x] Implement real "light sleep"
  "in light sleep mode the current consumption on a Lopy is 3.5 mA with RTC peripherals ON"
  https://forum.pycom.io/topic/3351/new-development-firmware-release-v1-19-0-b1/3
- [x] Add configuration for external WiFi antenna
- [x] Properly calculate sleep time from interval and duty cycle duration
- [x] Connect to Beep



*******************
Sandbox environment
*******************

Upload and reset
================
- [o] How to run program with soft reset instead of hard reset?
- [o] How to run multiple repl commands at once?
- [o] Improve build time
    - ``make recycle scopes=full``
    - ``make recycle scopes=main,hiveeyes``
    - ``make recycle scopes=main,terkin``
- [o] Improve tests
    - Run against non-standard MQTT port (1888)
    - UDP API
    - HTTP API
    - WiFi-HTTP telemetry
    - Pure-Python DS18B20 driver
    - State machine


*************
Documentation
*************
- [o] Docs, docs, docs
- [o] Add links to
    - https://docs.pycom.io/datasheets/development/fipy.html
    - https://docs.pycom.io/.gitbook/assets/specsheets/Pycom_002_Specsheets_FiPy_v2.pdf
    - https://docs.pycom.io/.gitbook/assets/fipy-pinout.pdf
    - https://pycom.io/wp-content/uploads/2018/08/fipySpecsheetAugust2017n2-1.pdf
- [o] Report about how much this framework weighs in - in terms of
      memory (RAM and flash) and maybe other resources
      {"memfree": 2522016}

- [o] Add guidelines for Python2, Python3, MicroPython and other
  programs required to setup the programming environment
- [o] Add "About", "Authors"
- [o] Add Sphinx documentation
- [o] Add doctests to documentation
- [o] Flash MicroPython from RaspberryPi: https://www.raspberrypi.org/forums/viewtopic.php?t=233367
- [o] Add topics about

    - Connectivity / Resiliency
    - Multi-telemetry
    - Configuration subsystem
    - User handbook
    - Developer handbook (Sandbox installation)
    - Workstation Support: Linux, macOS, Windows

- [o] Deep Sleep
    - https://www.instructables.com/id/ESP32-Deep-Sleep-Tutorial/
    - https://randomnerdtutorials.com/esp32-deep-sleep-arduino-ide-wake-up-sources/
    - https://forum.micropython.org/viewtopic.php?t=1198

- [o] https://atom.io/packages/pymakr


Other projects
==============
- https://github.com/microhomie
  https://microhomie.readthedocs.io/
- https://kapusta.cc/2017/12/02/home-made-air-quality-monitoring-using-wipy/
  https://kapusta.cc/2018/02/02/air-quality-monitor-revisited/
  https://github.com/ayoy/upython-aq-monitor/tree/lora

Misc
====
::

    workbench/testdrive/area-38/fipy-amo-02-mqtt-json/data.json {"temperature_0": 42.42, "temperature_1": -84.84}
    workbench/testdrive/area-38/fipy-amo-02-mqtt-json/data.lpp AGcBqAFn/LA=


**************
User interface
**************
- https://blog.koley.in/2019/339-bytes-of-responsive-css
  https://news.ycombinator.com/item?id=19622786



Firmware update output
======================
::

    Erased 2 MiB in 15.28 seconds
    Erased 4MB device flash fs in 1.22 second
    Wrote 20.95 KiB from bootloader.bin in 1.11 second
    Wrote 3 KiB from partitions.bin in 0.08 seconds
    Wrote 1.66 MiB from fipy.bin in 54.4 seconds
    Wrote 4 KiB from config in 0.1 seconds
    Device ID: 807D3AC2DE44
    LoRa MAC: 70B3D54992DBE31D
    Sigfox ID: 004D4881
    Sigfox PAC: 211AC57838BF7C29
