# Copy this file to "presets.mk" in order to set preferences for your sandbox environment.
# Any variables defined on the user environment will override the settings specified here.
#
# Example: Adjust serial port by saying
# export MCU_PORT=/dev/cu.usbmodemPy001711


# The serial port the device is attached to.
MCU_PORT ?= /dev/ttyS3

# Whether to cross-compile to bytecode.
MPY_CROSS ?= true

# Use "bytecode" or "pycom" here for Genuine MicroPython vs. Pycom MicroPython.
MPY_TARGET ?= pycom

# Specify MicroPython version.
MPY_VERSION ?= 1.11


# Firmware building
FWB_XTENSA_GCC ?= /path/to/xtensa-esp32-elf-1.22.0-98/bin

# Genuine MicroPython
FWB_MICROPYTHON_GENUINE ?= /path/to/micropython
FWB_ESPIDF_GENUINE ?= /path/to/esp-idf

# Pycom MicroPython
FWB_MICROPYTHON_PYCOM ?= /path/to/pycom-micropython-sigfox
FWB_ESPIDF_PYCOM ?= /path/to/pycom-esp-idf
