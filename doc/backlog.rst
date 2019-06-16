#######################################
Hiveeyes MicroPython Datalogger backlog
#######################################


**********
Datalogger
**********

Prio 1
======
- [o] Check appropriate interrupt handling of lowlevel sensor drivers
- [o] Gracefully set time using NTP
  https://docs.pycom.io/firmwareapi/micropython/utime.html#maintaining-actual-calendar-datetime
- [o] Unlock NVRAM storage as ConfigurationSettings overlay
- [o] Add named fields based on NVRAM overlay
- [o] AP mode
- [o] Make retry interval / WiFi timeout configurable
- [o] Sensor enabled/disabled for configuration settings
- [o] Aggregate errors and submit using MQTT
- [o] Reactivate Watchdog Timer
- [o] Enable/disable sensors
- [o] Transmit system states via MQTT

Prio 1.1
========
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
- [o] Properly calculate sleep time from interval and duty cycle duration
- [o] Connect to Beep
- [o] Follow up with
    - https://community.hiveeyes.org/t/terkin-for-micropython/233/10
    - https://community.hiveeyes.org/t/fipy-verliert-programm-nach-power-off-durch-leeren-lipo-vermutlich-brownout-filesystem-corruption/2057
- [o] Documentation 140mm. Getting started, Pictures, Sphinx.
- [o] Write about Terkin Telemetry.
- [o] New target ``make format-flash``.
- [o] Bundle and upload package to GitHub always when invoking ``make release``?
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
- [o] ESP32 Mock for testing
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


Prio 1.3
========
- [o] Looks like the HX711 does not grok the ``offset`` parameter?
- [o] Appropriate control for turning on DEBUG logging
- [o] Guard against running without (valid?) ``settings.py``
- [o] Use non-u-name imports, see also https://micropython.readthedocs.io/en/latest/library/#python-standard-libraries-and-micro-libraries
- [o] Add software tests
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
- [o] Unlock frozen modules: Upload .mby code through mby-cross
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
