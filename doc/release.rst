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


********************************
Build and publish firmware image
********************************

=================
Pycom MicroPython
=================
For building the Pycom firmware with frozen modules, there's a make target,
which will copy source artifacts of the Terkin Datalogger into the frozen
directory appropriately::

    make sync-frozen path=/home/develop/pycom/pycom-micropython-sigfox/esp32/frozen/Custom

After that, the regular build process may be started using::

    cd /home/develop/pycom/pycom-micropython-sigfox/esp32

    export BOARD=FIPY
    make -j8 BOARD=${BOARD} VARIANT=BASE FS=LFS release
