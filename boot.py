# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3

from machine import UART
import pycom
import machine
import os


def extend_syspath():
    """
    Extend Python module search path.
    Dependency modules are shipped through the "dist-packages" folder.
    Please populate this folder appropriately before expecting anything to work.

    Just run:

        make install-requirements

    to bring everything into shape.
    """
    import sys
    sys.path.append('dist-packages')
    print('[boot.py] INFO: Python module search path is:', sys.path)
    print()


if __name__ == '__main__':
    pycom.heartbeat(False)
    uart = UART(0, baudrate=115200)
    os.dupterm(uart)
    extend_syspath()
