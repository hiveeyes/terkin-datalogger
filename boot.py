# -*- coding: utf-8 -*-
#
# Hiveeyes MicroPython Datalogger
# https://github.com/hiveeyes/hiveeyes-micropython-firmware
#
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
#
import pycom


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

    # Done by ``self.device.enable_serial()`` already.
    # import os; from machine import UART
    # uart = UART(0, baudrate=115200); os.dupterm(uart)

    extend_syspath()
