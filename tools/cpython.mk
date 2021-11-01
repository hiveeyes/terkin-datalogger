## Setup prerequisites for CPython
setup-cpython:

	@# Define program paths.
	$(eval pip := .venv/bin/pip3)
	$(eval python := .venv/bin/python)

	# Install Terkin
	$(python) setup.py develop

	# Install CircuitPython libraries.
	$(pip) install --requirement=requirements-cpython.txt --upgrade

## Setup prerequisites for CPython on single-board-computers (SBC)
setup-sbc:

	@# Define path to the "pip" program.
	$(eval pip := .venv/bin/pip3)

	# Install modules.
	$(pip) install -r requirements-sbc.txt

setup-gpsd:
	sudo apt install gpsd gpsd-clients

## Invoke datalogger on CPython
run-cpython:
	.venv/bin/terkin --config=src/settings.py --daemon

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
	.venv/bin/pycallgraph ${pycg_options} graphviz -- .venv/bin/terkin --config=src/settings.py

	# Generate "pycallgraph.dot"
	.venv/bin/pycallgraph ${pycg_options} graphviz --output-format=dot --output-file=pycallgraph.dot -- .venv/bin/terkin --config=src/settings.py
	dot -Tsvg pycallgraph.dot > pycallgraph.svg


## Setup Dragino/LoRaWAN libraries
setup-dragino-lorawan:
	-$(MAKE) setup
	-$(MAKE) setup-cpython

	@# Define path to the "dist-packages" installation directory.
	$(eval target_dir := ./dist-packages)

	# Install driver support for Dragino LoRa Hat.
	curl --location https://github.com/daq-tools/dragino-lorawan/archive/ttn3-terkin.tar.gz | tar -C $(target_dir) --strip-components=1 -xzvf - dragino-lorawan-ttn3-terkin/dragino

	# Install updated pySX127x driver.
	curl --location https://github.com/daq-tools/pySX127x/archive/dragino.tar.gz | tar -C $(target_dir)/dragino --strip-components=1 -xzvf - pySX127x-dragino/SX127x

	# Install default `dragino.toml`
	wget --no-clobber https://raw.githubusercontent.com/daq-tools/dragino-lorawan/ttn3-terkin/dragino.toml

## Setup prerequisites for running on Raspberry Pi / Dragino
setup-dragino:
	-$(MAKE) setup-dragino-lorawan
	-$(MAKE) setup-sbc
	-$(MAKE) setup-gpsd
