# -*- coding: utf-8 -*-
#
# Terkin Datalogger
# https://github.com/hiveeyes/terkin-datalogger
#
# (c) 2019-2020 Andreas Motl <andreas@hiveeyes.org>
# (c) 2019-2020 Jan Hoffmann <jan.hoffmann@bergamsee.de>
# (c) 2019-2020 Richard Pobering <richard@hiveeyes.org>
#
# License: GNU General Public License, Version 3
#
"""
Please check https://community.hiveeyes.org/t/operate-the-terkin-datalogger-sandbox/2332
in order to get an idea about how to operate the sandbox of this software.

Have fun!
"""


# Global reference to Bootloader object.
bootloader = None


if __name__ == '__main__':

    import sys
    print('[boot.py] INFO: Python module search path is:', sys.path)

    # Extend module search path.
    print('[boot.py] INFO: Universal MicroPython Application Loader (umal)')
    from umal import MicroPythonBootloader
    bootloader = MicroPythonBootloader()
    bootloader.extend_syspath()
