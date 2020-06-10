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

# Conditionally load "presets.mk".
MAKE_PRESETS := $(shell test -e "presets.mk" && echo "yes")
ifeq ($(MAKE_PRESETS),yes)
	include presets.mk
endif

# Load modules
include tools/help.mk
include tools/base.mk
include tools/setup.mk
include tools/build.mk
include tools/docs.mk
include tools/release.mk

include tools/terkin.mk
include tools/pycom.mk
include tools/micropython.mk
include tools/bluetooth.mk

include tools/cpython.mk


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



# -----------------------------
# File compilation and transfer
# -----------------------------

## Compile all library files using mpy-cross
mpy-compile: check-mpy-version check-mpy-target

	@echo "$(INFO) Ahead-of-time compiling to .mpy $(MPY_TARGET)"

	$(eval mpy_path := lib-mpy)

	@echo "$(INFO) Populating folder \"$(mpy_path)\""
	@rm -rf $(mpy_path)

	@$(MAKE) mpy-cross what="--out $(mpy_path) dist-packages"
	@$(MAKE) mpy-cross what="--out $(mpy_path) src/lib"

	@echo "$(INFO) Size of $(mpy_path):"
	@du -sch $(mpy_path)

## Upload framework, program and settings and restart attached to REPL
recycle: install-framework install-sketch reset-device-attached

## Upload framework, program and settings and restart device
recycle-ng: install-ng

	@# Restart device after prompting the user for confirmation.
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
		$(MAKE) console; \
	fi


## Upload program and settings and restart attached to REPL
sketch-and-run: install-sketch reset-device-attached

## Pyboard-D transfer
pyboard-install: check-mpy-version check-mpy-target

	@$(MAKE) mpy-compile

	# Inactive
	@#rsync -auv dist-packages lib-mpy src/boot.py src/main.py src/settings.py /Volumes/PYBFLASH; \

	@if test -e "/Volumes/PYBFLASH"; then \
		rsync -auv src/lib/umal.py src/lib/mininet.py /Volumes/PYBFLASH/lib; \
		rsync -auv lib-mpy /Volumes/PYBFLASH; \
		rsync -auv src/boot.py src/main.py /Volumes/PYBFLASH; \
		cp src/settings.pybd.py /Volumes/PYBFLASH/settings.py; \
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
		$(MAKE) lftp lftp_recipe=tools/upload-mpy-$(MPY_TARGET).lftprc; \
	else \
		$(MAKE) lftp lftp_recipe=tools/upload-all.lftprc; \
	fi

## Install all files to the device, using USB (rshell)
install-rshell:

	@if test "${mpy_cross}" = "true"; then \
		$(MAKE) mpy-compile && \
		if test "${MPY_TARGET}" = "pycom"; then \
			$(rshell) $(rshell_options) --file tools/upload-mpy-pycom.rshell; \
		else \
			$(rshell) $(rshell_options) --file tools/upload-mpy-genuine.rshell; \
		fi; \
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
	@if test "${MPY_TARGET}" = "pycom"; then \
		$(rshell) $(rshell_options) mkdir /flash/dist-packages; \
		$(rshell) $(rshell_options) rsync --mirror dist-packages /flash/dist-packages; \
	else \
		$(rshell) $(rshell_options) mkdir /pyboard/dist-packages; \
		$(rshell) $(rshell_options) rsync --mirror dist-packages /pyboard/dist-packages; \
	fi

install-framework: check-mcu-port
	@if test "${MPY_TARGET}" = "pycom"; then \
		$(rshell) $(rshell_options) --file tools/upload-framework-pycom.rshell; \
	else \
		$(rshell) $(rshell_options) --file tools/upload-framework-genuine.rshell; \
	fi

install-sketch: check-mcu-port
	@if test "${MPY_TARGET}" = "pycom"; then \
		$(rshell) $(rshell_options) --file tools/upload-sketch-pycom.rshell; \
	else \
		$(rshell) $(rshell_options) --file tools/upload-sketch-genuine.rshell; \
	fi

refresh-requirements: check-mcu-port
	@rm -r dist-packages
	$(MAKE) download-requirements
	@if test "${MPY_TARGET}" = "pycom"; then \
		$(rshell) $(rshell_options) rm -r /flash/dist-packages; \
		$(rshell) $(rshell_options) ls /flash/dist-packages; \
	else; \
		$(rshell) $(rshell_options) rm -r /pyboard/dist-packages; \
		$(rshell) $(rshell_options) ls /pyboard/dist-packages; \
	fi
	$(MAKE) install-requirements


# ------------
# Applications
# ------------
terkin-and-run: check-mcu-port
	$(MAKE) install-framework
	$(MAKE) reset-device-attached

ratrack-and-run: check-mcu-port
	$(MAKE) install-framework
	$(MAKE) reset-device-attached
