# ======================
# github-release program
# ======================

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
	@cp -r dist-packages lib boot.py main.py settings.example*.py $(work_dir)
	@cp -r hiveeyes terkin $(work_dir)/lib

    # Create .tar.gz and .zip archives.
	tar -czf $(tarfile) -C $(build_dir) $(releasename)
	(cd $(build_dir); zip -r ../$(zipfile) $(releasename))

publish-release: prepare-release check-github-release create-release-archives

	@echo "Uploading release artefacts for $(releasename) to GitHub"

	@# Show current releases.
	@#$(github-release) info --user hiveeyes --repo hiveeyes-micropython-firmware

    # Create Release.
	@#$(github-release) release --user hiveeyes --repo hiveeyes-micropython-firmware --tag $(version) --draft
	$(github-release) release --user hiveeyes --repo hiveeyes-micropython-firmware --tag $(version)

    # Upload release artifacts.
	$(github-release) upload --user hiveeyes --repo hiveeyes-micropython-firmware --tag $(version) --name $(notdir $(tarfile)) --file $(tarfile) --replace
	$(github-release) upload --user hiveeyes --repo hiveeyes-micropython-firmware --tag $(version) --name $(notdir $(zipfile)) --file $(zipfile) --replace
