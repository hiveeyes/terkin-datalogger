###########################
Terkin Datalogger releasing
###########################


*****************
Cut a new release
*****************
::

    make release bump=minor


**************************************
Build and publish distribution package
**************************************
Create .tar.gz and .zip archive at ``dist`` directory, create release on GitHub and upload them::

    export GITHUB_TOKEN={redacted}
    make publish-release version=0.1.0

Create .tar.gz and .zip archive at ``dist`` directory only::

    make create-release-archives version=0.1.0



*********************
Build firmware images
*********************
For building self-contained firmware images, the
toolchain has to be installed appropriately. YMMV.


=============================
Genuine MicroPython for ESP32
=============================
Building is based on the ``FROZEN_MANIFEST`` file ``mpy_manifest.py`` included
within the Terkin Datalogger repository. The build process is straight forward::

    cd /home/develop/toolchain/micropython

    export PATH=/home/develop/toolchain/xtensa-esp32-elf-1.22.0-98/bin:$PATH
    export ESPIDF=/home/develop/toolchain/esp-idf
    make -j8 --directory=ports/esp32 BOARD=GENERIC_SPIRAM FROZEN_MANIFEST=/home/develop/hiveeyes/terkin-datalogger/mpy_manifest.py

The firmware image will be located at ``./ports/esp32/build-GENERIC_SPIRAM/firmware.bin``.


=============================
Genuine MicroPython for STM32
=============================
::

    cd /home/develop/toolchain/micropython
    make -j8 --directory=ports/stm32 BOARD=PYBD_SF6 FROZEN_MANIFEST=/home/develop/hiveeyes/terkin-datalogger/mpy_manifest.py


The firmware image will be located at ``./ports/stm32/build-PYBD_SF6/firmware.dfu``.


=================
Pycom MicroPython
=================
For building the Pycom firmware with frozen modules, there's a make target,
which will copy all source artifacts of the Terkin Datalogger into the frozen
directory appropriately::

    make sync-frozen path=/home/develop/toolchain/pycom-micropython-sigfox/esp32/frozen/Custom

After that, the regular build process may be started using::

    cd /home/develop/toolchain/pycom-micropython-sigfox/esp32

    export PATH=/home/develop/toolchain/xtensa-esp32-elf-1.22.0-98/bin:$PATH
    export IDF_PATH=/home/develop/toolchain/pycom-esp-idf
    make -j8 BOARD=FIPY VARIANT=BASE FS=LFS release
