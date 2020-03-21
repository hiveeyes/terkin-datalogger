# =================
# Firmware building
# =================

## Copy source artifacts to MicroPython's frozen module folder
sync-frozen:

	@if test "${path}" = ""; then \
		echo "Frozen module path not given, please invoke \"make sync-frozen path=/home/develop/pycom/pycom-micropython-sigfox/esp32/frozen/Custom\"."; \
		exit 1; \
	fi

	@if ! test -e "${path}"; then \
		echo "Frozen module path at ${path} does not exist."; \
		exit 1; \
	fi

	echo "Deleting all modules from $(path)"
	rm -rf $(path)/*

	echo "Copying modules to $(frozen_path)"
	rsync -auv --exclude=__pycache__ dist-packages/* src/lib/* $(path)


build-firmware-esp32-generic: install-buildtools
	$(python3) -m tools.build --vendor=genuine --micropython="$(FWB_MICROPYTHON_GENUINE)" --toolchain="$(FWB_XTENSA_GCC)" --espidf="$(FWB_ESPIDF_GENUINE)" --architecture="esp32" --board="GENERIC_SPIRAM" --label="Annapurna-0.2.0" --manifest="mpy_manifest.py"  --release-path="./dist"

build-firmware-esp32-pycom: install-buildtools
	$(python3) -m tools.build --vendor=pycom --micropython="$(FWB_MICROPYTHON_PYCOM)" --toolchain="$(FWB_XTENSA_GCC)" --espidf="$(FWB_ESPIDF_PYCOM)" --architecture="esp32" --board="LOPY4" --sources='dist-packages/*,src/lib/*' --release-path="./dist"

install-buildtools: setup-virtualenv3
	@$(pip3) install --quiet --requirement requirements-build.txt --upgrade


# -------
# Testing
# -------
build-annapurna:
	docker run -v `pwd`/dist-packages:/opt/frozen -it goinvent/pycom-fw build FIPY annapurna-0.6.0dev2 v1.20.0.rc12.1 idf_v3.1
