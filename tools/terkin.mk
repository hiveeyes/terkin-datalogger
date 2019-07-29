# ================
# Programming port
# ================

# Use MCU_PORT environment variable
$(eval mcu_port     := ${MCU_PORT})

# Fall back to MCU_SERIAL_PORT environment variable
ifeq ($(mcu_port),)
    $(eval mcu_port := ${MCU_SERIAL_PORT})
endif

# Fall back to value from .terkin/floatip
ifeq ($(mcu_port),)
    $(eval mcu_port := $(shell cat '.terkin/floatip'))
endif

# Set default options for rshell
$(eval mcu_transfer_buffer  := 2048)

# Determine mcu port type
ifneq ($(mcu_port),)
    ifneq (,$(findstring /dev,$(mcu_port)))
        $(eval mcu_port_type := usb)
    else
        $(eval mcu_port_type := ip)
    endif
endif

# Sanity-check MCU_PORT
check-mcu-port:
	@#echo Connecting via port type $(mcu_port_type)
	@echo "Device port: ${mcu_port_type} => ${mcu_port}"
	@if test "${mcu_port}" = ""; then \
        echo "MCU port could not be obtained, please set MCU_PORT environment variable or populate .terkin/floatip"; \
        exit 1; \
	fi


# ===========
# Compilation
# ===========

# Whether to use mpy-cross
$(eval mpy_cross     := ${MPY_CROSS})
