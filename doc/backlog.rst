################################
Hiveeyes MPY data logger backlog
################################


*******************
Sandbox environment
*******************

Efficiency
==========
- [o] How to run program with soft reset instead of hard reset?
- [o] How to run multiple repl commands at once?
- [o] Improve build time
    - ``make recycle scopes=full``
    - ``make recycle scopes=main,hiveeyes``
    - ``make recycle scopes=main,terkin``

Misc
====
- [o] Release version 0.1.0
- [o] Upload .mby code through mby-cross
- [o] Docs, docs, docs
- [o] Report about how much this framework weighs in - in terms of
      memory (RAM and flash) and maybe other resources


*************
Documentation
*************
- [o] Add guidelines for Python2, Python3, MicroPython and other
  programs required to setup the programming environment
- [o] Add "About", "Authors"


**********
Datalogger
**********
- [o] Solid configuration system
- [o] Use pure-Python "urllib" without dependency to "libpcre"
- [o] Appropriate logging
- [o] Periodic servicing tasks
- [o] Poll/refresh WiFi connection
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
- [o] Multi-network WiFi
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
