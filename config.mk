# *******************************
# Programming sandbox environment
# *******************************

# Serial interface settings
# =========================
$(eval serial_port     := /dev/cu.usbmodemPye090a1)
$(eval serial_bufsize  := 30)
$(eval rshell_options  := --port $(serial_port) --buffer-size $(serial_bufsize) --timing)
