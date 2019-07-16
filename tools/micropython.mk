# ================
# Programming port
# ================
$(eval mcu_port     := ${MCU_PORT})
ifeq ($(MCU_PORT),)
    $(eval mcu_port := ${MCU_SERIAL_PORT})
endif
$(eval mcu_transfer_buffer  := 2048)
$(eval rshell_options  := --port $(mcu_port) --user micro --password python --buffer-size $(mcu_transfer_buffer) --timing)

ifneq (,$(findstring /dev,$(mcu_port)))
    $(eval mcu_port_type := usb)
else
    $(eval mcu_port_type := ip)
endif

check-mcu-port:
	@echo Connecting via port type $(mcu_port_type)
	@if test "${MCU_PORT}" = ""; then \
        if test "${MCU_SERIAL_PORT}" = ""; then \
            echo "ERROR: Environment variable 'MCU_PORT' or 'MCU_SERIAL_PORT' not set"; \
            exit 1; \
        fi; \
	fi


# ======================
# Pycom firmware updater
# ======================
$(eval pycom_fwtool_cli_macos := /Applications/Pycom\ Firmware\ Update.app/Contents/Resources/pycom-fwtool-cli)
$(eval pycom_fwtool_cli_windows := c:\\Program\ Files\ (x86)\\Pycom\\Pycom\ Firmware\ Update\\pycom-fwtool-cli.exe)

PYCOM_MACOS := $(or $(and $(wildcard $(pycom_fwtool_cli_macos)),1),0)
PYCOM_WINDOWS := $(or $(and $(wildcard $(pycom_fwtool_cli_windows)),1),0)

ifeq ($(PYCOM_MACOS),1)
	pycom_fwtool_cli := $(pycom_fwtool_cli_macos)
endif
ifeq ($(PYCOM_WINDOWS),1)
	pycom_fwtool_cli := $(pycom_fwtool_cli_windows)
endif

check-pycom-fwtool:
	@if test "${pycom_fwtool_cli}" = ""; then \
		echo "ERROR: Pycom Firmware Updater not found"; \
		exit 1; \
	else \
		echo "INFO: Found Pycom Firmware Updater at $(pycom_fwtool_cli)"; \
	fi


# ================
# Action utilities
# ================

list-serials:
	@$(rshell) --list

rshell: check-mcu-port
	$(rshell) $(rshell_options)

repl: check-mcu-port
	$(rshell) $(rshell_options) repl

console: check-mcu-port

ifeq ($(mcu_port_type),usb)
	@echo "Connecting via serial port ${mcu_port}."
	$(miniterm) ${mcu_port} 115200
else
	@echo "Connecting via telnet to ${mcu_port}. Please enter User: micro, Password: python"
	@#telnet ${mcu_port}
	expect -c 'spawn telnet ${mcu_port}; expect "*?ogin as:*"; sleep 0.2; send -- "micro\r"; expect "*?assword:*"; sleep 0.2; send -- "python\r"; interact;'
endif

list-boards: check-mcu-port
	@$(rshell) $(rshell_options) boards

device-info: check-mcu-port
	@$(rshell) $(rshell_options) --quiet repl '~ import os ~ os.uname() ~'

reset-device: check-mcu-port
	@$(rshell) $(rshell_options) --quiet repl '~ import machine ~ machine.reset() ~'

reset-device-attached: check-mcu-port
	@$(rshell) $(rshell_options) --quiet repl '~ import machine ~ machine.reset()'

reset-ampy:
	$(ampy) --port $(serial_port) --delay 1 reset

format-flash: check-mcu-port

	@# Old version
	@# $(rshell) $(rshell_options) --file tools/clean.rshell

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

erase-fs: check-mcu-port
	$(eval retval := $(shell bash -c 'read -s -p "Erase the filesystem on the device? THIS WILL DESTROY DATA ON YOUR DEVICE. [y/n]? " outcome; echo $$outcome'))
	@if test "$(retval)" = "y"; then \
		echo; \
		\
		echo Erasing filesystem; \
		$(pycom_fwtool_cli) --port ${MCU_PORT} erase_fs; \
	else \
		echo; \
	fi
