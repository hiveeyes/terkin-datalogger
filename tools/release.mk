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
	$(eval name := hiveeyes-micropython-firmware)
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

	@cp -r dist-packages lib boot.py main.py settings.example*.py $(work_dir)
	@cp -r hiveeyes terkin $(work_dir)/lib

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

	@cp -r lib-mpy boot.py main.py settings.example*.py $(work_dir)
	@cp -r lib/mboot.py lib/mininet.py $(work_dir)/lib

    # Create .tar.gz and .zip archives.
	tar -czf $(tarfile_mpy) -C $(build_dir) $(artefact)
	(cd $(build_dir); zip -9 -r ../$(zipfile_mpy) $(artefact))

build-release: prepare-release create-source-archives create-mpy-archives

publish-release: check-github-release build-release

	@echo "Uploading release artefacts for $(releasename) to GitHub"

	@# Show current releases.
	@#$(github-release) info --user hiveeyes --repo hiveeyes-micropython-firmware

    # Create Release.
	@#$(github-release) release --user hiveeyes --repo hiveeyes-micropython-firmware --tag $(version) --draft

	$(github-release) release --user hiveeyes --repo hiveeyes-micropython-firmware --tag $(version) || true

    # Upload source release artifacts.
	$(github-release) upload --user hiveeyes --repo hiveeyes-micropython-firmware --tag $(version) --name $(notdir $(tarfile_source)) --file $(tarfile_source) --replace
	$(github-release) upload --user hiveeyes --repo hiveeyes-micropython-firmware --tag $(version) --name $(notdir $(zipfile_source)) --file $(zipfile_source) --replace

    # Upload mpy release artifacts.
	$(github-release) upload --user hiveeyes --repo hiveeyes-micropython-firmware --tag $(version) --name $(notdir $(tarfile_mpy)) --file $(tarfile_mpy) --replace
	$(github-release) upload --user hiveeyes --repo hiveeyes-micropython-firmware --tag $(version) --name $(notdir $(zipfile_mpy)) --file $(zipfile_mpy) --replace
