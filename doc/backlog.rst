#######################################
Hiveeyes MicroPython Datalogger backlog
#######################################


**********
Datalogger
**********

Prio 1
======
- [x] Solid configuration system
- [x] Use pure-Python "urllib" without dependency to "libpcre"
- [x] Handle "Connection to MQTT broker failed or lost"
- [x] Multi-network WiFi

Prio 2
======
- [o] Add improved logging
- [o] Improve logging by adding stacktrace printer
- [o] Improve tooling by adding file watcher or even delta patching
- [o] Improve display of "Networking address" by decoding mac address values
- [o] Add configuration variant based on JSON file
- [o] Reconnect to WiFi and MQTT when dropping off, use exp. backoff?
- [o] Periodic servicing tasks for NetworkManager
- [o] Add MQTT-based runtime configuration like ``mqtt://daq.example.org/.../settings.json`` or
  ``.../rpc/request`` vs. ``.../rpc/response``

Prio 3
======
- [o] Introduce Measurement (single) and Reading (bunch) objects
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

Prio 4
======
- [o] Upload watcher
- [o] Add deepsleep
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



Closed
======
- [/] Unlock NVRAM storage::

    > Set the value of the specified key in the NVRAM memory area of the external flash.
    > Data stored here is preserved across resets and power cycles.
    > Value can only take 32-bit integers at the moment.

  - https://github.com/pycom/pydocs/blob/master/firmwareapi/pycom/pycom.md#pycomnvs_setkey-value
  - https://docs.espressif.com/projects/esp-idf/en/latest/api-reference/storage/nvs_flash.html
- [/] class NvsStore: https://forum.pycom.io/topic/2775/keeping-state-when-awaking-from-sleep


*******************
Sandbox environment
*******************

General
=======
- [x] Release version 0.1.0
- [o] Upload .mby code through mby-cross
- [o] Docs, docs, docs
- [o] Report about how much this framework weighs in - in terms of
      memory (RAM and flash) and maybe other resources
      {"memfree": 2522016}
- [o] Add release tooling
- [o] Add snapshot of ``dist-packages`` folder as asset to each release on GitHub
- [o] Add software tests


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
- [o] Add guidelines for Python2, Python3, MicroPython and other
  programs required to setup the programming environment
- [o] Add "About", "Authors"
- [o] Add Sphinx documentation
- [o] Add doctests to documentation
