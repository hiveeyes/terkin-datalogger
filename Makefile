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
include tools/bluetooth.mk


# ----
# Help
# ----
.DEFAULT_GOAL := help

help: show-rules
	@echo "$$(tput bold)Documentation:$$(tput sgr0)"
	@echo
	@echo "Please check https://community.hiveeyes.org/t/operate-the-terkin-datalogger-sandbox/2332 "
	@echo "in order to get an idea how to operate this software sandbox."
	@echo
	@echo "Have fun!"
	@echo


# -----
# Setup
# -----
## Prepare sandbox environment and download requirements
setup: setup-environment download-requirements mpy-cross-setup


# -----------------------
# Discovery & Maintenance
# -----------------------

setup-terkin-agent:
	$(pip3) install --pre --requirement requirements-terkin-agent.txt

## Run the MicroTerkin Agent, e.g. "make terkin-agent action=maintain"
terkin-agent: setup-terkin-agent
	sudo $(python3) tools/terkin.py $(action) $(macs)

## Load the MiniNet module to the device and start a WiFi access point.
provide-wifi: check-mcu-port
	@$(rshell) $(rshell_options) --quiet cp lib/mininet.py /flash/lib
	@$(rshell) $(rshell_options) --quiet repl "~ from mininet import MiniNet ~ MiniNet().activate_wifi_ap()"
	@echo

## Load the MiniNet module to the device and start a WiFi STA connection.
connect-wifi: check-mcu-port
	@$(rshell) $(rshell_options) --quiet cp lib/mininet.py /flash/lib/mininet_wip.py
	@$(rshell) $(rshell_options) --quiet repl "~ from mininet_wip import MiniNet ~ MiniNet().connect_wifi_sta('$(ssid)', '$(password)')"
	@echo

## Load the MiniNet module to the device and get IP address.
ip-address: check-mcu-port
	@$(rshell) $(rshell_options) --quiet cp lib/mininet.py /flash/lib
	@$(rshell) $(rshell_options) --quiet repl "~ from mininet import MiniNet ~ print(MiniNet().get_ip_address()) ~"
	@echo


# -----------------------------
# File compilation and transfer
# -----------------------------

## Compile all library files using mpy-cross
mpy-compile: check-mpy-version check-mpy-target

	@echo "$(INFO) Ahead-of-time compiling to .mpy $(MPY_TARGET)"

	$(eval mpy_path := lib-mpy-$(MPY_VERSION)-$(MPY_TARGET))

	@echo "$(INFO) Populating folder \"$(mpy_path)\""
	@rm -rf $(mpy_path)

	@if test "${MPY_TARGET}" = "pycom"; then \
		$(MAKE) mpy-cross what="--out $(mpy_path) dist-packages"; \
	fi
	@$(MAKE) mpy-cross what="--out $(mpy_path) lib"
	@$(MAKE) mpy-cross what="--out $(mpy_path)/terkin terkin"

	@echo "$(INFO) Size of $(mpy_path):"
	@du -sch $(mpy_path)

## Upload framework, program and settings and restart attached to REPL
recycle: install-framework install-sketch reset-device-attached

## Upload framework, program and settings and restart device
recycle-ng: install-ng

	# Restart device after prompting the user for confirmation.
	@echo
	@echo "$(WARNING) It is crucial all files have been transferred successfully before restarting the device."
	@echo "          Otherwise, chances are high the program will crash after restart."
	@echo
	@echo "$(ADVICE) You might want to check the output of the file transfer process above for any errors."
	@echo

	@if test "${mcu_port_type}" = "ip"; then \
		$(MAKE) confirm text="Restart device using the HTTP API?" && \
		$(MAKE) restart-device-http; \
	elif test "${mcu_port_type}" = "usb"; then \
		$(MAKE) confirm text="Restart device using the REPL?" && \
		$(MAKE) reset-device; \
	fi


## Upload program and settings and restart attached to REPL
sketch-and-run: install-sketch reset-device-attached

## Pyboard-D transfer
pyboard-install: check-mpy-version check-mpy-target

	@$(MAKE) mpy-compile

	# Inactive
	@#rsync -auv dist-packages lib-mpy terkin boot.py main.py settings.py /Volumes/PYBFLASH; \

	@if test -e "/Volumes/PYBFLASH"; then \
		rsync -auv lib/umal.py lib/mininet.py /Volumes/PYBFLASH/lib; \
		rsync -auv lib-mpy-$(MPY_VERSION)-$(MPY_TARGET) /Volumes/PYBFLASH; \
		rsync -auv boot.py main.py /Volumes/PYBFLASH; \
		cp settings.pybd.py /Volumes/PYBFLASH/settings.py; \
	else \
		echo "ERROR: Could not find /Volumes/PYBFLASH, exiting"; \
		exit 1; \
	fi

pyboard-reset: check-mcu-port-strict
	@diskutil unmount /Volumes/PYBFLASH || true
	@$(MAKE) reset-device
	@sleep 2
	@$(MAKE) console

pyboard-recycle: pyboard-install pyboard-reset


# ------------------
# File transfer solo
# ------------------

## Install all files to the device, using rshell
install: install-requirements install-framework install-sketch

## Install all files to the device, using FTP
install-ftp:

	@if test "${mpy_cross}" = "true"; then \
		$(MAKE) mpy-compile && \
		$(MAKE) lftp lftp_recipe=tools/upload-mpy-$(MPY_VERSION).lftprc; \
	else \
		$(MAKE) lftp lftp_recipe=tools/upload-all.lftprc; \
	fi

## Install all files to the device, using USB (rshell)
install-rshell:

	@if test "${mpy_cross}" = "true"; then \
		$(MAKE) mpy-compile && \
		$(rshell) $(rshell_options) --file tools/upload-mpy.rshell; \
	else \
		$(MAKE) install; \
	fi

## Install all files to the device, using best method
install-ng: check-mcu-port

	@if test "${mcu_port_type}" = "ip"; then \
		$(MAKE) notify status=INFO status_ansi="$(INFO)" message="Uploading MicroPython code to device using FTP" && \
		$(MAKE) install-ftp; \
	elif test "${mcu_port_type}" = "usb"; then \
		$(MAKE) notify status=INFO status_ansi="$(INFO)" message="Uploading MicroPython code to device using USB" && \
		$(MAKE) install-rshell; \
	fi

	@# User notification
	@$(MAKE) notify status=OK status_ansi="$(OK)" message="MicroPython code upload finished"

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

build-annapurna:
	docker run -v `pwd`/dist-packages:/opt/frozen -it goinvent/pycom-fw build FIPY annapurna-0.6.0dev2 v1.20.0.rc12.1 idf_v3.1


#release-and-publish: release publish-release

# Release this piece of software.
# Synopsis:
#   "make release bump=minor"   (major,minor,patch)
release: bumpversion push publish-release
