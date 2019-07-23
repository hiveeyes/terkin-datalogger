# ***********************
# The MicroTerkin sandbox
# ***********************

# See also https://community.hiveeyes.org/t/terkin-for-micropython/233/21


# =============
# Initial setup
# =============
#
# Refresh sources and dependencies::
#
#   git pull
#   make setup
#
# Establish network connectivity::
#
#   export MCU_PORT=/dev/cu.usbmodemPy001711
#   make connect-wifi ssid=YourNetwork password=YourPassword
#
# Transfer files::
#
#   export MCU_PORT=192.168.178.33
#   make install-ftp
#
# Watch log output::
#
#   make console
#
# Start over::
#
#   -- Press reset button
#   -- Have fun


# ================
# Maintenance mode
# ================
#
# When the device is already running, it is already attached to a network.
# So, to make it stay connected and pull it out of deep sleep, you might
# want to adjust one step in the procedure above.
#
# Establish network connectivity::
#
#   make terkin-agent action=maintain
#


# =============
# Main Makefile
# =============

# Load modules
include tools/help.mk
include tools/core.mk
include tools/setup.mk
include tools/release.mk

include tools/terkin.mk
include tools/pycom.mk
include tools/micropython.mk


# -----
# Setup
# -----
## Prepare sandbox environment and download requirements
setup: setup-environment download-requirements


# -----------------------
# Discovery & Maintenance
# -----------------------

setup-terkin-agent:
	$(pip3) install -r requirements-terkin-agent.txt

.PHONY: terkin-agent
## Run the MicroTerkin Agent, e.g. "make terkin-agent action=maintain"
terkin-agent: setup-terkin-agent
	sudo $(python3) tools/terkin.py $(action) $(macs)

## Load the MiniNet module to the device and start a WiFi access point.
provide-wifi:
	@$(rshell) $(rshell_options) --quiet cp lib/mininet.py /flash/lib
	@$(rshell) $(rshell_options) --quiet repl "~ from mininet import MiniNet ~ MiniNet().activate_wifi_ap()"
	@echo

## Load the MiniNet module to the device and start a WiFi STA connection.
connect-wifi:
	@$(rshell) $(rshell_options) --quiet cp lib/mininet.py /flash/lib
	@$(rshell) $(rshell_options) --quiet repl "~ from mininet import MiniNet ~ MiniNet().connect_wifi_sta('$(ssid)', '$(password)')"
	@echo

## Load the MiniNet module to the device and get IP address.
ip-address:
	@$(rshell) $(rshell_options) --quiet cp lib/mininet.py /flash/lib
	@$(rshell) $(rshell_options) --quiet repl "~ from mininet import MiniNet ~ print(MiniNet().get_ip_address()) ~"
	@echo


# -----------------------
# File transfer & Execute
# -----------------------

## Upload framework, program and settings and restart attached to REPL
recycle: install-framework install-sketch reset-device-attached

## Upload framework, program and settings and restart device
recycle-ng: install-ng

	@# Conditionally
	@#$(MAKE) sleep

	@# Prompt the user for action.
	$(eval retval := $(shell bash -c 'read -s -p "Restart device using the HTTP API [y/n]? " outcome; echo $$outcome'))
	@if test "$(retval)" = "y"; then \
		echo; \
		$(MAKE) restart-device; \
	else \
		echo; \
	fi

## Upload program and settings and restart attached to REPL
sketch-and-run: install-sketch reset-device-attached

## Restart device using the HTTP API
restart-device:
	$(eval ip_address := $(shell cat .terkin/floatip))

	@# Notify user about the power cycling.
	@$(MAKE) notify status=INFO message="Restarting device at IP address $(ip_address) using HTTP API"

	@# Send restart command to HTTP API
	@# TODO: If this fails, maybe reset automatically using the serial interface.
	$(eval response := $(shell http --check-status --timeout=3 POST "http://$(ip_address)/restart" 2> /dev/null || (echo "Your command failed with $$?")))

	@# Evaluate response
	@if test "${response}" = "ACK"; then \
		$(MAKE) notify status=SUCCESS message="Device restart acknowledged. Please wait some seconds for reboot."; \
	else \
		$(MAKE) notify status=ERROR message="Device restart using HTTP API failed. Try using a different method."; \
	fi

	@# TODO: Actually check if device becomes available again before signalling readyness.
	@echo "Ready."


notify:
	@echo "$(status): $(message)"
	@if test "${RUNNING_IN_HELL}" != "true"; then \
		$(python3) tools/terkin.py notify "$(message)" "$(status)"; \
	fi


# ------------------
# File transfer solo
# ------------------

## Install all files to the device, using rshell
install: install-requirements install-framework install-sketch

## Install all files to the device, using FTP
install-ftp:
	lftp -u micro,python ${mcu_port} < tools/upload-all.lftprc
	@echo "lftp status: $$?"

sleep:
	@sleep 1

## Install all files to the device, using best method
install-ng: check-mcu-port

	@# User notification
	$(MAKE) notify status=INFO message="Uploading MicroPython code to device"

	@if test "${mcu_port_type}" = "ip"; then \
		$(MAKE) install-ftp; \
	elif test "${mcu_port_type}" = "usb"; then \
		$(MAKE) install; \
	fi

	@# User notification
	$(MAKE) notify status=INFO message="MicroPython code upload finished"

install-requirements: check-mcu-port
	$(rshell) $(rshell_options) mkdir /flash/dist-packages
	$(rshell) $(rshell_options) rsync dist-packages /flash/dist-packages

install-framework: check-mcu-port
	$(rshell) $(rshell_options) --file tools/upload-framework.rshell

install-sketch: check-mcu-port
	$(rshell) $(rshell_options) --file tools/upload-sketch.rshell

refresh-requirements: check-mcu-port
	rm -r dist-packages
	$(MAKE) download-requirements
	$(rshell) $(rshell_options) rm -r /flash/dist-packages
	$(rshell) $(rshell_options) ls /flash/dist-packages
	$(MAKE) install-requirements


# ------------
# Applications
# ------------
terkin: install-terkin
ratrack: install-ratrack

terkin: check-mcu-port
	@#$(rshell) $(rshell_options) --file tools/upload-framework.rshell
	$(rshell) $(rshell_options) --file tools/upload-terkin.rshell

ratrack: check-mcu-port
	# $(rshell) $(rshell_options) --file tools/upload-framework.rshell
	$(rshell) $(rshell_options) --file tools/upload-ratrack.rshell



# ---------
# Releasing
# ---------

#release-and-publish: release publish-release

# Release this piece of software.
# Synopsis:
#   "make release bump=minor"   (major,minor,patch)
release: bumpversion push publish-release
