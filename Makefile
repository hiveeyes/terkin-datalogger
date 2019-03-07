include config.mk
include tools/core.mk


# ============
# Main targets
# ============

setup-micropython:
	@# FIXME: Describe how to install MicroPython on other platforms.
	@# brew install micropython

install-requirements:
	@echo "INFO: Please install MicroPython for Unix"
	micropython -m upip install -p dist-packages -r requirements-mpy.txt

recycle:
	$(rshell) $(rshell_options) --file tools/upload-requirements.rshell
	$(rshell) $(rshell_options) --file tools/upload-sketch.rshell
	@#$(MAKE) reset

reset:
	$(ampy) --port $(serial_port) --delay 1 reset

sync-all:
	$(rshell) $(rshell_options) rsync . /flash

sync-main:
	@#$(rshell) $(rshell_options) cp main.py /flash
	@#$(rshell) $(rshell_options) cp ./lib/radio.py /flash/lib

sync-lib:
	$(rshell) $(rshell_options) rsync ./lib /flash/lib

rshell:
	$(rshell) $(rshell_options)

repl:
	$(rshell) $(rshell_options) repl
