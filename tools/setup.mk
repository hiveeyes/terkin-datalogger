EXECUTABLES = wget curl

check-download-tools:
	$(foreach exec,$(EXECUTABLES),\
		$(if $(shell which $(exec)),,$(error "Program '$(exec)' not found in PATH. Please install it.")))

download-requirements: check-download-tools

	@# Define path to the "dist-packages" installation directory.
	$(eval target_dir := ./dist-packages)

	@echo "$(INFO) Downloading and installing all 3rd-party modules into ${target_dir}"

	@-$(MAKE) download-requirements-real target_dir=${target_dir} && ([ $$? -eq 0 ] \
		&& echo "$(OK) Installation successful") || echo "$(ERROR) Installation failed"


download-requirements-real:

	@# Alias to "wget" program.
	$(eval fetch := wget --quiet --no-clobber --directory-prefix)

	# Install "upip", the PyPI package manager for MicroPython.
	$(pip3) install --no-cache --upgrade --upgrade-strategy eager "pycopy-cpython-upip==1.3.3"

	# Install all required packages listed in file "requirements-mpy.txt".
	$(python3) -m upip install -p $(target_dir) -r requirements-mpy.txt


	## Utility libraries

	# Install "os.path" under the different name "os_path"
	rm $(target_dir)/os_path.py || true
	$(fetch) $(target_dir) --output-document=$(target_dir)/os_path.py https://raw.githubusercontent.com/pfalcon/pycopy-lib/7ba2231/os.path/os/path.py

	# Install "micropython-base64" without 'micropython-binascii', 'micropython-re-pcre', 'micropython-struct'
	$(fetch) $(target_dir) https://raw.githubusercontent.com/pfalcon/pycopy-lib/52d356b5/base64/base64.py

	# Install "micropython-logging" without "micropython-os"
	# to avoid collision with libraries shipped as Pycom builtins.
	mkdir -p $(target_dir)/logging
	$(fetch) $(target_dir)/logging https://raw.githubusercontent.com/pfalcon/pycopy-lib/52d356b5/logging/logging/__init__.py
	$(fetch) $(target_dir)/logging https://raw.githubusercontent.com/pfalcon/pycopy-lib/52d356b5/logging/logging/handlers.py

	# Install updated "micropython-datetime" module
	rm $(target_dir)/datetime.py || true
	$(fetch) $(target_dir) https://raw.githubusercontent.com/daq-tools/pycopy-lib/improve-datetime/datetime/datetime.py

	# Install slightly updated "dotty_dict" module
	# https://github.com/pawelzny/dotty_dict
	mkdir -p $(target_dir)/dotty_dict
	$(fetch) $(target_dir)/dotty_dict https://raw.githubusercontent.com/pawelzny/dotty_dict/v1.1.1/dotty_dict/__init__.py
	$(fetch) $(target_dir)/dotty_dict https://raw.githubusercontent.com/pawelzny/dotty_dict/v1.1.1/dotty_dict/dotty_dict.py

	# Install state machine library
	#curl --location https://github.com/fgmacedo/python-statemachine/archive/v0.7.1.tar.gz | tar -C $(target_dir) --strip-components=1 -xzvf - python-statemachine-0.7.1/statemachine

	# pysm==0.3.9
	#curl --location https://github.com/pgularski/pysm/archive/v0.3.9-alpha.tar.gz | tar -C $(target_dir) --strip-components=1 -xzvf - pysm-0.3.9-alpha/pysm


	## API

	# Install MicroWebSrv2
	# https://github.com/jczic/MicroWebSrv
	#curl --location https://github.com/jczic/MicroWebSrv2/archive/v2.0.6.tar.gz | tar -C $(target_dir) --strip-components=1 -xzvf - MicroWebSrv2-2.0.6/MicroWebSrv2
	curl --location https://github.com/daq-tools/MicroWebSrv2/archive/improve-setup.tar.gz | tar -C $(target_dir) --strip-components=1 -xzvf - MicroWebSrv2-improve-setup/MicroWebSrv2

	# Install MicroDNSSrv
	# https://github.com/jczic/MicroDNSSrv
	#$(fetch) $(target_dir) https://raw.githubusercontent.com/jczic/MicroDNSSrv/4cd90f6/microDNSSrv.py

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

	# Install "urequests" module.
	rm $(target_dir)/urequests.py || true
	$(fetch) $(target_dir) --output-document=$(target_dir)/urequests.py https://raw.githubusercontent.com/daq-tools/pycopy-lib/improve-urequests/urequests/urequests/__init__.py

	# Install "umqtt" module.
	rm $(target_dir)/umqtt.py || true
	$(fetch) $(target_dir) --output-document=$(target_dir)/umqtt.py https://raw.githubusercontent.com/daq-tools/pycopy-lib/improve-umqtt/umqtt.simple/umqtt/simple.py

	# Install PyCayenneLPP from Git repository.
	$(eval tmpdir := ./.pycayennelpp.tmp)
	rm -rf $(tmpdir)
	mkdir -p $(tmpdir)
	git clone https://github.com/hiveeyes/pycayennelpp $(tmpdir)
	rm -r $(tmpdir)/cayennelpp/tests
	cp -r $(tmpdir)/cayennelpp $(target_dir)/
	rm -rf $(tmpdir)

	# Install SIM800 driver
	rm $(target_dir)/pythings_sim800.py || true
	$(fetch) $(target_dir) --output-document=$(target_dir)/pythings_sim800.py https://raw.githubusercontent.com/hiveeyes/pythings-sim800/pppos/SIM800L.py


	## RTC and non-volatile memory

	# Driver for DS3231 RTC
	#$(fetch) $(target_dir) https://raw.githubusercontent.com/micropython-Chinese-Community/mpy-lib/db40eda7/misc/DS3231/DS3231.py
	#$(fetch) $(target_dir) https://raw.githubusercontent.com/hiveeyes/DS3231micro/add-temperature/DS3231micro.py
	$(fetch) $(target_dir) https://raw.githubusercontent.com/poesel/Power_DS3231_Adapter/master/src/DS3231tokei.py

	# Driver for AT24C32 EEPROM
	$(fetch) $(target_dir) https://raw.githubusercontent.com/mcauser/micropython-tinyrtc-i2c/1e650122a516513c1a5e348e1755c7dc829deab9/at24c32n.py


	## Sensors

	# 1. Install BME280 Libary
	@#$(fetch) $(target_dir) https://raw.githubusercontent.com/catdog2/mpy_bme280_esp8266/d7e052b/bme280.py
	@#$(fetch) $(target_dir) https://raw.githubusercontent.com/robert-hh/BME280/79ccf348ec674f15c92a1debf1aceb383db38321/bme280_int.py
	$(fetch) $(target_dir) https://raw.githubusercontent.com/robert-hh/BME280/79ccf348ec674f15c92a1debf1aceb383db38321/bme280_float.py

	# 2. Install Pycom OneWire and DS18x20 libraries

	# Genuine MicroPython driver for Pycom MicroPython 1.11.
	# https://github.com/micropython/micropython/tree/v1.11/drivers/onewire
	rm $(target_dir)/onewire_native.py || true
	rm $(target_dir)/ds18x20_native.py || true
	$(fetch) $(target_dir) --output-document=$(target_dir)/onewire_native.py https://raw.githubusercontent.com/daq-tools/micropython/improve-onewire/drivers/onewire/onewire.py
	$(fetch) $(target_dir) --output-document=$(target_dir)/ds18x20_native.py https://raw.githubusercontent.com/micropython/micropython/v1.11/drivers/onewire/ds18x20.py

	# Pure-Python onewire.py from pycom-libraries for Pycom MicroPython 1.9.4.
	# Has no CRC checks.
	#$(fetch) $(target_dir)/onewire https://raw.githubusercontent.com/pycom/pycom-libraries/60f2592/examples/DS18X20/onewire.py

	# Pure-Python onewire.py from pycom-libraries for Pycom MicroPython 1.9.4.
	# Enhanced by @robert-hh: Optimize timing, enable CRC check and slim the code.
	# https://github.com/robert-hh/Onewire_DS18X20
	# https://github.com/pycom/pycom-libraries/pull/62
	rm $(target_dir)/onewire_python.py || true
	rm $(target_dir)/ds18x20_python.py || true
	$(fetch) $(target_dir) --output-document=$(target_dir)/onewire_python.py https://raw.githubusercontent.com/robert-hh/Onewire_DS18X20/e2a8e8a/onewire.py
	$(fetch) $(target_dir) --output-document=$(target_dir)/ds18x20_python.py https://raw.githubusercontent.com/robert-hh/Onewire_DS18X20/e2a8e8a/ds18x20.py

	# 3. Install driver for MAX17043
	rm $(target_dir)/max17043.py || true
	$(fetch) $(target_dir) --output-document=$(target_dir)/max17043.py https://raw.githubusercontent.com/hiveeyes/DFRobot_MAX17043/better-micropython/micropython/DFRobot_MAX17043.py

	# 4. Install driver for SI7021
	$(fetch) $(target_dir) https://raw.githubusercontent.com/robert-hh/SI7021/e5d49689/SI7021.py

	# 5. Install INA219 library
	$(fetch) $(target_dir) https://raw.githubusercontent.com/chrisb2/pyb_ina219/f427017/ina219.py

	# 6. Install VEDirect library
	$(fetch) $(target_dir) https://github.com/nznobody/vedirect/raw/345a688/src/vedirect/vedirect.py


download-requirements-ui:

	@# Define path to the "dist-packages" installation directory.
	$(eval target_dir := ./dist-packages)

	## GUI
	curl --location https://github.com/hiveeyes/picotui/archive/micropython.zip | tar -C ${target_dir} --strip-components=1 -xvf - picotui-micropython/picotui


download-requirements-ratrack:

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
