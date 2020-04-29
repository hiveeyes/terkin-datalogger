install-cpython:

	@# Define path to the "pip" program.
	$(eval pip := .venv3/bin/pip3)

	@# Define path to the "dist-packages" installation directory.
	$(eval target_dir := ./dist-packages)

	# Install CircuitPython libraries.
	$(pip) install -r requirements-cpython.txt

	# Install driver support for Dragino LoRa Hat.
	curl --location https://github.com/daq-tools/dragino/archive/terkin.tar.gz | tar -C $(target_dir) --strip-components=1 -xzvf - dragino-terkin/dragino

	# Install updated pySX127x driver.
	curl --location https://github.com/daq-tools/pySX127x/archive/dragino.tar.gz | tar -C $(target_dir)/dragino --strip-components=1 -xzvf - pySX127x-dragino/SX127x

	# Install Victron Energy VE.Direct text protocol driver.
	$(pip) install git+https://github.com/karioja/vedirect@f74c0f2

run-cpython:
	.venv3/bin/python src/main_cpython.py
