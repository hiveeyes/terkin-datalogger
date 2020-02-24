# FROZEN_MANIFEST file for building firmware images for Genuine MicroPython.
# https://github.com/hiveeyes/terkin-datalogger/blob/master/doc/release.rst#build-firmware-images
include('$(PORT_DIR)/boards/manifest.py')
freeze('dist-packages')
freeze('src/lib')
