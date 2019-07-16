# =======================
# The MicroTerkin sandbox
# =======================

# Synopsis:
#
#   https://community.hiveeyes.org/t/terkin-for-micropython/233/21
#
#   git pull
#   make setup
#   make terkin-agent action=maintain
#   export MCU_PORT=192.168.178.33
#   make install-ng
#   make console
#
# - Press reset button
# - Have fun

include tools/core.mk
include tools/micropython.mk
include tools/setup.mk
include tools/release.mk


# -----
# Setup
# -----
setup: setup-environment download-requirements


# -----------------------
# Discovery & Maintenance
# -----------------------
setup-terkin-agent:
	$(pip3) install -r requirements-terkin-agent.txt

terkin-agent: setup-terkin-agent
	sudo $(python3) tools/terkin.py $(action)


# -----------------------
# File transfer & Execute
# -----------------------

recycle: install-framework install-sketch reset-device-attached

sketch-and-run: install-sketch reset-device-attached


# ------------------
# File transfer solo
# ------------------

install: install-requirements install-framework install-sketch

install-ftp:
	lftp -u micro,python ${MCU_PORT} < tools/upload-all.lftprc

install-ng:
	@if test "${mcu_port_type}" = "ip"; then \
		$(MAKE) install-ftp; \
	else \
		$(MAKE) install; \
	fi

install-pycom-firmware:
	$(pycom_fwtool_cli) --verbose --port $(MCU_PORT) flash --tar dist-firmwares/fipy/FiPy-1.20.0.rc11.tar.gz

install-requirements: check-mcu-port
	$(rshell) $(rshell_options) mkdir /flash/dist-packages
	$(rshell) $(rshell_options) rsync dist-packages /flash/dist-packages

install-framework: check-mcu-port
	$(rshell) $(rshell_options) --file tools/upload-framework.rshell

install-sketch: check-mcu-port
	$(rshell) $(rshell_options) --file tools/upload-sketch.rshell

refresh-requirements: check-mcu-port
	rm -r dist-packages
	$(MAKE) download-requirements
	$(rshell) $(rshell_options) rm -r /flash/dist-packages
	$(rshell) $(rshell_options) ls /flash/dist-packages
	$(MAKE) install-requirements


# ------------
# Applications
# ------------
terkin: install-terkin
ratrack: install-ratrack

terkin: check-mcu-port
	@#$(rshell) $(rshell_options) --file tools/upload-framework.rshell
	$(rshell) $(rshell_options) --file tools/upload-terkin.rshell

ratrack: check-mcu-port
	# $(rshell) $(rshell_options) --file tools/upload-framework.rshell
	$(rshell) $(rshell_options) --file tools/upload-ratrack.rshell



# ---------
# Releasing
# ---------

#release-and-publish: release publish-release

# Release this piece of software
# Synopsis:
#   make release bump=minor  (major,minor,patch)
release: bumpversion push publish-release
