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
