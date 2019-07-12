#######################################
Hiveeyes MicroPython Datalogger CHANGES
#######################################


Development
===========
- Explicitly ``deinit()`` LTE modem on each startup
- Fix ``settings.example-bob.py``. Thanks, @MKO1640 and @ClemensGruber!
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
- Add singleton factory method to ``TerkinDatalogger``. Thanks, @DieDiren.
- Increase timeout for ARP ping requests with "terkin.py"
- Use most recent "dotty_dict" module
- Properly format MAC addresses
- Add maintenance mode interval to configuration settings


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
  Thanks, @ClemensGruber.
- Add basic device-interval sensors ``SystemTemperature`` and ``SystemBatteryLevel``
- Explicitly shut down all peripherals having implicitly been turned on
- Add ``SystemWiFiMetrics`` sensor
- Add ``SystemUptime`` sensor
- Fix: Better explicitly initialize the ADC before reading it
- Improve ``SystemBatteryLevel`` sensor. Thanks, `Dominik <https://github.com/ayoy>`_!
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
    - Add bus driver for i2c and onewire busses
    - Settings: add busses to (sensor-)settings
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
- Add vanilla hx711.py by David Gerber
- Add improved HX711 library by Ralf Lindlein
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
- Add vanilla "dotty_dict" package
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
- Add .gitignore to exclude `*_local.py` configuration files
- WIP: Hands on FiPy
- First stable version
