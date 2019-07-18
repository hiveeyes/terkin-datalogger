download-requirements:

	# Define path to the "dist-packages" installation directory.
	$(eval target_dir := ./dist-packages)
	$(eval fetch := wget --quiet --no-clobber --directory-prefix)

	# Install "upip", the PyPI package manager for MicroPython.
	$(pip3) install pycopy-cpython-upip

	# Install all required packages listed in file "requirements-mpy.txt".
	$(python3) -m upip install -p $(target_dir) -r requirements-mpy.txt

	# Install "micropython-urllib.parse" without "micropython-re-pcre"
	# to avoid collision with libraries shipped as Pycom builtins.
	mkdir -p $(target_dir)/urllib
	$(fetch) $(target_dir)/urllib https://raw.githubusercontent.com/pfalcon/pycopy-lib/52d356b5/urllib.parse/urllib/parse.py
	touch $(target_dir)/urllib/__init__.py

	# Install "micropython-base64" without 'micropython-binascii', 'micropython-re-pcre', 'micropython-struct'
	$(fetch) $(target_dir) https://raw.githubusercontent.com/pfalcon/pycopy-lib/52d356b5/base64/base64.py

	# Install "micropython-logging" without "micropython-os"
	# to avoid collision with libraries shipped as Pycom builtins.
	mkdir -p $(target_dir)/logging
	$(fetch) $(target_dir)/logging https://raw.githubusercontent.com/pfalcon/pycopy-lib/52d356b5/logging/logging/__init__.py
	$(fetch) $(target_dir)/logging https://raw.githubusercontent.com/pfalcon/pycopy-lib/52d356b5/logging/logging/handlers.py

	# Install Pycom "mqtt.py"
	$(fetch) $(target_dir) https://raw.githubusercontent.com/pycom/pycom-libraries/6544105e/lib/mqtt/mqtt.py

	# Install MicroWebSrv and MicroDNSSrv libraries
	# https://github.com/jczic/MicroWebSrv
	# https://github.com/jczic/MicroDNSSrv
	$(fetch) $(target_dir) https://raw.githubusercontent.com/jczic/MicroWebSrv/b50ed11/microWebSrv.py
	$(fetch) $(target_dir) https://raw.githubusercontent.com/jczic/MicroWebSrv/b50ed11/microWebSocket.py
	$(fetch) $(target_dir) https://raw.githubusercontent.com/jczic/MicroWebSrv/b50ed11/microWebTemplate.py
	$(fetch) $(target_dir) https://raw.githubusercontent.com/jczic/MicroDNSSrv/4cd90f6/microDNSSrv.py

	# Install Pycoproc Libary
	$(fetch) $(target_dir) https://raw.githubusercontent.com/pycom/pycom-libraries/681302a4/lib/pycoproc/pycoproc.py

	# Install Quectel L76 GNSS library (Pytrack Board)
	$(fetch) $(target_dir) https://raw.githubusercontent.com/andrethemac/L76GLNSV4/b68b3402/L76GNSV4.py

	# Install Pytrack Board Libary
	$(fetch) $(target_dir) https://raw.githubusercontent.com/pycom/pycom-libraries/ce0cfa5/pytrack/lib/LIS2HH12.py

	# Install Pytrack Board Libary
	$(fetch) $(target_dir) https://raw.githubusercontent.com/pycom/pycom-libraries/0f123c7/pytrack/lib/pytrack.py

	# Install BME280 Libary
	$(fetch) $(target_dir) https://raw.githubusercontent.com/catdog2/mpy_bme280_esp8266/d7e052b/bme280.py

	# Install slightly updated "dotty_dict" module
	# https://github.com/pawelzny/dotty_dict
	mkdir -p $(target_dir)/dotty_dict
	$(fetch) $(target_dir)/dotty_dict https://raw.githubusercontent.com/pawelzny/dotty_dict/v1.1.1/dotty_dict/__init__.py
	$(fetch) $(target_dir)/dotty_dict https://raw.githubusercontent.com/pawelzny/dotty_dict/v1.1.1/dotty_dict/dotty_dict.py

	# Install OneWire and DS18x20 libraries
	# https://github.com/micropython/micropython/tree/master/drivers
	mkdir -p $(target_dir)/onewire
	touch $(target_dir)/onewire/__init__.py
	$(fetch) $(target_dir)/onewire https://raw.githubusercontent.com/pycom/pycom-libraries/aacafd62/examples/DS18X20/onewire.py

	# Install PyCayenneLPP from Git repository.
	$(eval tmpdir := ./.pycayennelpp.tmp)
	rm -rf $(tmpdir)
	mkdir -p $(tmpdir)
	git clone https://github.com/hiveeyes/pycayennelpp $(tmpdir)
	rm -r $(tmpdir)/cayennelpp/tests
	cp -r $(tmpdir)/cayennelpp $(target_dir)/
	rm -rf $(tmpdir)
