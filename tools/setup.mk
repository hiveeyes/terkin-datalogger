download-requirements:

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


	## API

	# Install MicroWebSrv and MicroDNSSrv libraries
	# https://github.com/jczic/MicroWebSrv
	# https://github.com/jczic/MicroDNSSrv
	$(fetch) $(target_dir) https://raw.githubusercontent.com/jczic/MicroWebSrv/b50ed11/microWebSrv.py
	$(fetch) $(target_dir) https://raw.githubusercontent.com/jczic/MicroWebSrv/b50ed11/microWebSocket.py
	$(fetch) $(target_dir) https://raw.githubusercontent.com/jczic/MicroWebSrv/b50ed11/microWebTemplate.py
	$(fetch) $(target_dir) https://raw.githubusercontent.com/jczic/MicroDNSSrv/4cd90f6/microDNSSrv.py

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

	# Install BME280 Libary
	@#$(fetch) $(target_dir) https://raw.githubusercontent.com/catdog2/mpy_bme280_esp8266/d7e052b/bme280.py
	@#$(fetch) $(target_dir) https://raw.githubusercontent.com/robert-hh/BME280/a7074fd2d5a140a14957dbb7c6f247f975a6dcfa/bme280_int.py
	$(fetch) $(target_dir) https://raw.githubusercontent.com/robert-hh/BME280/a7074fd2d5a140a14957dbb7c6f247f975a6dcfa/bme280_float.py

	# Install Pycom OneWire and DS18x20 libraries
	# https://github.com/micropython/micropython/tree/master/drivers
	mkdir -p $(target_dir)/onewire
	touch $(target_dir)/onewire/__init__.py

	# Vanilla onewire.py
	#$(fetch) $(target_dir)/onewire https://raw.githubusercontent.com/pycom/pycom-libraries/60f2592/examples/DS18X20/onewire.py

	# Optimize timing, enable CRC check and slim the code #62
	# https://github.com/pycom/pycom-libraries/pull/62
	$(fetch) $(target_dir)/onewire https://raw.githubusercontent.com/pycom/pycom-libraries/dabce8d9cc8cf3b9849446000d811a39c53b6093/examples/DS18X20/onewire.py


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
