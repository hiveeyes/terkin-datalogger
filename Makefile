include config.mk
include tools/core.mk


# ============
# Main targets
# ============

setup: setup-environment setup-micropython install-requirements

setup-micropython:
	@# FIXME: Describe how to install MicroPython on other platforms.
	@# brew install micropython

install-requirements:
	@echo "INFO: Please install MicroPython for Unix"
	export MICROPYPATH=`pwd`/dist-packages; micropython -m upip install -r requirements-mpy.txt

	# Remove some dependencies again which are already shipped as Pycom builtins
	rm dist-packages/re.py dist-packages/ffilib.py


# ==============
# rshell targets
# ==============

rshell:
	$(rshell) $(rshell_options)

repl:
	$(rshell) $(rshell_options) repl

recycle:
	$(rshell) $(rshell_options) --file tools/upload-requirements.rshell
	$(rshell) $(rshell_options) --file tools/upload-sketch.rshell
	@#$(MAKE) reset

list-serials:
	@$(rshell) $(rshell_options) --list

list-boards:
	@$(rshell) $(rshell_options) boards


# =====================
# Miscellaneous targets
# =====================

reset:
	$(ampy) --port $(serial_port) --delay 1 reset

upload-things:
	@echo "Uploading main application: main.py and settings.py"
	$(rshell) $(rshell_options) cp boot.py /flash
	$(rshell) $(rshell_options) cp main.py /flash
	$(rshell) $(rshell_options) cp settings.py /flash

upload-lib:
	$(rshell) $(rshell_options) rsync ./lib /flash/lib
