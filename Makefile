include config.mk
include tools/core.mk


# ============
# Main targets
# ============

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
