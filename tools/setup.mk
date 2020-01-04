EXECUTABLES = wget curl

check-download-tools:
	$(foreach exec,$(EXECUTABLES),\
		$(if $(shell which $(exec)),,$(error "Program '$(exec)' not found in PATH. Please install it.")))

download-requirements: check-download-tools

	# Define path to the "dist-packages" installation directory.
	$(eval target_dir := ./dist-packages)
	$(eval fetch := wget --quiet --no-clobber --directory-prefix)

	# Install "upip", the PyPI package manager for MicroPython.
	$(pip3) install --no-cache --upgrade --upgrade-strategy eager "pycopy-cpython-upip==1.3.3"

	# Install all required packages listed in file "requirements-mpy.txt".
	$(python3) -m upip install -p $(target_dir) -r requirements-mpy.txt


	## Utility libraries

	# Install "os.path" under the different name "os_path"
	@test -e $(target_dir)/os_path.py || $(fetch) $(target_dir) --output-document=$(target_dir)/os_path.py https://raw.githubusercontent.com/pfalcon/pycopy-lib/7ba2231/os.path/os/path.py

	# Install "micropython-base64" without 'micropython-binascii', 'micropython-re-pcre', 'micropython-struct'
	$(fetch) $(target_dir) https://raw.githubusercontent.com/pfalcon/pycopy-lib/52d356b5/base64/base64.py

	# Install "micropython-logging" without "micropython-os"
	# to avoid collision with libraries shipped as Pycom builtins.
	mkdir -p $(target_dir)/logging
	$(fetch) $(target_dir)/logging https://raw.githubusercontent.com/pfalcon/pycopy-lib/52d356b5/logging/logging/__init__.py
	$(fetch) $(target_dir)/logging https://raw.githubusercontent.com/pfalcon/pycopy-lib/52d356b5/logging/logging/handlers.py

	# Install slightly updated "dotty_dict" module
	# https://github.com/pawelzny/dotty_dict
	mkdir -p $(target_dir)/dotty_dict
	$(fetch) $(target_dir)/dotty_dict https://raw.githubusercontent.com/pawelzny/dotty_dict/v1.1.1/dotty_dict/__init__.py
	$(fetch) $(target_dir)/dotty_dict https://raw.githubusercontent.com/pawelzny/dotty_dict/v1.1.1/dotty_dict/dotty_dict.py

	# Install state machine library
	curl --location https://github.com/fgmacedo/python-statemachine/archive/v0.7.1.tar.gz | tar -C $(target_dir) --strip-components=1 -xzvf - python-statemachine-0.7.1/statemachine



	## API

	# Install MicroWebSrv and MicroDNSSrv libraries
	# https://github.com/jczic/MicroWebSrv
	# https://github.com/jczic/MicroDNSSrv
	#$(fetch) $(target_dir) https://raw.githubusercontent.com/jczic/MicroWebSrv/b50ed11/microWebSrv.py
	#$(fetch) $(target_dir) https://raw.githubusercontent.com/jczic/MicroWebSrv/b50ed11/microWebSocket.py
	#$(fetch) $(target_dir) https://raw.githubusercontent.com/jczic/MicroWebSrv/b50ed11/microWebTemplate.py
	#$(fetch) $(target_dir) https://raw.githubusercontent.com/jczic/MicroDNSSrv/4cd90f6/microDNSSrv.py

	# Install MicroWebSrv2
	curl --location https://github.com/jczic/MicroWebSrv2/archive/v2.0.6.tar.gz | tar -C $(target_dir) --strip-components=1 -xzvf - MicroWebSrv2-2.0.6/MicroWebSrv2

	# Install BLE GATTS Wrapper for Pycom devices
	# https://github.com/cmisztur/pycom-ble-gatt-wrapper
	#$(fetch) $(target_dir) https://raw.githubusercontent.com/cmisztur/pycom-ble-gatt-wrapper/1deab094cf91d33dfe833b686db90e6ac00ce577/L99_BLEGATTS.py
	#$(fetch) $(target_dir) https://raw.githubusercontent.com/cmisztur/pycom-ble-gatt-wrapper/1deab094cf91d33dfe833b686db90e6ac00ce577/L99_BLEGATTSCharacteristic.py
	#$(fetch) $(target_dir) https://raw.githubusercontent.com/cmisztur/pycom-ble-gatt-wrapper/1deab094cf91d33dfe833b686db90e6ac00ce577/L99_BLEGATTSService.py


	## Telemetry

	# Install "micropython-urllib.parse" without "micropython-re-pcre"
	# to avoid collision with libraries shipped as Pycom builtins.
	mkdir -p $(target_dir)/urllib
	$(fetch) $(target_dir)/urllib https://raw.githubusercontent.com/pfalcon/pycopy-lib/52d356b5/urllib.parse/urllib/parse.py
	touch $(target_dir)/urllib/__init__.py

	# Install Pycom MQTT client library
	$(fetch) $(target_dir) https://raw.githubusercontent.com/pycom/pycom-libraries/60f2592/lib/mqtt/mqtt.py

	# Install PyCayenneLPP from Git repository.
	$(eval tmpdir := ./.pycayennelpp.tmp)
	rm -rf $(tmpdir)
	mkdir -p $(tmpdir)
	git clone https://github.com/hiveeyes/pycayennelpp $(tmpdir)
	rm -r $(tmpdir)/cayennelpp/tests
	cp -r $(tmpdir)/cayennelpp $(target_dir)/
	rm -rf $(tmpdir)


	## Sensors

	# 1. Install BME280 Libary
	@#$(fetch) $(target_dir) https://raw.githubusercontent.com/catdog2/mpy_bme280_esp8266/d7e052b/bme280.py
	@#$(fetch) $(target_dir) https://raw.githubusercontent.com/robert-hh/BME280/3bc048f93e0d155264d212dea16f589607511ae2/bme280_int.py
	$(fetch) $(target_dir) https://raw.githubusercontent.com/robert-hh/BME280/3bc048f93e0d155264d212dea16f589607511ae2/bme280_float.py

	# 2. Install Pycom OneWire and DS18x20 libraries

	# Genuine MicroPython driver for Pycom MicroPython 1.11.
	# https://github.com/micropython/micropython/tree/v1.11/drivers/onewire
	@test -e $(target_dir)/onewire_native.py || $(fetch) $(target_dir) --output-document=$(target_dir)/onewire_native.py https://raw.githubusercontent.com/micropython/micropython/v1.11/drivers/onewire/onewire.py
	@test -e $(target_dir)/ds18x20_native.py || $(fetch) $(target_dir) --output-document=$(target_dir)/ds18x20_native.py https://raw.githubusercontent.com/micropython/micropython/v1.11/drivers/onewire/ds18x20.py

	# Pure-Python onewire.py from pycom-libraries for Pycom MicroPython 1.9.4.
	# Has no CRC checks.
	#$(fetch) $(target_dir)/onewire https://raw.githubusercontent.com/pycom/pycom-libraries/60f2592/examples/DS18X20/onewire.py

	# Pure-Python onewire.py from pycom-libraries for Pycom MicroPython 1.9.4.
	# Enhanced by @robert-hh: Optimize timing, enable CRC check and slim the code.
	# https://github.com/pycom/pycom-libraries/pull/62
	@test -e $(target_dir)/onewire_python.py || $(fetch) $(target_dir) --output-document=$(target_dir)/onewire_python.py https://raw.githubusercontent.com/robert-hh/Onewire_DS18X20/e2a8e8a/onewire.py
	@test -e $(target_dir)/ds18x20_python.py || $(fetch) $(target_dir) --output-document=$(target_dir)/ds18x20_python.py https://raw.githubusercontent.com/robert-hh/Onewire_DS18X20/e2a8e8a/ds18x20.py

    # 3. Install driver for MAX17043
	@test -e $(target_dir)/max17043.py || $(fetch) $(target_dir) --output-document=$(target_dir)/max17043.py https://raw.githubusercontent.com/hiveeyes/DFRobot_MAX17043/better-micropython/micropython/DFRobot_MAX17043.py


download-requirements-optional:

	## Ratrack

	# Install Pycoproc Libary
	$(fetch) $(target_dir) https://raw.githubusercontent.com/pycom/pycom-libraries/681302a4/lib/pycoproc/pycoproc.py

	# Install Quectel L76 GNSS library (Pytrack Board)
	$(fetch) $(target_dir) https://raw.githubusercontent.com/andrethemac/L76GLNSV4/b68b3402/L76GNSV4.py

	# Install Pytrack Board Libary
	$(fetch) $(target_dir) https://raw.githubusercontent.com/pycom/pycom-libraries/ce0cfa5/pytrack/lib/LIS2HH12.py

	# Install Pytrack Board Libary
	$(fetch) $(target_dir) https://raw.githubusercontent.com/pycom/pycom-libraries/0f123c7/pytrack/lib/pytrack.py


	## sqnsupgrade
	$(eval sqns_dir := ./dist-firmwares/sqnsupgrade)
	mkdir -p $(sqns_dir)
	$(fetch) $(sqns_dir) https://raw.githubusercontent.com/pycom/pycom-libraries/96af79be7abcfca9f41a240decc6bd50b55bf5c4/lib/sqnsupgrade/sqnsbr.py
	$(fetch) $(sqns_dir) https://raw.githubusercontent.com/pycom/pycom-libraries/96af79be7abcfca9f41a240decc6bd50b55bf5c4/lib/sqnsupgrade/sqnsbrz.py
	$(fetch) $(sqns_dir) https://raw.githubusercontent.com/pycom/pycom-libraries/96af79be7abcfca9f41a240decc6bd50b55bf5c4/lib/sqnsupgrade/sqnscodec.py
	$(fetch) $(sqns_dir) https://raw.githubusercontent.com/pycom/pycom-libraries/96af79be7abcfca9f41a240decc6bd50b55bf5c4/lib/sqnsupgrade/sqnscrc.py
	$(fetch) $(sqns_dir) https://raw.githubusercontent.com/pycom/pycom-libraries/96af79be7abcfca9f41a240decc6bd50b55bf5c4/lib/sqnsupgrade/sqnstp.py
	$(fetch) $(sqns_dir) https://raw.githubusercontent.com/pycom/pycom-libraries/96af79be7abcfca9f41a240decc6bd50b55bf5c4/lib/sqnsupgrade/sqnsupgrade.py
