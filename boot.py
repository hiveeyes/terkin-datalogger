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
Please check https://community.hiveeyes.org/t/operate-the-terkin-datalogger-sandbox/2332
in order to get an idea how to operate this software sandbox.

Have fun!
"""


# Global reference to Bootloader object.
bootloader = None


if __name__ == '__main__':

    import sys
    print('[boot.py] INFO: Python module search path is:', sys.path)

    # Extend module search path.
    print('[boot.py] INFO: Starting "mboot" bootloader')
    from mboot import MicroPythonBootloader
    bootloader = MicroPythonBootloader()
    bootloader.extend_syspath()
