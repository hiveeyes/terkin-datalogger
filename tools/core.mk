# -----------
# Environment
# -----------

$(eval venv2path    := .venv2)
$(eval pip2         := $(venv2path)/bin/pip)
$(eval python2      := $(venv2path)/bin/python)
$(eval platformio   := $(venv2path)/bin/platformio)

$(eval venv3path    := .venv3)
$(eval pip3         := $(venv3path)/bin/pip)
$(eval python3      := $(venv3path)/bin/python)
$(eval ampy         := $(venv3path)/bin/ampy)
$(eval rshell       := $(venv3path)/bin/rshell)

$(eval github-release := ./bin/github-release)

# Setup Python virtualenv
setup-virtualenv2:
	@test -e $(python2) || `command -v virtualenv` --python=python2 --no-site-packages $(venv2path)

setup-virtualenv3:
	@test -e $(python3) || `command -v virtualenv` --python=python3 --no-site-packages $(venv3path)
	$(pip3) --quiet install --requirement requirements-dev.txt

setup-environment: setup-virtualenv3


# ----------------
# Serial interface
# ----------------
$(eval serial_port     := ${MCU_SERIAL_PORT})
$(eval serial_bufsize  := 2048)
$(eval rshell_options  := --port $(serial_port) --buffer-size $(serial_bufsize) --timing)


# ----------
# PlatformIO
# ----------

install-platformio: setup-virtualenv2
	@$(pip2) install platformio --quiet

build-all: install-platformio
	@$(platformio) run

build-env: install-platformio
	@$(platformio) run --environment $(environment)


# --------------
# github-release
# --------------

check-github-release:
	@test -e $(github-release) || (echo 'ERROR: "github-release" not found.\nPlease install "github-release" to "./bin/github-release".\nSee https://github.com/aktau/github-release\n'; exit 1)

install-github-release:
	# https://github.com/aktau/github-release
	$(eval url := https://github.com/aktau/github-release/releases/download/v0.7.2/darwin-amd64-github-release.tar.bz2)

	# NotYetImplemented
	@exit 1

	@#@test -e $(github-release) || cd tmp; wget $(url)
	@#$(eval github-release := $(tools_dir)tmp/bin/darwin/amd64/github-release)
