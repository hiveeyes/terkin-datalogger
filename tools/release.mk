# ======================
# github-release program
# ======================

$(eval github-release := ./bin/github-release)

check-github-release:
	@test -e $(github-release) || (echo 'ERROR: "github-release" not found.\nPlease install "github-release" to "./bin/github-release".\nSee https://github.com/aktau/github-release\n'; exit 1)

install-github-release:
	# https://github.com/aktau/github-release
	$(eval url := https://github.com/aktau/github-release/releases/download/v0.7.2/darwin-amd64-github-release.tar.bz2)

	# NotYetImplemented
	@exit 1

	@#@test -e $(github-release) || cd tmp; wget $(url)
	@#$(eval github-release := $(tools_dir)tmp/bin/darwin/amd64/github-release)


# =========
# Releasing
# =========

prepare-release:

	@# Compute release name.
	$(eval name := terkin-datalogger)
	$(eval version := $(shell python3 -c 'import terkin; print(terkin.__version__)'))
	$(eval releasename := $(name)-$(version))

	@# Define directories.
	$(eval build_dir := ./build)
	$(eval dist_dir := ./dist)

	@# Define platform.
	$(eval platform := pycom)

create-source-archives: prepare-release

	$(eval artefact := $(releasename)-source)

	@# Define directories.
	$(eval work_dir := $(build_dir)/$(artefact))

	@# Define archive names.
	$(eval tarfile_source := $(dist_dir)/$(artefact).tar.gz)
	$(eval zipfile_source := $(dist_dir)/$(artefact).zip)

	@echo "Baking source release artefacts for $(artefact)"

    # Remove release bundle archives.
	@rm -f $(tarfile_source)
	@rm -f $(zipfile_source)

    # Populate build directory.
	@mkdir -p $(work_dir)
	@rm -r $(work_dir)
	@mkdir -p $(work_dir)

	@cp -r dist-packages lib src/boot.py src/main.py src/settings.example*.py $(work_dir)

    # Create .tar.gz and .zip archives.
	tar -czf $(tarfile_source) -C $(build_dir) $(artefact)
	(cd $(build_dir); zip -9 -r ../$(zipfile_source) $(artefact))

create-mpy-archives: prepare-release

	$(eval artefact := $(releasename)-$(platform)-mpy)

	@# Define directories.
	$(eval work_dir := $(build_dir)/$(artefact))

	@# Define archive names.
	$(eval tarfile_mpy := $(dist_dir)/$(artefact).tar.gz)
	$(eval zipfile_mpy := $(dist_dir)/$(artefact).zip)

	@echo "Baking source release artefacts for $(artefact)"

    # Remove release bundle archives.
	@rm -f $(tarfile_mpy)
	@rm -f $(zipfile_mpy)

    # Populate build directory.
	@mkdir -p $(work_dir)
	@rm -r $(work_dir)
	@mkdir -p $(work_dir)
	@mkdir -p $(work_dir)/lib

	@cp -r lib-mpy src/boot.py src/main.py src/settings.example*.py $(work_dir)
	@cp -r lib/umal.py lib/mininet.py $(work_dir)/lib

    # Create .tar.gz and .zip archives.
	tar -czf $(tarfile_mpy) -C $(build_dir) $(artefact)
	(cd $(build_dir); zip -9 -r ../$(zipfile_mpy) $(artefact))

build-release: prepare-release create-source-archives create-mpy-archives

publish-release: check-github-release build-release

	@echo "Uploading release artefacts for $(releasename) to GitHub"

	@# Show current releases.
	@#$(github-release) info --user hiveeyes --repo terkin-datalogger

    # Create Release.
	@#$(github-release) release --user hiveeyes --repo terkin-datalogger --tag $(version) --draft

	$(github-release) release --user hiveeyes --repo terkin-datalogger --tag $(version) || true

    # Upload source release artifacts.
	$(github-release) upload --user hiveeyes --repo terkin-datalogger --tag $(version) --name $(notdir $(tarfile_source)) --file $(tarfile_source) --replace
	$(github-release) upload --user hiveeyes --repo terkin-datalogger --tag $(version) --name $(notdir $(zipfile_source)) --file $(zipfile_source) --replace

    # Upload mpy release artifacts.
	$(github-release) upload --user hiveeyes --repo terkin-datalogger --tag $(version) --name $(notdir $(tarfile_mpy)) --file $(tarfile_mpy) --replace
	$(github-release) upload --user hiveeyes --repo terkin-datalogger --tag $(version) --name $(notdir $(zipfile_mpy)) --file $(zipfile_mpy) --replace


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
	rsync -auv --exclude=__pycache__ dist-packages/* lib/* $(path)


## Release this piece of software
release: bumpversion push publish-release
	# Synopsis:
	#   "make release bump=minor"   (major,minor,patch)


# -------
# Testing
# -------
build-annapurna:
	docker run -v `pwd`/dist-packages:/opt/frozen -it goinvent/pycom-fw build FIPY annapurna-0.6.0dev2 v1.20.0.rc12.1 idf_v3.1
