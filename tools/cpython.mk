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

setup-sbc:

	@# Define path to the "pip" program.
	$(eval pip := .venv3/bin/pip3)

	# Install modules.
	$(pip) install -r requirements-sbc.txt

setup-gpsd:
	sudo apt install gpsd gpsd-clients

run-cpython:
	.venv3/bin/terkin --daemon

setup-dragino:
	-$(MAKE) setup
	-$(MAKE) setup-cpython
	-$(MAKE) setup-sbc
	-$(MAKE) setup-gpsd
