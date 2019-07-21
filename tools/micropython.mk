# ================
# Action utilities
# ================

$(eval rshell_options  := --port $(mcu_port) --user micro --password python --buffer-size $(mcu_transfer_buffer) --quiet)
#$(eval rshell_options  := --port $(mcu_port) --user micro --password python --buffer-size $(mcu_transfer_buffer) --timing)


## List all serial interfaces
list-serials:
	@$(rshell) --list

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
