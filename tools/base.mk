# -----------
# Environment
# -----------

# Better safe than sorry
export LANG=en_US

# Ignore deprecation warnings in Python
# https://stackoverflow.com/questions/879173/how-to-ignore-deprecation-warnings-in-python/879249
export PYTHONWARNINGS=ignore:Deprecation

# Define content of virtualenvs
$(eval venv2path    := .venv2)
$(eval pip2         := $(venv2path)/bin/pip)
$(eval python2      := $(venv2path)/bin/python)
$(eval platformio   := $(venv2path)/bin/platformio)

$(eval venvpath    := .venv)
$(eval pip3         := $(venvpath)/bin/pip)
$(eval python3      := $(venvpath)/bin/python)
$(eval ampy         := $(venvpath)/bin/ampy)
$(eval rshell       := $(venvpath)/bin/rshell)
$(eval miniterm     := $(venvpath)/bin/miniterm.py)

$(eval bumpversion  := $(venvpath)/bin/bumpversion)
$(eval pytest       := $(venvpath)/bin/pytest)
$(eval coverage     := $(venvpath)/bin/coverage)


# ------------------
# Python virtualenvs
# ------------------
check-virtualenv:
	@$(MAKE) check-program program="virtualenv" hint="Install on Debian-based systems using 'apt install python-virtualenv python3-virtualenv' or use the package manager of your choice"

setup-virtualenv2: check-virtualenv
	virtualenv --python=python2 $(venv2path)

setup-virtualenv3:
	@test -e $(python3) || python3 -m venv $(venvpath)
	@$(pip3) --quiet install --requirement requirements-dev.txt

setup-environment: setup-virtualenv3


# --------------
# Workstation OS
# --------------

# Poor man's operating system detection
# https://renenyffenegger.ch/notes/development/make/detect-os
# https://gist.github.com/sighingnow/deee806603ec9274fd47
# https://stackoverflow.com/questions/714100/os-detecting-makefile/14777895#14777895

UNAME=$(shell uname -a 2> /dev/null)
OSNAME=$(shell uname -s 2> /dev/null)

ifeq ($(OS),Windows_NT)
    $(eval RUNNING_IN_HELL := true)
endif
ifneq (,$(findstring Microsoft,$(UNAME)))
    $(eval RUNNING_IN_WSL := true)
endif

## Display operating system information
uname:
	@echo "OSNAME           $(OSNAME)"
	@echo "UNAME            $(UNAME)"
	@echo "RUNNING_IN_HELL  $(RUNNING_IN_HELL)"
	@echo "RUNNING_IN_WSL   $(RUNNING_IN_WSL)"


# ----------
# PlatformIO
# ----------

install-platformio: setup-virtualenv2
	@$(pip2) install platformio --quiet

build-all: install-platformio
	@$(platformio) run

build-env: install-platformio
	@$(platformio) run --environment $(environment)


# -------
# Release
# -------

# Release this piece of software
# Synopsis:
#   make release bump=minor  (major,minor,patch)
#release: bumpversion push

bumpversion: install-releasetools
	@$(bumpversion) $(bump)

push:
	git push && git push --tags

install-releasetools: setup-virtualenv3
	@$(pip3) install --quiet --requirement requirements-release.txt --upgrade


# --------------
# Software tests
# --------------
PYTEST_OPTIONS="--log-level DEBUG --log-format='%(asctime)-15s [%(name)-35s] %(levelname)-8s: %(message)s' --log-date-format='%Y-%m-%dT%H:%M:%S%z' --verbose"

## Setup requirements for running the testsuite
setup-tests: setup-virtualenv3
	$(pip3) install --requirement requirements-test.txt

.PHONY: test
## Run testsuite
test:
	@export PYTEST_ADDOPTS=$(PYTEST_OPTIONS) && \
	    $(pytest) test -m "$(marker)"

## Run testsuite, with verbose output
test-verbose:
	@export PYTEST_ADDOPTS=$(PYTEST_OPTIONS) && \
	    $(pytest) --log-cli-level=DEBUG test -m "$(marker)"

## Run testsuite, with coverage report
test-coverage:
	$(coverage) run -m pytest -vv
	$(coverage) report


# -------------
# Miscellaneous
# -------------
sleep:
	@sleep 1

notify:

	@if test "${status_ansi}" != ""; then \
		echo "$(status_ansi) $(message)"; \
    else \
		echo "$(status) $(message)"; \
	fi

	@$(python3) -m tools.notify "$(message)" "$(status)" || true

prompt_yesno:
	$(eval retval := $(shell bash -c 'read -s -p " [y/n] " outcome; echo $$outcome'))
	@echo $(retval)

	@if test "$(retval)" != "y"; then \
		exit 1; \
	fi

confirm:
	@# Prompt the user to confirm action.
	@printf "$(CONFIRM) $(text)"
	@$(MAKE) prompt_yesno

check-program:
	@if test "$(shell which $(program))" = ""; then \
		echo "ERROR: \"$(program)\" program not installed."; \
		echo "HINT: $(hint)"; \
		exit 1; \
	fi


# Variable debugging.
# https://blog.jgc.org/2015/04/the-one-line-you-should-add-to-every.html
## It allows you to quickly get the value of any makefile variable, e.g. "make print-MCU_PORT"
print-%: ; @echo $*=$($*)


# Colors!
# http://jamesdolan.blogspot.com/2009/10/color-coding-makefile-output.html
# http://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html
NO_COLOR=\033[0m
MAGENTA_DARK_COLOR=\033[35m
GREEN_COLOR=\033[32;01m
RED_COLOR=\033[31;01m
ORANGE_COLOR=\033[38;5;208m
YELLOW_COLOR=\033[33;01m
BLUE_COLOR=\033[34;01m
CYAN_COLOR=\033[36;01m
BOLD=\033[1m
UNDERLINE=\033[4m
REVERSED=\033[7m

OK=$(GREEN_COLOR)[OK]     $(NO_COLOR)
INFO=$(BLUE_COLOR)[INFO]   $(NO_COLOR)
ERROR=$(RED_COLOR)[ERROR]  $(NO_COLOR)
WARNING=$(ORANGE_COLOR)[WARNING]$(NO_COLOR)
ADVICE=$(CYAN_COLOR)[ADVICE] $(NO_COLOR)
CONFIRM=$(YELLOW_COLOR)[CONFIRM]$(NO_COLOR)


colors:
	@echo --- 1st ---
	@echo "$(MAGENTA_DARK_COLOR)Magenta 8$(NO_COLOR)"
	@echo "$(YELLOW_COLOR)Bright Yellow 16$(NO_COLOR)"
	@echo "$(ORANGE_COLOR)Orange 256$(NO_COLOR)"
	@echo "$$(tput setaf 6)Cyan (tput)$$(tput sgr0)"
	@echo "$$(tput setaf 6)$$(tput bold)Cyan Bold (tput)$$(tput sgr0)"

	@echo --- 2nd ---
	@printf "$(MAGENTA_DARK_COLOR)Magenta 8$(NO_COLOR)\n"
	@printf "$(YELLOW_COLOR)Bright Yellow 16$(NO_COLOR)\n"
	@printf "$(ORANGE_COLOR)Orange 256$(NO_COLOR)\n"
