include tools/core.mk


# =====
# Setup
# =====

setup: setup-environment install-requirements upload-requirements

install-requirements:

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

	# Install Pycom "mqtt.py"
	$(fetch) $(target_dir) https://raw.githubusercontent.com/pycom/pycom-libraries/6544105e/lib/mqtt/mqtt.py

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
	$(fetch) $(target_dir)/onewire https://raw.githubusercontent.com/micropython/micropython/a065d78/drivers/onewire/ds18x20.py

	# Install PyCayenneLPP from Git repository.
	$(eval tmpdir := ./.pycayennelpp.tmp)
	rm -rf $(tmpdir)
	mkdir -p $(tmpdir)
	git clone https://github.com/hiveeyes/pycayennelpp $(tmpdir)
	rm -r $(tmpdir)/cayennelpp/tests
	cp -r $(tmpdir)/cayennelpp $(target_dir)/
	rm -rf $(tmpdir)


upload-requirements:
	$(rshell) $(rshell_options) mkdir /flash/dist-packages
	$(rshell) $(rshell_options) rsync dist-packages /flash/dist-packages


refresh-requirements:
	rm -r dist-packages
	$(MAKE) install-requirements
	$(rshell) $(rshell_options) rm -r /flash/dist-packages
	$(rshell) $(rshell_options) ls /flash/dist-packages
	$(MAKE) upload-requirements


# =========
# Utilities
# =========

check-serial-port:
	@if test "${MCU_SERIAL_PORT}" = ""; then \
		echo "ERROR: Environment variable 'MCU_SERIAL_PORT' not set"; \
		exit 1; \
	fi

rshell: check-serial-port
	$(rshell) $(rshell_options)

repl: check-serial-port
	$(rshell) $(rshell_options) repl

reset: check-serial-port
	$(rshell) $(rshell_options) --file tools/reset.rshell

recycle: check-serial-port
	$(rshell) $(rshell_options) --file tools/upload-requirements.rshell
	$(rshell) $(rshell_options) --file tools/upload-sketch.rshell
	@#$(MAKE) reset

list-serials:
	@$(rshell) --list

list-boards: check-serial-port
	@$(rshell) $(rshell_options) boards


# =============
# Miscellaneous
# =============

reset-defunct:
	$(ampy) --port $(serial_port) --delay 1 reset

upload-things:
	@echo "Uploading main application: main.py and settings.py"
	$(rshell) $(rshell_options) cp boot.py /flash
	$(rshell) $(rshell_options) cp main.py /flash
	$(rshell) $(rshell_options) cp settings.py /flash

upload-lib:
	$(rshell) $(rshell_options) rsync ./lib /flash/lib


# =========
# Releasing
# =========
check-version:
	@if test "$(version)" = ""; then \
		echo "ERROR: Make variable 'version' not set"; \
		exit 1; \
	fi

create-release-archives: check-version
	$(eval name := hiveeyes-micropython-firmware)
	$(eval releasename := $(name)-$(version))
	$(eval build_dir := ./build)
	$(eval work_dir := $(build_dir)/$(releasename))
	$(eval dist_dir := ./dist)

    # Populate build directory.
	mkdir -p $(work_dir)
	cp -r dist-packages hiveeyes terkin lib boot.py main.py settings.example.py $(work_dir)

    # Create .tar.gz and .zip archives.
	tar -czf $(dist_dir)/$(releasename).tar.gz -C $(build_dir) $(releasename)
	(cd $(build_dir); zip -r ../$(dist_dir)/$(releasename).zip $(releasename))

publish-release: check-version check-github-release create-release-archives
	$(eval name := hiveeyes-micropython-firmware)
	$(eval releasename := $(name)-$(version))
	$(eval dist_dir := ./dist)
	$(eval dist_file_tar := $(dist_dir)/$(releasename).tar.gz)
	$(eval dist_file_zip := $(dist_dir)/$(releasename).zip)

	# Show current releases.
	$(github-release) info --user hiveeyes --repo hiveeyes-micropython-firmware

    # Create Release.
	@#$(github-release) release --user hiveeyes --repo hiveeyes-micropython-firmware --tag $(version) --draft
	$(github-release) release --user hiveeyes --repo hiveeyes-micropython-firmware --tag $(version)

    # Upload release artifacts.
	$(github-release) upload --user hiveeyes --repo hiveeyes-micropython-firmware --tag $(version) --name $(notdir $(dist_file_tar)) --file $(dist_file_tar) --replace
	$(github-release) upload --user hiveeyes --repo hiveeyes-micropython-firmware --tag $(version) --name $(notdir $(dist_file_zip)) --file $(dist_file_zip) --replace
