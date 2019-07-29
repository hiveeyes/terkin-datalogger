# -*- coding: utf-8 -*-
#
# Hiveeyes MicroPython Datalogger
# https://github.com/hiveeyes/hiveeyes-micropython-firmware
#
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
#
"""
-----
Setup
-----

Just run::

    make setup
    make install

to bring everything into shape.

Then, invoke::

    make sketch-and-run

to upload the program and reset the ESP32.
"""


def extend_syspath():
    """
    Extend Python module search path.
    Dependency modules are shipped through the "dist-packages" folder.
    Please populate this folder appropriately as shown above before
    expecting anything to work.
    """
    import sys

    # vanilla: ['', '/flash', '/flash/lib']

    sys.path[0:0] = ['/flash/lib-mpy']
    sys.path.extend(['dist-packages', 'terkin', 'hiveeyes'])

    print('[boot.py] INFO: Python module search path is:', sys.path)


if __name__ == '__main__':

    # Enable heartbeat LED.
    """
    try:
        import pycom
        pycom.heartbeat(True)
    except:
        pass
    """

    # Extend module search path.
    extend_syspath()
