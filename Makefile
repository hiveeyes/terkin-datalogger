include tools/core.mk


# =====
# Setup
# =====

setup: setup-environment download-requirements

download-requirements:

    # Define path to the "dist-packages" installation directory.
	$(eval target_dir := ./dist-packages)
	$(eval fetch := wget --quiet --no-clobber --directory-prefix)

	# Install "upip", the PyPI package manager for MicroPython.
	$(pip3) install micropython-cpython-upip

	# Install all required packages listed in file "requirements-mpy.txt".
	$(python3) -m upip install -p $(target_dir) -r requirements-mpy.txt

	# Install "micropython-urllib.parse" without "micropython-re-pcre"
	# to avoid collision with libraries shipped as Pycom builtins.
	mkdir -p $(target_dir)/urllib
	$(fetch) $(target_dir)/urllib https://raw.githubusercontent.com/pfalcon/micropython-lib/5f619c88/urllib.parse/urllib/parse.py
	touch $(target_dir)/urllib/__init__.py

	# Install "micropython-base64" without 'micropython-binascii', 'micropython-re-pcre', 'micropython-struct'
	$(fetch) $(target_dir) https://raw.githubusercontent.com/pfalcon/micropython-lib/5f619c88/base64/base64.py

	# Install "micropython-logging" without "micropython-os"
	# to avoid collision with libraries shipped as Pycom builtins.
	mkdir -p $(target_dir)/logging
	$(fetch) $(target_dir)/logging https://raw.githubusercontent.com/pfalcon/micropython-lib/5f619c88/logging/logging/__init__.py
	$(fetch) $(target_dir)/logging https://raw.githubusercontent.com/pfalcon/micropython-lib/5f619c88/logging/logging/handlers.py

	# Install Pycom "mqtt.py"
	$(fetch) $(target_dir) https://raw.githubusercontent.com/pycom/pycom-libraries/6544105e/lib/mqtt/mqtt.py

	# Install Pycoproc Libary
	$(fetch) $(target_dir) https://raw.githubusercontent.com/pycom/pycom-libraries/681302a4/lib/pycoproc/pycoproc.py

	#Install quectel L76 GNSS library (Pytrack Board)
	$(fetch) $(target_dir) https://raw.githubusercontent.com/andrethemac/L76GLNSV4/b68b3402/L76GNSV4.py

	#Install Pytrack Board Libary
	$(fetch) $(target_dir) https://raw.githubusercontent.com/pycom/pycom-libraries/ce0cfa5/pytrack/lib/LIS2HH12.py

	#Install Pytrack Board Libary
	$(fetch) $(target_dir) https://raw.githubusercontent.com/pycom/pycom-libraries/0f123c7/pytrack/lib/pytrack.py

	#Install BME280 Libary
	$(fetch) $(target_dir) https://raw.githubusercontent.com/catdog2/mpy_bme280_esp8266/d7e052b/bme280.py

	# Install and patch "dotty_dict"
	# https://github.com/pawelzny/dotty_dict
	mkdir -p $(target_dir)/dotty_dict
	$(fetch) $(target_dir)/dotty_dict https://raw.githubusercontent.com/pawelzny/dotty_dict/c040a96/dotty_dict/__init__.py
	$(fetch) $(target_dir)/dotty_dict https://raw.githubusercontent.com/pawelzny/dotty_dict/c040a96/dotty_dict/dotty_dict.py
	patch --forward dist-packages/dotty_dict/dotty_dict.py tools/dotty_dict-01.patch || true

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



# ================
# Action utilities
# ================

list-serials:
	@$(rshell) --list

check-serial-port:
	@if test "${MCU_SERIAL_PORT}" = ""; then \
		echo "ERROR: Environment variable 'MCU_SERIAL_PORT' not set"; \
		exit 1; \
	fi

rshell: check-serial-port
	$(rshell) $(rshell_options)

repl: check-serial-port
	$(rshell) $(rshell_options) repl

console: check-serial-port
	$(miniterm) ${MCU_SERIAL_PORT} 115200

list-boards: check-serial-port
	@$(rshell) $(rshell_options) boards

device-info: check-serial-port
	@$(rshell) $(rshell_options) --quiet repl pyboard 'import os ~ os.uname() ~'

reset-device: check-serial-port
	@$(rshell) $(rshell_options) --quiet repl pyboard 'import machine ~ machine.reset() ~'

reset-device-attached: check-serial-port
	@$(rshell) $(rshell_options) --quiet repl pyboard 'import machine ~ machine.reset()'

reset-ampy:
	$(ampy) --port $(serial_port) --delay 1 reset


# =======================
# File transfer & Execute
# =======================

recycle: install-framework install-sketch reset-device-attached

sketch-and-run: install-sketch reset-device-attached


# =============
# File transfer
# =============

install: install-requirements install-framework install-sketch

install-requirements: check-serial-port
	$(rshell) $(rshell_options) mkdir /flash/dist-packages
	$(rshell) $(rshell_options) rsync dist-packages /flash/dist-packages

install-framework: check-serial-port
	$(rshell) $(rshell_options) --file tools/upload-framework.rshell

install-sketch: check-serial-port
	$(rshell) $(rshell_options) --file tools/upload-sketch.rshell

refresh-requirements:
	rm -r dist-packages
	$(MAKE) download-requirements
	$(rshell) $(rshell_options) rm -r /flash/dist-packages
	$(rshell) $(rshell_options) ls /flash/dist-packages
	$(MAKE) install-requirements

format-flash: check-serial-port

	@# Old version
	@# $(rshell) $(rshell_options) --file tools/clean.rshell

	$(eval retval := $(shell bash -c 'read -s -p "Format /flash on the device with LittleFS? This will delete your program. [y/n]? " outcome; echo $$outcome'))
	@if test "$(retval)" = "y"; then \
		echo; \
		\
		echo Creating LittleFS filesystem; \
		$(rshell) $(rshell_options) --quiet repl pyboard 'import pycom ~ pycom.bootmgr(fs_type=pycom.LittleFS, reset=True) ~'; \
		\
		echo Formatting filesystem; \
		$(rshell) $(rshell_options) --quiet repl pyboard 'import os ~ os.fsformat(\"/flash\") ~'; \
		\
		echo Resetting device; \
    	$(rshell) $(rshell_options) --quiet repl pyboard 'import machine ~ machine.reset() ~'; \
	fi


# --------------------
# Application specific
# --------------------
terkin: install-terkin
ratrack: install-ratrack

terkin: check-serial-port
	@#$(rshell) $(rshell_options) --file tools/upload-framework.rshell
	$(rshell) $(rshell_options) --file tools/upload-terkin.rshell

ratrack: check-serial-port
	# $(rshell) $(rshell_options) --file tools/upload-framework.rshell
	$(rshell) $(rshell_options) --file tools/upload-ratrack.rshell



# =========
# Releasing
# =========
prepare-release:

	@# Compute release name.
	$(eval name := hiveeyes-micropython-firmware)
	$(eval version := $(shell python3 -c 'import terkin; print(terkin.__version__)'))
	$(eval releasename := $(name)-$(version))

	@# Define directories.
	$(eval build_dir := ./build)
	$(eval work_dir := $(build_dir)/$(releasename))
	$(eval dist_dir := ./dist)

	@# Define archive names.
	$(eval tarfile := $(dist_dir)/$(releasename).tar.gz)
	$(eval zipfile := $(dist_dir)/$(releasename).zip)

create-release-archives: prepare-release

	@echo "Baking release artefacts for $(releasename)"

    # Remove release bundle archives.
	@rm -f $(tarfile)
	@rm -f $(zipfile)

    # Populate build directory.
	@mkdir -p $(work_dir)
	@rm -r $(work_dir)
	@mkdir -p $(work_dir)
	@cp -r dist-packages hiveeyes terkin lib boot.py main.py settings.example.py $(work_dir)

    # Create .tar.gz and .zip archives.
	tar -czf $(tarfile) -C $(build_dir) $(releasename)
	(cd $(build_dir); zip -r ../$(zipfile) $(releasename))

publish-release: prepare-release check-github-release create-release-archives

	@echo "Uploading release artefacts for $(releasename) to GitHub"

	@# Show current releases.
	@#$(github-release) info --user hiveeyes --repo hiveeyes-micropython-firmware

    # Create Release.
	@#$(github-release) release --user hiveeyes --repo hiveeyes-micropython-firmware --tag $(version) --draft
	@#$(github-release) release --user hiveeyes --repo hiveeyes-micropython-firmware --tag $(version)

    # Upload release artifacts.
	$(github-release) upload --user hiveeyes --repo hiveeyes-micropython-firmware --tag $(version) --name $(notdir $(tarfile)) --file $(tarfile) --replace
	$(github-release) upload --user hiveeyes --repo hiveeyes-micropython-firmware --tag $(version) --name $(notdir $(zipfile)) --file $(zipfile) --replace

release-and-publish: release publish-release
