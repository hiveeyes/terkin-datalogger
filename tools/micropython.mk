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


# ================
# Action utilities
# ================

## List all serial interfaces
list-serials:
	@$(rshell) --list

## List all MicroPython boards
list-boards: check-mcu-port
	@$(rshell) $(rshell_options) boards

## Inquire device information
device-info: check-mcu-port
	@$(rshell) $(rshell_options) --quiet repl '~ import os ~ os.uname() ~'

## Open console over serial or telnet
console: check-mcu-port

## Run interactive rshell on the device
rshell: check-mcu-port
	$(rshell) $(rshell_options)

## Run interactive REPL on the device
repl: check-mcu-port
	$(rshell) $(rshell_options) repl

ifeq ($(mcu_port_type),usb)
	@echo "Connecting via serial port ${mcu_port}."
	$(miniterm) ${mcu_port} 115200
else
	@echo "Connecting via telnet to ${mcu_port}. Please enter User: micro, Password: python"
	@#telnet ${mcu_port}
	expect -c 'spawn telnet ${mcu_port}; expect "*?ogin as:*"; sleep 0.2; send -- "micro\r"; expect "*?assword:*"; sleep 0.2; send -- "python\r"; interact;'
endif

## Send reset command to device
reset-device: check-mcu-port
	@$(rshell) $(rshell_options) --quiet repl '~ import machine ~ machine.reset() ~'

## Send reset command to device and keep the REPL shell attached
reset-device-attached: check-mcu-port
	@$(rshell) $(rshell_options) --quiet repl '~ import machine ~ machine.reset()'

reset-ampy:
	$(ampy) --port $(serial_port) --delay 1 reset
