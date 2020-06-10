## Setup prerequisites for CPython
setup-cpython:

	@# Define program paths.
	$(eval pip := .venv3/bin/pip3)
	$(eval python := .venv3/bin/python)

	# Install Terkin
	$(python) setup.py develop

	# Install CircuitPython libraries.
	$(pip) install -r requirements-cpython.txt


	@# Define path to the "dist-packages" installation directory.
	$(eval target_dir := ./dist-packages)

	# Install driver support for Dragino LoRa Hat.
	curl --location https://github.com/daq-tools/dragino/archive/terkin.tar.gz | tar -C $(target_dir) --strip-components=1 -xzvf - dragino-terkin/dragino

	# Install updated pySX127x driver.
	curl --location https://github.com/daq-tools/pySX127x/archive/dragino.tar.gz | tar -C $(target_dir)/dragino --strip-components=1 -xzvf - pySX127x-dragino/SX127x

## Setup prerequisites for CPython on single-board-computers (SBC)
setup-sbc:

	@# Define path to the "pip" program.
	$(eval pip := .venv3/bin/pip3)

	# Install modules.
	$(pip) install -r requirements-sbc.txt

setup-gpsd:
	sudo apt install gpsd gpsd-clients

## Invoke datalogger on CPython
run-cpython:
	.venv3/bin/terkin --config=src/settings.py --daemon

run-cpython-callgraph:

	# Setup
	$(pip3) install pycallgraph2 graphviz

	@# All
	@#$(eval pycg_options :=  --no-groups --include="__main__" --include="umal.*" --include="terkin.*" --exclude="terkin.configuration.*" --exclude="terkin.logging.*" --exclude="terkin.util.*" --exclude="terkin.exception.*")

	@# Reduced
	@#$(eval pycg_options :=  --no-groups --include="terkin.*" --exclude="terkin.configuration.*" --exclude="terkin.logging.*" --exclude="terkin.util.*" --exclude="terkin.exception.*")

	@# Slim 1
	@#$(eval pycg_options :=  --no-groups --include="terkin.*" --exclude="terkin.driver.*" --exclude="terkin.configuration.*" --exclude="terkin.logging.*" --exclude="terkin.util.*" --exclude="terkin.exception.*")

	@# Main + Network
	$(eval pycg_options :=  --no-groups --include="terkin.datalogger.*" --include="terkin.device.*" --include="terkin.network.*" --include="terkin.telemetry.*")

	# Generate "pycallgraph.png"
	.venv3/bin/pycallgraph ${pycg_options} graphviz -- .venv3/bin/terkin --config=src/settings.py

	# Generate "pycallgraph.dot"
	.venv3/bin/pycallgraph ${pycg_options} graphviz --output-format=dot --output-file=pycallgraph.dot -- .venv3/bin/terkin --config=src/settings.py
	dot -Tsvg pycallgraph.dot > pycallgraph.svg


## Setup prerequisites for running on Raspberry Pi / Dragino
setup-dragino:
	-$(MAKE) setup
	-$(MAKE) setup-cpython
	-$(MAKE) setup-sbc
	-$(MAKE) setup-gpsd
