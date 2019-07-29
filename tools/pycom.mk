# ======================
# Pycom firmware updater
# ======================
$(eval pycom_fwtool_cli_macos := /Applications/Pycom\ Firmware\ Update.app/Contents/Resources/pycom-fwtool-cli)
$(eval pycom_fwtool_cli_windows := /mnt/c/Program\ Files\ \(x86\)/Pycom/Pycom\ Firmware\ Update/pycom-fwtool-cli.exe)
$(eval pycom_fwtool_cli_linux := /usr/local/bin/pycom-fwtool-cli)

PYCOM_MACOS := $(or $(and $(wildcard $(pycom_fwtool_cli_macos)),1),0)
PYCOM_WINDOWS := $(or $(and $(wildcard $(pycom_fwtool_cli_windows)),1),0)
PYCOM_LINUX := $(or $(and $(wildcard $(pycom_fwtool_cli_linux)),1),0)

ifeq ($(PYCOM_MACOS),1)
	pycom_fwtool_cli := $(pycom_fwtool_cli_macos)
	pycom_firmware_port := $(mcu_port)
endif
ifeq ($(PYCOM_WINDOWS),1)
	pycom_fwtool_cli := $(pycom_fwtool_cli_windows)
	pycom_firmware_port :=$(subst /dev/ttyS, COM, $(mcu_port))
endif
ifeq ($(PYCOM_LINUX),1)
	pycom_fwtool_cli := $(pycom_fwtool_cli_linux)
	pycom_firmware_port := $(mcu_port)
endif

check-pycom-fwtool:
	@if test "${pycom_fwtool_cli}" != ""; then \
		echo "INFO: Found Pycom Firmware Updater at \"$(pycom_fwtool_cli)\""; \
	else \
		echo; \
		echo "$(ERROR) Pycom Firmware Updater not found"; \
		echo; \
		echo "$(ADVICE) Please go to https://docs.pycom.io/gettingstarted/installation/firmwaretool/ and follow "; \
		echo "          the instructions to download the appropriate program matching your operating system."; \
		echo; \
		exit 1; \
	fi

check-firmware-upgrade-port:
	@if test "${mcu_port_type}" = "ip"; then \
		echo; \
		echo "ERROR: Unable to install firmware over IP"; \
		echo; \
		echo "ADVICE: Please adjust the \"MCU_PORT\" environment variable to point to a serial device spec like"; \
		echo; \
		echo "    export MCU_PORT=/dev/cu.usbmodemPy002342   # reka"; \
		echo; \
		exit 1; \
	fi

install-pycom-firmware-preflight: check-pycom-fwtool check-firmware-upgrade-port
	@# Ask the user to confirm firmware installation.
	@$(MAKE) confirm text="Install Pycom firmware \"$(pycom_firmware_file)\" on the device connected to \"$(pycom_firmware_port)\""


# ===========================
# Firmware and device actions
# ===========================

# FIXME: Expand this to more hardware
pycom_firmware_file := FiPy-1.20.0.rc11.tar.gz

# Download Pycom firmware to your workstation
download-pycom-firmware:

	@# Define path to the "dist-packages" installation directory.
	$(eval target_dir := ./dist-firmwares)
	@#$(eval fetch := wget --no-clobber --unlink --directory-prefix)
	$(eval fetch := wget --no-clobber --unlink)

	@mkdir -p $(target_dir)
	@#$(fetch) $(target_dir) https://github.com/pycom/pycom-micropython-sigfox/releases/download/v1.20.0.rc12/FiPy-1.20.0.rc12-application.elf

	$(eval url := "https://software.pycom.io/downloads/$(pycom_firmware_file)")
	@echo "INFO: Downloading firmware from \"$(url)\""
	$(fetch) --output-document=$(target_dir)/$(pycom_firmware_file) "$(url)" | true

## Display chip_id
chip_id: check-mcu-port
	$(pycom_fwtool_cli) --port $(pycom_firmware_port) chip_id

## Install Pycom firmware on device
install-pycom-firmware: install-pycom-firmware-preflight download-pycom-firmware
	echo "INFO: Installing firmware \"$(pycom_firmware_file)\""
	"$(pycom_fwtool_cli)" --verbose --port "$(pycom_firmware_port)" flash --tar "dist-firmwares/$(pycom_firmware_file)"

## Format flash filesystem with LittleFS
format-flash: check-mcu-port

	@# Old version
	@# $(rshell) $(rshell_options) --file tools/clean.rshell

	@# Ask the user to confirm formatting.
	@$(MAKE) confirm text="Format /flash on the device with LittleFS? THIS WILL DESTROY DATA ON YOUR DEVICE."

	@echo Creating and formatting LittleFS filesystem
	$(rshell) $(rshell_options) --quiet repl pyboard 'import os, pycom ~ pycom.bootmgr(fs_type=pycom.LittleFS, reset=True) ~ os.fsformat(\"/flash\") ~'

## Erase flash filesystem
erase-fs: check-mcu-port

	@# Ask the user to confirm erasing.
	@$(MAKE) confirm text="Erase the filesystem on the device? THIS WILL DESTROY DATA ON YOUR DEVICE."

	@echo Erasing filesystem
	$(pycom_fwtool_cli) --port ${pycom_firmware_port} erase_fs
