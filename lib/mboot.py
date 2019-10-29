# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
"""
Universal MicroPython bootloader.
"""

class McuFamily:
    """ """

    STM32 = 1
    ESP32 = 2


class MicroPythonPlatform:
    """ """

    Vanilla = 1
    Pycom = 2


class PlatformInfo:
    """ """

    def __init__(self):

        self.mcu = None
        self.vendor = None
        self.micropython_version = None

        self.resolve_platform()

    def resolve_platform(self):
        """ """

        import sys

        self.micropython_version = sys.implementation.version

        if sys.platform == 'esp32':
            self.mcu = McuFamily.ESP32
            self.vendor = MicroPythonPlatform.Vanilla

        if sys.platform in ['WiPy', 'LoPy', 'LoPy4', 'GPy', 'FiPy']:
            self.mcu = McuFamily.ESP32
            self.vendor = MicroPythonPlatform.Pycom

        if sys.platform in ['pyboard']:
            self.mcu = McuFamily.STM32
            self.vendor = MicroPythonPlatform.Vanilla


class MicroPythonBootloader:
    """ """

    def __init__(self):
        self.platform_info = PlatformInfo()

    def extend_syspath(self):
        """Extend Python module search path.
        Dependency modules are shipped through the "dist-packages" folder.
        Please populate this folder appropriately as shown above before
        expecting anything to work.


        """
        import sys

        # Vanilla Pycom MicroPython: ['', '/flash', '/flash/lib']
        # Vanilla MicroPython: ['', '/lib']

        # Extend by path containing frozen modules.
        if self.platform_info.vendor == MicroPythonPlatform.Pycom:
            if sys.implementation[1] == (1, 11, 0):
                bytecode_path = 'lib-mpy-1.11-pycom'
            else:
                bytecode_path = 'lib-mpy-1.9.4-pycom'
        else:
            bytecode_path = 'lib-mpy-1.11-bytecode'

        # Extend by all paths required for running the sandboxed firmware.
        if '/flash' in sys.path:
            sys.path[0:0] = ['/flash/{}'.format(bytecode_path)]
            sys.path.extend(['/flash/dist-packages', '/flash/terkin', '/flash/hiveeyes'])
        else:
            sys.path[0:0] = ['/{}'.format(bytecode_path)]
            sys.path.extend(['/dist-packages', '/terkin', '/hiveeyes'])

        """
        # Experiments.
        sys.path[0:0] = ['/flash/terkin', '/flash/hiveeyes']
        #sys.path[0:0] = ['/flash/lib-mpy']
        sys.path.extend(['dist-packages2'])
        #sys.path.extend(['dist-packages2', 'terkin', 'hiveeyes'])
        #sys.path.extend(['dist-packages', 'terkin', 'hiveeyes'])
        #sys.path.extend(['terkin', 'hiveeyes'])
        """

        print('[mboot]   INFO: Python module search path is:', sys.path)
