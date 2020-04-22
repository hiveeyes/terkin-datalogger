# ======================
# github-release program
# ======================

$(eval github-release := ./bin/github-release)

check-github-release:
	@test -e $(github-release) || (echo 'ERROR: "github-release" not found.\nPlease install "github-release" to "./bin/github-release".\nSee https://github.com/meterup/github-release/releases\n'; exit 1)

install-github-release:
	# https://github.com/aktau/github-release
	$(eval url := https://github.com/meterup/github-release/releases/download/v0.7.5/darwin-amd64-github-release.tar.bz2)

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
	$(eval version := $(shell PYTHONPATH=./src/lib python3 -c 'import terkin; print(terkin.__version__)'))
	$(eval releasename := $(name)-$(version))

	@# Define directories.
	$(eval build_dir := ./build)
	$(eval dist_dir := ./dist/source)

	@# Define platform.
	$(eval platform := pycom)

	@# Ensure directories exist.
	@mkdir -p $(build_dir)
	@mkdir -p $(dist_dir)

create-source-archives: prepare-release

	$(eval artefact := $(releasename)-source)

	@# Define directories.
	$(eval work_dir := $(build_dir)/$(artefact))

	@# Define archive names.
	$(eval tarfile_source := $(dist_dir)/$(artefact).tar.gz)
	$(eval zipfile_source := $(dist_dir)/$(artefact).zip)

	@echo "Baking source release artefacts for $(artefact), target is $(dist_dir)"

	@# Remove release bundle archives.
	@rm -f $(tarfile_source)
	@rm -f $(zipfile_source)

	@# Clean build directory.
	@mkdir -p $(work_dir)
	@rm -r $(work_dir)
	@mkdir -p $(work_dir)

	@# Populate build directory.
	@cp -r dist-packages src/lib src/boot.py src/main.py src/settings.example*.py $(work_dir)

	@# Clean Python build artefacts.
	@find $(work_dir) -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

	@# Create .tar.gz and .zip archives.
	@tar -czf $(tarfile_source) -C $(build_dir) $(artefact)
	@(cd $(build_dir); zip -q -9 -r ../$(zipfile_source) $(artefact))

	$(github-release) upload --user hiveeyes --repo terkin-datalogger --tag $(version) --name $(notdir $(tarfile_source)) --file $(tarfile_source) --replace
	$(github-release) upload --user hiveeyes --repo terkin-datalogger --tag $(version) --name $(notdir $(zipfile_source)) --file $(zipfile_source) --replace

create-mpy-archives: prepare-release

	$(eval artefact := $(releasename)-$(platform)-mpy-$(MPY_VERSION))

	@# Define directories.
	$(eval work_dir := $(build_dir)/$(artefact))

	@# Define archive names.
	$(eval tarfile_mpy := $(dist_dir)/$(artefact).tar.gz)
	$(eval zipfile_mpy := $(dist_dir)/$(artefact).zip)

	@echo "Baking mpy release artefacts for $(artefact), target is $(dist_dir)"

	@# Remove release bundle archives.
	@rm -f $(tarfile_mpy)
	@rm -f $(zipfile_mpy)

	@# Clean build directory.
	@mkdir -p $(work_dir)
	@rm -r $(work_dir)
	@mkdir -p $(work_dir)
	@mkdir -p $(work_dir)/lib

	@# Precompile libraries.
	rm -rf lib-mpy
	$(MAKE) mpy-compile

	@# Populate build directory.
	@cp -r lib-mpy src/boot.py src/main.py src/settings.example*.py $(work_dir)
	@cp -r src/lib/umal.py src/lib/mininet.py $(work_dir)/lib

	@# Create .tar.gz and .zip archives.
	@tar -czf $(tarfile_mpy) -C $(build_dir) $(artefact)
	@(cd $(build_dir); zip -q -9 -r ../$(zipfile_mpy) $(artefact))

	$(github-release) upload --user hiveeyes --repo terkin-datalogger --tag $(version) --name $(notdir $(tarfile_mpy)) --file $(tarfile_mpy) --replace
	$(github-release) upload --user hiveeyes --repo terkin-datalogger --tag $(version) --name $(notdir $(zipfile_mpy)) --file $(zipfile_mpy) --replace

make-github-release: prepare-release

	@# Show current releases.
	@#$(github-release) info --user hiveeyes --repo terkin-datalogger

	@# Create Release.
	@#$(github-release) release --user hiveeyes --repo terkin-datalogger --tag $(version) --draft

	$(github-release) release --user hiveeyes --repo terkin-datalogger --tag $(version) || true

packages: check-github-release make-github-release

	@echo "Uploading release artefacts for $(releasename) to GitHub"

    # Source artifacts.
	$(MAKE) create-source-archives

    # mpy artifacts.
	MPY_TARGET=pycom MPY_VERSION=1.11 $(MAKE) create-mpy-archives platform=pycom
	MPY_TARGET=bytecode MPY_VERSION=1.12 $(MAKE) create-mpy-archives platform=genuine

## Release this piece of software
release: bumpversion push
	# Synopsis:
	#   "make release bump=minor"   (major,minor,patch)
