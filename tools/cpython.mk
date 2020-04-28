install-cpython:

	# Install CircuitPython libraries.
	.venv3/bin/pip3 install -r requirements-circuitpython.txt

	@# Define path to the "dist-packages" installation directory.
	$(eval target_dir := ./dist-packages)

	# Install driver support for Dragino LoRa Hat.
	curl --location https://github.com/daq-tools/dragino/archive/terkin.tar.gz | tar -C $(target_dir) --strip-components=1 -xzvf - dragino-terkin/dragino

	# Install updated pySX127x driver.
	curl --location https://github.com/daq-tools/pySX127x/archive/dragino.tar.gz | tar -C $(target_dir)/dragino --strip-components=1 -xzvf - pySX127x-dragino/SX127x

run-cpython:
	.venv3/bin/python src/main_cpython.py
