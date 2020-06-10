#######################
Pycom firmware bundling
#######################


************
Introduction
************
In order to bundle an appropriate release tarball to be used
flashing through ``pycom-fwtool-cli``, you will have to take
the appropriate steps.

See also https://forum.pycom.io/topic/4518/firmware-update-elf-vs-tar.

************
Step by step
************

Install ``esptool`` into Python virtualenv::

    .venv3/bin/pip install esptool
    pio run

Get and extract vanilla tarball::

    # Download confirmed tarball release.
    wget https://packages.hiveeyes.org/hiveeyes/foss/pycom/FiPy-1.20.1.r1.tar.gz

    # Extract into temporary build directory.
    mkdir build
    tar -xzf FiPy-1.20.1.r1.tar.gz --directory build

Use Pycom firmware release (ELF file)::

    # Download most recent ELF file as of 2019-10-17.
    http --download --follow https://github.com/pycom/pycom-micropython-sigfox/releases/download/v1.20.1.r1/FiPy-1.20.1.r1-application.elf

    # Convert to image file and put into place.
    esptool.py --chip esp32 elf2image --output build/fipy.bin FiPy-1.20.1.r1-application.elf

Create new tarball::

    cd build; tar -czf ../FiPy-1.20.1.r1-rebundled.tar.gz *; cd -

Flash to device::

    pycom-fwtool-cli --verbose --port $MCU_PORT flash --tar FiPy-1.20.1.r1-rebundled.tar.gz
