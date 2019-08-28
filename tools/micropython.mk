# ============
# Dependencies
# ============

$(eval rshell_options  := --port $(mcu_port) --user micro --password python --buffer-size $(mcu_transfer_buffer))
#$(eval rshell_options  := --port $(mcu_port) --user micro --password python --buffer-size $(mcu_transfer_buffer) --baud 115200 --quiet)
#$(eval rshell_options  := --port $(mcu_port) --user micro --password python --buffer-size $(mcu_transfer_buffer) --timing)

$(eval mpy-cross-all := ./bin/mpy_cross_all.py)



# ================
# Action utilities
# ================

## List all serial interfaces
list-serials:
	@$(rshell) --list


# -------------
# REPL / rshell
# -------------

## Reset port or even USB subsystem
reset-port:
ifeq ($(RUNNING_IN_HELL),true)
	@echo "TODO: Reset USB subsystem on Windows"
else
	@echo "Restarting USB subsystem"
	systemctl restart usb
endif

## List all MicroPython boards
list-boards: check-mcu-port
	@$(rshell) $(rshell_options) boards
	@echo

## Inquire device information
device-info: check-mcu-port
	@$(rshell) $(rshell_options) --quiet repl '~ import os ~ os.uname() ~'
	@echo

## Open console over serial or telnet
console: check-mcu-port
ifeq ($(mcu_port_type),usb)
	@echo "Connecting via serial port ${mcu_port}."
	$(miniterm) ${mcu_port} 115200
else
	@echo "Connecting via telnet to ${mcu_port}. Please enter User: micro, Password: python"
	@#telnet ${mcu_port}
	expect -c 'spawn telnet ${mcu_port}; expect "*?ogin as:*"; sleep 0.2; send -- "micro\r"; expect "*?assword:*"; sleep 0.2; send -- "python\r"; interact;'
endif

## Run interactive rshell on the device
rshell: check-mcu-port
	$(rshell) $(rshell_options)
	@echo

## Run interactive REPL on the device
repl: check-mcu-port
	$(rshell) $(rshell_options) repl
	@echo

## Send reset command to device
reset-device: check-mcu-port
	@echo "Resetting device"
	@$(rshell) $(rshell_options) --quiet repl '~ import machine ~ machine.reset() ~'
	@echo
	@echo

## Send reset command to device and keep the REPL shell attached
reset-device-attached: check-mcu-port
	@$(rshell) $(rshell_options) --quiet repl '~ import machine ~ machine.reset()'
	@echo

reset-ampy:
	$(ampy) --port $(serial_port) --delay 1 reset
	@echo


# -------------------------
# Ahead of time compilation
# -------------------------

mpy-cross-setup: setup-virtualenv2

	@echo "$(INFO) Installing mpy-cross"
	@$(pip2) --quiet install mpy-cross==1.9.4

	@echo "$(INFO) Installing mpy-cross-all"
	@mkdir -p ./bin
	@wget --quiet --unlink --output-document $(mpy-cross-all) https://raw.githubusercontent.com/hiveeyes/micropython/mpy-cross-plus/tools/mpy_cross_all.py


# ----
# lftp
# ----

# On Windows, you might want to install "lftp" through "Chocolatey" by invoking "choco install lftp".
# Path to "lftp.exe" would be at C:\ProgramData\chocolatey\bin\lftp.exe then.
$(eval lftp_unix := lftp)
$(eval lftp_windows := /mnt/c/ProgramData/chocolatey/bin/lftp.exe)

LFTP_UNIX := $(shell which $(lftp_unix))
LFTP_WINDOWS := $(or $(and $(wildcard $(lftp_windows)),1),0)

ifneq ($(LFTP_UNIX),)
	lftp_bin := $(LFTP_UNIX)
endif
ifeq ($(LFTP_WINDOWS),1)
	lftp_bin := $(lftp_windows)
endif

check-lftp:
	@echo "$(INFO) Checking for existance of the \"lftp\" program at \"$(lftp_bin)\""
	@test -n "$(lftp_bin)" -a -e "$(lftp_bin)" || (echo "\nERROR: \"lftp\" program not found.\nPlease install it on your machine.\n"; exit 1)

lftp: check-lftp

	@# Invoke lftp, platform agnostic
	$(lftp_bin) -u micro,python ${mcu_port} < ${lftp_recipe}

	@# Path to "lftp.exe" would be at C:\ProgramData\chocolatey\bin\lftp.exe then.
	@echo "lftp status: $$?"
