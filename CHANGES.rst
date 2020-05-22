#########################
Terkin Datalogger CHANGES
#########################


Development
===========

2020-05-22 0.10.0
=================
- Rework LoRaWAN settings and remove ``join_attempt_count`` since we can't control
  the join attempts. Thanks, @thiasB!
- Add APB activation method for LoRaWAN. Thanks, @thiasB!
- Rename "busses" to "buses" all over the place
- Fix ABP auth parameter passing for Dragino
- Improve inline documentation and logging re. LoRaWAN OTAA vs. ABP
- Disable LoRa by default
- LoRaWAN: consider restored join status for both, OTAA and ABP activation. Thanks, @thiasB!
- Add Sphinx documentation. Thanks, @poesel!
- Update Makefile tooling for upgrading Pycom MicroPython firmware
- Add Makefile target to generate callgraph
- Add minimal weight scale adjustment wizard
- Add Sequans LTE Modem support for Pycom GPy/FiPy devices. Thanks, @wetterfrosch and @tonke!
- Refactor more sensors for self-registration
- Adjust sandbox for installation on newer Debian/Ubuntu distributions. Thanks, Jan!
- Add sensor wrappers for BMP280 and INA219. Thanks, @tonke!
- Don't log configuration on startup by default. Thanks, @tonke!
- Improve registering buses
- Add sensor tests for SBCs
- Add sensor wrapper for PiUSV. Thanks, @tonke!
- Update PyCayenneLPP library to include "Generic" and "Unix Time" types.
- Add updated MicroPython "datetime" module to satisfy PyCayenneLPP
- Improve firmware builder
- Add make target to upload "settings.py"

2020-05-04 0.9.0
================
- Fix LoRa subsystem
- Add Si7021 sensor. Thanks, @thiasB!
- Add a bunch of sensors for RaspberryPi. Thanks, @tonke!
- Improve drivers VEDirect, EPSolar, ADS1x15. Thanks, @tonke!
- Fix tests
- Update TTN decoder.js. Thanks, @thiasB!
- Improve reading sensors by returning SensorReading object from driver
- Improve registering sensors by moving the setup to the sensor modules
- Improve CPython/RaspberryPi setup tooling and documentation
- Improve new sensor registration architecture once more
- Clean up EPSolar hardware driver
- Self-register EPSolarSensor
- Resolve woes with ModuleNotFoundError
- Switch settings to new LPP format scheme. Thanks, @thiasB!
- Import scale parameters as floating point number. Thanks, @thiasB!
- Update TTN README. Thanks, @thiasB!
- Enable native DS18x20 driver by default. Thanks, @ClemensGruber and @thiasB!
- Nail RaspberryPi dependencies
- Add ``sensors.power_toggle_buses`` setting, defaults to True. Thanks, @tonke!
- Improve PyTrack sensor. Thanks, @tonke!
- Update Dragino setup tooling
- Add "join_attempt_count" and "join_attempt_interval" settings re. LoRa. Thanks, @tonke!
- Add setup.py for CPython
- Improve logging and exception handling for CPython
- Make configuration file backup optional
- Improve sensor registration and startup
- Add "terkin" commandline entrypoint
- Trim CPython compatibility layer
- Improve CPython bootstrapping and logging
- Improve gpiozero and gpsd sensors. Thanks, @tonke!
- Add BME280 on Odroid XU4 based on smbus2. Thanks, @tonke!
- Fix setup.py re. encoding of README.rst
- LoRa: Ignore downlink messages for sleep interval and data payload inclusion
  on devices not running Pycom or Vanilla MicroPython. Thanks, @thiasB!
- LoRa: return to sleep interval from settings after reset. Thanks, @thiasB!
- Improve I2C bus support for Odroid XU4. Thanks, @tonke!
- Improve GPSD sensor. Thanks, @tonke!
- Use I2C bus 5 as secondary on Raspberry Pi. Thanks, @tonke!
- Improve sensor enablement evaluation. Now, sensor
  sections have to be enabled explicitly within settings.
- Fix button manager setup
- Update documentation
- Fix DS18x20 module names
- Fix tests and improve test robustness
- Fix LANG locale setting for Click at runtime. Thanks, @tonke!
- Improve CPython bootstrapping
- Fix webserver imports
- Move UDP modeserver implementation
- Don't start WiFi by default
- Make UDP modeserver and HTTP API ports configurable
- Various networking improvements
- Improve CPython setup
- Add UI spike on CPython based on Picotui
- Upgrade MicroWebSrv2 module
- Improve packaging and prepare upload to PyPI

2020-04-28 0.8.0
================
- Support SX127x on Dragino LoRa/GPS HAT for LoRa. Thanks @tonke and many more, see:
  https://github.com/mayeranalytics/pySX127x/issues/21#issuecomment-620695583
- Add TTN/LoRaWAN README. Thanks, @thiasB!
- TTN: Add payload converter code for PutsReq.com HTTP endpoint. Thanks, @thiasB!

2020-04-27 0.7.2
================
- Fix ``I2CBus.power_on``. Thanks, @tonke!

2020-04-26 0.7.1
================
- Improve packaging
- Improve compatibility between Genuine MicroPython and Pycom MicroPython
  - https://github.com/micropython/micropython/issues/5915
  - https://github.com/pycom/pycom-micropython-sigfox/issues/436

2020-04-22 0.7.0
================
- Fix sandbox installation issue by nailing pycopy-cpython-upip to 1.2.6
- Improve sanity checks for sandbox setup
- Improve RGB-LED signalling
- Import microWebSrv only when enabling HTTP service to save memory
- Make WiFi work in non-threaded environments again
- Improve MiniNet WiFi connectivity
- Improve logging timestamping
- Improve sandbox tooling robustness
- Upgrade to pycopy-cpython-upip==1.3.3 again. Thanks, Paul!
- Add basic recycle task for uploading the code to the Pyboard D
- Start LoRa on demand to reduce memory consumption
- Defer loading modules for sensors at runtime to save memory
- Load the ADC module for "SystemBatteryLevel" at runtime
- Fix missing ADC module import
- Process DS18B20 addresses case insensitive
- Port to ESP32 WROVER with MicroPython 1.11. Thanks, Markus!
- Fix network status flag
- Improve cross-compilation tooling re. Pycom vs. pyboard-D
- Display HTTP egress payload in log output on INFO level
- Add option to use external WiFi antenna
- Pyboard D-series: Improve sandbox tooling
- Pyboard D-series: Make the source tree compatible with Genuine MicroPython
- Adjust slightly for running on Pycom devices again
- WiFi adjustments for Pyboard-D
- Appropriately compute sleep time, resolve #4
- Make ``make setup`` more platform-agnostic, resolve #20
- Add external antenna option for vanilla MicroPython
- Use trimmed-down settings.py for PYBD
- Add configuration settings overlay per ``settings-user.json``
- Improve robustness with minimal configuration for PYBD
- Improve instructions for Pycom firmware bundling and installation
- Adjust sandbox infrastructure for Pycom MicroPython 1.11
- Fix import path of ``onewire`` module
- Fix weird error when freezing modules
- Add LoPy4 support in Bootloader. Thanks, @poesel.
- Add auto docstrings with pyment. Thanks, @poesel.
- Large refactoring.
    - Get rid of the "hiveeyes" module namespace.
    - Rework the "sensors.system" configuration section.
- Improve configuration module.
    - Reduce convolution of "purge_sensible_settings"
    - Be more graceful when attempting to read json settings
- Add missing ``import socket`` to LoRa module. Thanks, @thiasB!
- Improve multi-platform support
    - Refactor platform switch and rename first stage bootloader
      to *Universal MicroPython Application Loader (umal)*
    - Improve gracefulness for MachineResetCause helper
- Improve WiFi robustness on first connection attempt
- Gracefully handle buses without names. Thanks, @thiasB!
- Be graceful if OSError exception object received from
  MQTT publishing has no "errno" attribute.
- Improve sensor registration mechanics again
- Improve utility functions to work around the 128-bit UUID byte swap problem.
  Thanks, @poesel!
- Disable web server by default.
- Make use of LoRaWAN state restoration from NVRAM. Thanks, @thiasB!
- Only restore LoRa state from NVRAM on wake from deep sleep. Thanks, @thiasB!
- Refactor BLE encoding/decoding utility functions
- Improve connection to WiFi after starting again
- Use ``lte.deinit(reset=True)`` for shutting down LTE modem on startup,
  see https://forum.pycom.io/topic/3083/lte-deinit-not-working/2. Thanks, @combaindeft!
- Speed up shutting down LTE modem on startup by not invoking "detach"
  as we haven't actually been attached at all, like ``lte.deinit(detach=False, reset=True)``.
  Thanks @arapostol for https://github.com/pycom/pycom-micropython-sigfox/pull/255/files
  which made us look at the source code in detail.
- Improve robustness of WiFi manager re. "connectivity after reset" again
- Improve inline documentation
- Improve platform switch for system sensors
- Acquire ``onewire.py`` drivers for both Vanilla MicroPython and Pycom MicroPython
  as ``onewire_native.py`` vs. ``onewire_python.py``.
- Fix 1-Wire multi-platform support again. Thanks, @poesel!
- Port codebase to Genuine MicroPython on ESP32. Thanks, @poesel!
- Adjust naming for sensor driver adapters
- Obtain improved lowlevel MicroPython driver for the MAX17043. Thanks, @poesel!
- Upgrade to MicroWebSrv2. Thanks, Jean-Christophe (@jczic)!
- Fix multi-platform support for SystemTemperatureSensor
- Improve WiFi connectivity after hard reset again
- Catch KeyboardInterrupt in order to properly shut down the HTTP server. Thanks, @jczic!
- Just start HTTP server once without trying again
- Upgrade to MicroWebSrv2 2.0.2
- Catch ``KeyboardInterrupt`` exceptions in WiFi keepalive thread and
  ``UdpServer`` in order to shut down using a single ``CTRL-C``
- Upgrade to MicroWebSrv2 2.0.3. Thanks, @jczic!
- Improve thread shutdown behavior when receiving ``SIGINT`` / ``CTRL-C``
- Improve sensor reading from 1-Wire DS18X20 devices
- Support native 1-Wire/DS18X20 MicroPython driver
- Improve 1-Wire/DS18X20 support after the pure-Python variant has
  aligned its API to the one of Genuine MicroPython. Thanks, @robert-hh!
- Remove ``fastboot`` setting as the LTE modem can already be shutdown
  more quickly by using ``deattach=False``
- Improve timekeeping
- Update 1-Wire/DS18X20 driver again.
  The DS18B20 driver now also supports parasite power mode. Thanks, @robert-hh!
- Improve bootstrap messages
- Add boolean flags for enabling/disabling Wifi and LoRa. Thanks @thiasB!
- Skip reading WiFi sensors when WiFi is disabled. Thanks @thiasB!
- Optimize reading the HX711. Don't ever use ``read_average()``. Instead, just
  ``read()`` the sensor ten times for computing the median.
- Port LTE attach procedure from "Autonome Zelle". Thanks, @wtf!
- Fix installation of "MicroWebSrv2" dependency. Thanks, Chris!
- Shut down peripherals regardless of using deep sleep or not
- Battery voltage sensor: Make ADC attenuation configurable. Thanks, @thiasB!
- Power on I2C peripheral after power off. Thanks, @ckrohne!
- Enable WiFi by default if not explicitly disabled within configuration
- Improve "make install-ng": Now also works over USB/UART
- LoRaWAN/TTN integration for real. Thanks, @thiasB!
- Introduce ``DataFrame`` object to improve internal data transfer.
- Backward compatibility for sensor type "system.battery-voltage".
- Improve cross-compilation for MicroPython 1.12, see #61. Thanks, @poesel!
- Fix Makefile target "install-pycom-firmware".
- Add GPRS modem support for SIM800. Thanks, @sarusso!
- Sandbox: Separate desktop notifications from tools/terkin.py.
  Fix nasty dependency bug on the "netaddr" module.
  Add gracefulness to "make notify" target.
- Adjust directory layout: Move "terkin" files to "lib" folder
- Adjust directory layout: Move root files to "src/" folder
- Support firmware image building for Genuine MicroPython
- Sandbox presets: "config.mk" is now "presets.mk"
- Upgrade to rshell 0.0.26
- Adjust directory layout: Move "lib/" folder inside "src/" folder
- Add missing "_boot.py" to custom MicroPython firmware images. Thanks, @poesel!
- Clean up rshell upload scripts for bytecode uploading
- Fix module search path computation in bootloader
- Stop messing with terminal on UART0 for now
- Add firmware builder machinery
- Add lowlevel driver for DS3231 RTC
- Upgrade to rshell 0.0.27
- Add basic test suite
- Adjust machinery to run under pytest
- Add tests for WiFi
- Add MQTT telemetry test. Needs running MQTT broker.
- Add ``pytest-docker-fixtures`` to invoke the MQTT telemetry tests
  against a Mosquitto broker running on Docker.
- Add test coverage reporting
- Skip Mosquitto/Docker integration tests on Windows/WSL
- Improve test suite re. Mosquitto dependency
- Add LoRaWAN tests
- Add tests covering sleep modes and maintenance mode
- Add tests covering sensor machinery
- Add tests covering GPRS telemetry
- Improve tests covering LoRaWAN message decoding with environmental sensors
- Update 3rd-party modules
- Fix flakyness of MQTT test
- Add tests covering HTTP uplink telemetry
- Use updated "umqtt" module for CPython compatibility
- Use "time.time()" rather than "time.time_ns()" to retain compatibility
  with Python3.6. Thanks, Matthias!
- Add new make targets for the testsuite to the inline Make documentation.
  Thanks, Markus!
- Improve error reporting for "make setup"
- Improve test coverage for HTTP telemetry / urequests module
- Add test coverage for "system.voltage.battery" by mocking the ADC
- Round sensor values according to settings
- Start supporting CPython on Linux/RaspberryPi. Thanks, @tonke!

2019-08-19 0.6.0
================
- Explicitly ``deinit()`` LTE modem on each startup
- Fix ``settings.example-bob.py``. Thanks, `@MKO1640`_ and `@ClemensGruber`_.
- Improve formatting of BEEP telemetry field mapping for BOB
- Disable telemetry adapter offline state for now
- Disable DEBUG log level for system sensors
- Add the "maintenance" device status / mode
- Add UDP mode server for signalling the device into maintenance mode
- Add device discovery and UDP client for signalling maintenance mode
- Attempt to fix woes with IPv6 addresses from ``terkin.py``
- Skip networks like 127.0.0.0/8 and 169.254.0.0/16 for ``terkin.py``
- Make "terkin.py" handle multiple MAC address prefixes
  coming from different Pycom devices. Now: WiPy, FiPy.
- Optionally read MAC address from command line in order to
  discover and maintain specific device
- Add MQTT authentication
- Update documentation
- Improve rshell access over IP
- Rename environment variable ``MCU_SERIAL_PORT`` to ``MCU_PORT``
  for configuring both USB/UART port and IP address
- Use offset values for DS18B20 sensors from settings
- Enable/disable individual sensors per settings
- Install MicroWebSrv and MicroDNSSrv libraries into ``dist-packages`` folder
- Add singleton factory method to ``TerkinDatalogger``. Thanks, `@DieDiren`_.
- Increase timeout for ARP ping requests with "terkin.py"
- Use most recent "dotty_dict" module
- Properly format MAC addresses
- Add maintenance mode interval to configuration settings
- Lazily import "ButtonManager" for trimming #11
- Improve MAC address parsing and formatting
- Improve MAC address normalization by also removing dashes and dots
- Follow the Pycopy MicroPython fork, standard library wise
- Upgrade to Dotty Dict 1.1.1. Thanks, `@pawelzny`_.
- Improve sandbox tooling incl. FTP source code upload
- DS18B20: Extend time between starting the
  conversion and reading the sensor to one second.
- Add MiniNet helper and corresponding ``Makefile`` rule ``wifi-connect``
- Ship configuration blueprint with deep sleep disabled
- Improve MiniNet helper to get IP address
- Set default maintenance duty cycle to 15 seconds
- Improve Watchdog subsystem by adjusting to edge cases. Thanks, `@pinguin999`_.
- Reorder sections when uploading using FTP
- Add Self-documenting-Makefile helper
- Improve Pycom firmware installation
- Slightly document Makefile targets
- Increase timeout when sending ARP packets for device discovery. Thanks, `@ClemensGruber`_.
- Slightly adjust "make help". More Makefile improvements.
- Desktop notifications for MicroTerkin Agent
- Make MicroTerkin Agent write detected IP address into file
- Improve Makefile sandbox tooling
- Prettify logging
- Optionally start modeserver, defaulting to true
- Add basic HTTP API subsystem. Thanks `@vkuhlen`_ and `@DieDiren`_.
- Add ``make provide-wifi`` command for starting the access point interactively
- Start WiFi in STA_AP mode by default
- Disable garbage collector when reading sensors to improve timing
- Improve tooling and inline documentation
- Add option ``main.fastboot`` for skipping LTE modem teardown
  for faster development iterations
- Curate the garbage collector
- Add backup mechanism for configuration files
- Fix polling for WiFi connectivity
- HTTP API: Add basic endpoints for configuration settings
- Add backup configuration snippet to settings blueprint files
- Makefile: Prompt for restart after FTP transfer
- Makefile: Add ``RUNNING_IN_HELL`` flag
- Makefile: Suppress desktop notifications on Windows for now
- Makefile-Todo: Use lftp.exe for file transfer on Windows?
- Extend module search path to "terkin" and "hiveeyes"
  folders in order to support native Pymakr operation
- Make reference to "datalogger" object available in global scope
- Slightly tweak garbage collector curator to collect
  garbage after computing and setting threshold
- Add more accessor methods to ``TerkinConfiguration``
- Add ``get_last_stacktrace`` utility function
- Fix memory exhaustion when starting the MicroWebSrv twice
- HTTP API: Add endpoints for getting and setting individual configuration settings
- Object model refactoring
- HTTP API: Add endpoint for getting the last reading
- Refactor ``sensors``-section of configuration settings
- Settings: Rename sensor "key" attribute to sensor "id"
- Settings: Rename HX711 enumeration attribute from "address" to "number"
- Fix broken dependencies re. ``pycopy-collections``
- Move HTTP API request/response examples to screenshots folder
- Constructor refactoring and naming things
- Add ``id`` attribute to bus configuration settings
- Refactor and improve DS18B20 settings, reading and processing
- Improve prettified sensor readings log output
- Improve HTTP API
- Improve initialization robustness with bus device objects
- Add ``mpy-cross-util.py``
- Add ahead-of-time compilation using ``mpy-cross``
  through ``make recycle-ng MPY_CROSS=true``
- Refactoring, documentation, cleanups, naming things
- Improve user experience with ``mpy-mk`` sandbox toolkit. Thanks, `@rohlan`_ and `@ClemensGruber`_.
  - Fix interactive confirmation
  - Add advices to guide user on errors
  - Improve Windows compatibility for the ``ng`` series of commands
- Add colors to ``mpy-mk``
- Add note about installing ``pycom-fwtool-cli`` on Linux. Thanks, weef.
- mpy-mk: Improve operating system detection
- mpy-mk: Streamline user interface
- Another attempt at touch button wakeup
- mpy-mk: Improve cross compilation
- sensors: Use BME280 library by robert-hh
- mpy-mk: Add "make colors" for colored output testing on Windows
- Make MicroTerkin Agent compatible with Python3.5. Thanks, `@rohlan`_.
- Attempt to automate installation of the modem firmware (WIP). Thanks, `@rohlan`_.
- Gracefully ignore missing "py-notifier" package on Linux. Thanks, `@rohlan`_.
- Fix ``scapy`` dependency woes. Thanks, `@rohlan`_.
- Add tools for building firmware images for ESP32 based on Pycom MicroPython.
  Thanks, `@emmanuel-florent`_.
- onewire.py: Use library optimized for timing and with enabled CRC checks by `@robert-hh`_, thanks!
- First steps with BLE (WIP)
- First steps with LTE (WIP)
- Be more graceful when starting network services
- Wrap "station.isconnected()" to mitigate unhandled exceptions on timeout errors
- Extend default watchdog timeout to 60 seconds
- Try two times to connect to WiFi station
- Makefile improvements
  - Don't run "mpy-cross-setup" on each invocation of "mpy-compile"
  - Don't clobber "mpy_cross_all.py"
- Improve LED signalling
- Parallelize networking subsystem
- Prepare real "light sleep" (WIP)
- Attempt to reset WiFi connection if scanning fails
- Add ``umal``, the Universal MicroPython Application Loader
- Reconfigure watchdog when connecting the device using MiniNet
- Propagate platform information for implementing platform switch conditions
- Transfer ``umal`` bootloader and the ``mininet`` module to the ``lib`` folder
- Start making Terkin platform-agnostic. Thanks, Markus!
- Add release archives with frozen modules compatible to Pycom MicroPython


2019-06-22 0.5.1
================
- HX711: Configure data pin as pull-up to be able to detect readiness
- Disable Watchdog in blueprint settings
- Improve logging and terminal handling in bootstrap phase
- Improve release bundling


2019-06-22 0.5.0
================

**Power saving.**

- Improve documentation
- Improve voltage divider settings for reading the battery level
- Package the release bundle with the same directory layout as the sandbox
- Add foundation for having button events through ESP32 touch pads
- Add basic logging configuration settings to support turning off logging entirely
- Fix purging of sensible configuration keys
- Improve MAC address formatting when logging network status
- Try 11 dB attenuation for measuring vcc
- Disable heartbeat through RGB-LED, just blink twice on startup
- Turn off interrupts while powering down the HX711
- Improve inline documentation and logging
- Improve IRQ handling when reading the HX711
- Sleep for 80 microseconds after pulling HX711 clock pin ``PD_SCK`` to HIGH
- Improve bus- and sensor power-management. Add "power_on" signal.
- Explicitly turn off LTE modem before deep sleep
- Use 6dB attenuation factor again when reading the ADC for measuring VCC
- Conditionally turn off LTE modem
- WiFi STA: Get hold of auth mode and store into NVRAM to skip WiFi scan on each cycle
- WiFi STA: Erase auth mode from NVRAM if connection fails
- Refactor radio/networking subsystem
- Explicitly start and stop Terminal on UART0 based on configuration
- HX711: Hold clock pin "PD_SCK" in designated state through internal
  pull-up in the RTC-domain, even during deep sleep.
- HX711: Improve setup and initialization after power up
- Add watchdog and feed it


2019-06-17 0.4.0
================

**Getting real.**

- Upgrade to ``Pycom MicroPython 1.20.0.rc11``
- Stop leaking sensible information into settings output
- Improve documentation
- Switch to LittleFS
- Add deep sleep
- Improve Makefile targets
- Add more wakeup reasons
- Add missing configuration section for HX711 to settings example.
  Thanks, `@ClemensGruber`_.
- Add basic device-interval sensors ``SystemTemperature`` and ``SystemBatteryLevel``
- Explicitly shut down all peripherals having implicitly been turned on
- Add ``SystemWiFiMetrics`` sensor
- Add ``SystemUptime`` sensor
- Fix: Better explicitly initialize the ADC before reading it
- Improve ``SystemBatteryLevel`` sensor. Thanks, `@ayoy`_.
- Make ``TelemetryTransportHTTP`` work again
- Improve telemetry subsystem re. multi-protocol and -topology. Enable HTTP telemetry.
- Add configuration example for BEEP-BOB ``settings.example-bob.py``
- Honor "scale" and "offset" parameters when reading the HX711. Fix #6.
- Improve reading the HX711 re. wrong kg scaling.
  Transmit all raw values and settings of HX711.
- Attempt to improve #5: Reading Vcc.
- Add missing "topology" configuration settings attribute
  for MQTT telemetry to example configurations
- Fix deep sleep
- Conditionally start telemetry subsystem just if networking is available
- Improve robustness wrt. WiFi connectivity
- Improve log messages
- Bump version to 0.4.0dev
- Improve purging of sensible configuration settings
- SystemBatteryLevel: Obtain voltage divider parameters from settings
- Improve release tooling
- Improve error signalling for missing "topology" configuration setting


2019-06-07 0.3.0
================

**Yaks all the way down.**

- Add ds18x20 lib
- Implement DS and HX sensors using ``AbstractSensor``
- ds18x20: Add reading multiple sensors
- Populate SensorManager, add bus management, add OneWireBus
- SensorManager: Make ds18x20 use OneWire-Bus through ``AbstractBus``
- ds18x20: fix runtime issues, resetting OneWire before scanning for devices
- Little cleanup
- SensorManager
    - Add bus driver for i2c and onewire buses
    - Settings: add buses to (sensor-)settings
    - Convention: Bus address ``<BUS_FAMILY>:<BUS_NUMBER>``
- Makefile|libs:
    - Add bme280, Pycoproc, Quectel L76 GNSS library (Pytrack Board)
    - Add Pytrack Board Library, Pytrack Board Accelerator
- SensorManager
    - Add bus to sensor registry
    - Add bme280 (humidity, temperature, pressure)
    - Add i2c bus
    - Cleanups
- Compensate for missing ``_onewire`` package, maybe on older firmwares
- Move acquire_bus to ``AbstractSensor``
- Fix I2C pin propagation
- Add Pytrack sensor
- Don't croak on failures
- Fix HX711 pin wiring
- Move Pytrack sensor to ratrack namespace
- Add Pytrack Quectel L76 GNSS sensor
- Makefile: cleanup (rm old DS18X20 lib)
- settings|sensor: add TODO: "i2c-address -> settings -> sensor"
- settings|sensor: add TODO: "i2c-address -> settings -> sensor"
- Sensors: naming, (WIP!) hardcoded proposal for naming (see bme280)
- Add Pytrack support
- Moar sensors
- Add appropriate logging
- Improve LoRa subsystem
- Improve logging, code cosmetics
- Add "make clean" target
- Enable all sensors
- Improve bus registration
- Improve BME280 readings
- Improve documentation
- Update documentation
- Add LoRaWAN/TTN telemetry with CayenneLPP
- Start WiFi before LoRaWAN
- Reduce logging noise
- Improve sandbox, documentation and naming things
- Update documentation
- Remove main.py.dist again
- Improve automatic sensor field naming
- Improve example settings
- Improve logging all over the place
- Upgrade to rshell 0.0.21
- Use “device_id” as part of the MQTT “client_id”
- Fix telemetry success signalling
- Cleanup
- Improve network/telemetry error handling, robustness
  and convenience for WiFi and MQTT connectivity
- Improve logging
- Update documentation
- Improve reporting about which telemetry targets succeeded


2019-03-23 0.2.1
================

**Fixes.**

- Fix install-requirements re. dotty_dict patching
- Fix "make list-serials"
- Dependencies: add OneWire & DS18x20 libraries
- Fix urllib dep
- Introduce SensorManager
- Fix urllib dep


2019-03-17 0.2.0
================

**Fill in the gaps, lots of.**

- Update documentation
- Update backlog
- Improve MQTT robustness by compensating ``ECONNRESET`` and ``ECONNABORTED`` exceptions
  from connection to MQTT broker by attempting to transparently reconnect next time when
  performing a telemetry submission.
- Stop connecting to further WiFi networks after getting connected already
- Make the telemetry domain obtain the "format" parameter from
  configuration settings in order to control the serialization method.
- Update MQTT address example settings
- Improve WiFi STA connectivity and status reporting
- Improve status reporting and inline comments
- Fix example configuration
- Improve documentation
- Preparing cayenneLPP into telemetry, new convention for sensor mapping (e.g. channel in CayenneLPP)
- Lora works now, cleaning up and restructuring, might be good
- Add TTN to get_handler() and transmit()
- Improve telemetry target selector
- Add PyCayenneLPP package to foundation libraries
- Add telemetry target for running Base64-encoded CayenneLPP over MQTT
- install upip via pypi
- Add project header to main sketch files
- Improve PyCayenneLPP installation
- Reduce rshell buffer size to "30"
- Improve Telemetry - Multiple telemetry sinks running in parallel - Add MQTT driver adapter
- Streamline sensor reading vs. telemetry submission
- Trim configuration settings output
- Naming things
- Improve documentation
- Fix channel naming in example configuration
- Skip reporting the current configuration settings as this crashes the serial output on WSL.
- Use environment variable "MCU_SERIAL_PORT" for configuring serial port
- Overhaul make target "setup-requirements" to populate "dist-packages"
- Update documentation, improve README and add README-HARDWARE.md
- Improve "refresh-requirements" make target
- Documentation, once more
- Bump documentation again
- Slight application namespace refactoring
- Improve reporting
- Don't enable serial device in "boot.py"
- Improve documentation
- Add examples for different use cases
- Build distribution archive files and upload them to GitHub
- Refactoring/modularization
- Update documentation
- Minor fixes
- Re-add BobDatalogger
- Add release tooling


2019-03-14 0.1.0
================

**Architecture blueprint. Works, sort of.**

- Add build environment
- Begin with documentation
- Large refactoring
- Remove "urllib" package as we might want to pull it back in using "upip" later.
- Add dependency management through "dist-packages" folder by using "upip" with MicroPython on Unix
- Improve framework layout
- Improve robustness of TelemetryClient
- Add DummySensor
- Add MemoryFree sensor
- Update documentation
- Add vanilla ``hx711.py`` by `David Gerber`_
- Add improved HX711 library by `Ralf Lindlein`_
- Improve documentation
- Code cosmetics, improve logging
- Add HX711 sensor component
- Update documentation and tooling
- Improve HX711 sensor robustness, don't block the device driver while waiting for hardware intercom
- Add watchdog timer (WDT) support
- Idle in the mainloop
- Naming things
- Run garbage collector on each loop iteration
- Prepare RTC code
- Ignore empty sensor readings
- Naming things, HX711 robustness
- Add vanilla Dotty Dict package
- Add basic TTN example
- TTN for real?
- Improve configuration system and WiFi STA connectivity
- Update documentation
- This and that
- Troubleshooting git errors, whatever, need to commit
- Add LoRaWAN (TTN) flavour to terking devices
- this and that, still WIP, not working
- WIP: code is running, but not connected to TTN successfull
- Lora works now, cleaning up and restructuring, might be good
- Resolve urllib dependency woes
- Use telemetry parameters from configuration settings
- This and that
- Use sensor parameters from configuration settings
- Increase number of retry attempts for catching a WiFi connection, essentially checking for 15 seconds
- Update documentation
- Refactor LoRaWAN bootstrapping


2019-03-01 0.0.0
================

**Baby steps.**

- Initial commit
- Add .gitignore to exclude ``*_local.py`` configuration files
- WIP: Hands on FiPy
- First stable version


.. _David Gerber: https://github.com/geda
.. _Ralf Lindlein: https://github.com/walterheisenberg
.. _@ClemensGruber: https://github.com/ClemensGruber
.. _@MKO1640: https://github.com/MKO1640
.. _@DieDiren: https://github.com/DieDiren
.. _@vkuhlen: https://github.com/vkuhlen
.. _@pawelzny: https://github.com/pawelzny/
.. _@ayoy: https://github.com/ayoy
.. _@pinguin999: https://github.com/pinguin999
.. _@rohlan: https://github.com/rohlan
.. _@emmanuel-florent: https://github.com/emmanuel-florent
.. _@robert-hh: https://github.com/robert-hh/
