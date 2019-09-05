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

$(eval venv3path    := .venv3)
$(eval pip3         := $(venv3path)/bin/pip)
$(eval python3      := $(venv3path)/bin/python)
$(eval ampy         := $(venv3path)/bin/ampy)
$(eval rshell       := $(venv3path)/bin/rshell)
$(eval miniterm     := $(venv3path)/bin/miniterm.py)

$(eval bumpversion  := $(venv3path)/bin/bumpversion)


# ------------------
# Python virtualenvs
# -------------------
check-virtualenv:
	@$(MAKE) check-program program="virtualenv" hint="Install on Debian-based systems using 'apt install python-virtualenv python3-virtualenv' or use the package manager of your choice"

setup-virtualenv2: check-virtualenv
	virtualenv --python=python2 --no-site-packages $(venv2path)

setup-virtualenv3: check-virtualenv
	virtualenv --python=python3 --no-site-packages $(venv3path)
	$(pip3) --quiet install --requirement requirements-dev.txt

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

	@if test "${RUNNING_IN_HELL}" != "true" -a "${RUNNING_IN_WSL}" != "true"; then \
		$(python3) tools/terkin.py notify "$(message)" "$(status)"; \
	fi

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
	@if test "$(shell command -v $(program))" = ""; then \
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
NO_COLOR=\x1b[0m
MAGENTA_DARK_COLOR=\x1b[35m
GREEN_COLOR=\x1b[32;01m
RED_COLOR=\x1b[31;01m
ORANGE_COLOR=\x1b[38;5;208m
YELLOW_COLOR=\x1b[33;01m
CYAN_COLOR=\x1b[36;01m
BOLD=\x1b[1m
UNDERLINE=\x1b[4m
REVERSED=\x1b[7m

OK=$(GREEN_COLOR)[OK]     $(NO_COLOR)
INFO=$(NO_COLOR)[INFO]   $(NO_COLOR)
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
