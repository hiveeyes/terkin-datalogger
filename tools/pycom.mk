# ======================
# Pycom firmware updater
# ======================
$(eval pycom_fwtool_cli_macos := /Applications/Pycom\ Firmware\ Update.app/Contents/Resources/pycom-fwtool-cli)
$(eval pycom_fwtool_cli_windows := /mnt/c/Program\ Files\ \(x86\)/Pycom/Pycom\ Firmware\ Update/pycom-fwtool-cli.exe)

PYCOM_MACOS := $(or $(and $(wildcard $(pycom_fwtool_cli_macos)),1),0)
PYCOM_WINDOWS := $(or $(and $(wildcard $(pycom_fwtool_cli_windows)),1),0)

ifeq ($(PYCOM_MACOS),1)
	pycom_fwtool_cli := $(pycom_fwtool_cli_macos)
	pycom_firmware_port := $(mcu_port)
endif
ifeq ($(PYCOM_WINDOWS),1)
	pycom_fwtool_cli := $(pycom_fwtool_cli_windows)
        pycom_firmware_port :=$(subst /dev/ttyS, COM, $(mcu_port))
endif

check-pycom-fwtool:
	@if test "${pycom_fwtool_cli}" = ""; then \
		echo "ERROR: Pycom Firmware Updater not found"; \
		exit 1; \
	else \
		echo "INFO: Found Pycom Firmware Updater at $(pycom_fwtool_cli)"; \
	fi


# ===============
# Pycom utilities
# ===============

pycom_firmware_file := FiPy-1.20.0.rc11.tar.gz

# Download Pycom firmware to your workstation
download-pycom-firmware:

	@# Define path to the "dist-packages" installation directory.
	$(eval target_dir := ./dist-firmwares)
	@#$(eval fetch := wget --no-clobber --unlink --directory-prefix)
	$(eval fetch := wget --no-clobber --unlink)

	@mkdir -p $(target_dir)
	@#$(fetch) $(target_dir) https://github.com/pycom/pycom-micropython-sigfox/releases/download/v1.20.0.rc12/FiPy-1.20.0.rc12-application.elf

	$(fetch) --output-document=$(target_dir)/$(pycom_firmware_file) https://software.pycom.io/downloads/$(pycom_firmware_file) | true

## Display chip_id
chip_id: check-mcu-port
	$(pycom_fwtool_cli) --port $(pycom_firmware_port) chip_id

## Install Pycom firmware on device
install-pycom-firmware: download-pycom-firmware

	@if test "${mcu_port_type}" = "ip"; then \
		echo; \
		echo "ERROR: Unable to install firmware over IP"; \
		exit 1; \
	fi

	# Prompt the user for action.
	$(eval retval := $(shell bash -c 'read -s -p "Install Pycom firmware \"$(pycom_firmware_file)\" on the device connected to \"$(pycom_firmware_port)\" [y/n]? " outcome; echo $$outcome'))
	@if test "$(retval)" = "y"; then \
		echo; \
		\
		echo Installing firmware $(pycom_firmware_file); \
		$(pycom_fwtool_cli) --verbose --port $(pycom_firmware_port) flash --tar dist-firmwares/$(pycom_firmware_file); \
	else \
		echo; \
	fi

## Format flash filesystem with LittleFS
format-flash: check-mcu-port

	@# Old version
	@# $(rshell) $(rshell_options) --file tools/clean.rshell

	# Prompt the user for action.
	$(eval retval := $(shell bash -c 'read -s -p "Format /flash on the device with LittleFS? THIS WILL DESTROY DATA ON YOUR DEVICE. [y/n]? " outcome; echo $$outcome'))
	@if test "$(retval)" = "y"; then \
		echo; \
		\
		echo Creating LittleFS filesystem; \
		$(rshell) $(rshell_options) --quiet repl pyboard 'import pycom ~ pycom.bootmgr(fs_type=pycom.LittleFS, reset=True) ~'; \
		\
		echo Formatting filesystem; \
		$(rshell) $(rshell_options) --quiet repl pyboard 'import os ~ os.fsformat(\"/flash\") ~'; \
		\
		echo Resetting device; \
		$(rshell) $(rshell_options) --quiet repl pyboard 'import machine ~ machine.reset() ~'; \
	else \
		echo; \
	fi

## Erase flash filesystem
erase-fs: check-mcu-port
	# Prompt the user for action.
	$(eval retval := $(shell bash -c 'read -s -p "Erase the filesystem on the device? THIS WILL DESTROY DATA ON YOUR DEVICE. [y/n]? " outcome; echo $$outcome'))
	@if test "$(retval)" = "y"; then \
		echo; \
		\
		echo Erasing filesystem; \
		$(pycom_fwtool_cli) --port ${pycom_firmware_port} erase_fs; \
	else \
		echo; \
	fi
