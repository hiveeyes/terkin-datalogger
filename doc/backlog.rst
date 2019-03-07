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
- [o] Improve build time: ``make recycle scope=full``

Misc
====
- [o] Release version 0.1.0
- [o] Upload .mby code through mby-cross
- [o] Docs, docs, docs


**********
Datalogger
**********
- [o] Solid configuration system
- [o] Use pure-Python "urllib" without dependency to "libpcre"
- [o] Appropriate logging
- [o] Periodic servicing tasks
- [o] Poll WiFi connection
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
