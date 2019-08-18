########################################
Hiveeyes MicroPython Datalogger research
########################################


************
Python tools
************
- https://github.com/pycampers/ampy
  https://pypi.org/project/adafruit-ampy/
- https://github.com/dhylands/rshell
- https://github.com/wendlers/mpfshell
- https://github.com/microhomie/microhomie/blob/master/install.mpf


**************
Python modules
**************
- https://github.com/lucien2k/sonoff-python
- https://xasyncsockets.hc2.fr/
  https://github.com/jczic/xAsyncSockets
- https://pypi.org/project/picotui/1.0/
- https://github.com/pfalcon/picoweb
  https://github.com/pfalcon/pycopy-lib/tree/master/uasyncio
- https://github.com/pycom/pycom-libraries/blob/master/examples/OTA/OTA_server.py


*******************
Pycom documentation
*******************
- https://github.com/pycom/pydocs/tree/master/firmwareapi/micropython
- https://github.com/pycom/pydocs/tree/master/firmwareapi/pycom
- https://micropython.readthedocs.io/en/latest/library/index.html


***************
Pycom resources
***************
- https://github.com/pycom/pycom-micropython-sigfox/tree/release-candidate
- https://software.pycom.io/downloads/FiPy.html
- https://software.pycom.io/downloads/FiPy-1.20.0.rc7.tar.gz
- https://github.com/pycom/pycom-micropython-sigfox/archive/release-candidate.tar.gz



*****
Notes
*****
- The board advertises itself as ‘wipy-wlan-xxxx’ or ‘sipy-wlan-xxxx’ or something similar where ‘xxxx’
  are four hexadecimal digits. The password for all these networks is ‘www.pycom.io’::

    Default AP WiFi credentials.

    2 fipy-wlan-42bc (3, 'www.pycom.io') 0

- To compile before uploading and upload the compiled file (you need mpy-cross in your path)::

    mpfs > putc boot.py



platformio device list::

    /dev/cu.usbmodemPye090a1
    ------------------------
    Hardware ID: USB VID:PID=04D8:EF98 SER=Pye090a1 LOCATION=20-2
    Description: Expansion3

How to reset machine using rshell?
::

    #repl

    #repl pyboard import sys~
    #repl pyboard sys.exit()~

    #repl pyboard from main import reset~
    #repl pyboard reset()





*********************
Compile the whole SDK
*********************
::

    make build-env environment=fipy


https://github.com/pycom/pycom-micropython-sigfox
~/.platformio/packages/toolchain-xtensa32/xtensa-esp32-elf/

~/.platformio/packages/toolchain-xtensa32/bin/xtensa-esp32-elf-gcc --version
xtensa-esp32-elf-gcc (crosstool-NG crosstool-ng-1.22.0-80-g6c4433a) 5.2.0


::

    brew install micropython

    git clone --depth=1 https://github.com/pycom/pycom-micropython-sigfox.git
    git clone --depth=1 https://github.com/pycom/pycom-esp-idf.git

    git clone --recursive --branch release-candidate --depth=1 https://github.com/pycom/pycom-micropython-sigfox.git
    git clone --recursive --branch idf_v3.1 --depth=1 https://github.com/pycom/pycom-esp-idf.git

    cd pycom-micropython-sigfox
    git checkout release-candidate
    git submodule update --init


    cd pycom-esp-idf
    git submodule update --init


    cd pycom-micropython-sigfox
    export PATH=$PATH:$HOME/.platformio/packages/toolchain-xtensa32/bin

    cd mpy-cross && make clean && make && cd ..


    cd esp32
    export IDF_PATH=/Users/amo/dev/hiveeyes/tools/pycom/pycom-esp-idf
    export BUILD_VERBOSE=1

    # Make sure that your board is placed into programming mode, otherwise flashing will fail.
    # Put device into programming mode
    https://docs.pycom.io/gettingstarted/programming/safeboot.html#bootloader

    # Hold down the button while booting


    make BOARD=FIPY clean
    make BOARD=FIPY
    make BOARD=FIPY flash





    make BOARD=FIPY clean
    make BOARD=FIPY TARGET=boot

    source .venv2/bin/activate
    python /Users/amo/dev/hiveeyes/tools/pycom-micropython-sigfox/esp32/../../pycom-esp-idf/components/esptool_py/esptool/esptool.py --chip esp32 elf2image --flash_mode dio --flash_freq 80m -o build/FIPY/release/bootloader/bootloader.bin build/FIPY/release/bootloader/bootloader.elf
    deactivate

    make BOARD=FIPY TARGET=app
    make BOARD=FIPY flash
