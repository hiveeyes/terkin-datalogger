# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
"""
Universal MicroPython bootloader.
"""


class McuFamily:

    STM32 = 1
    ESP32 = 2


class MicroPythonPlatform:

    Vanilla = 1
    Pycom = 2


class PlatformInfo:

    def __init__(self):

        self.mcu = None
        self.vendor = None
        self.micropython_version = None

        self.resolve_platform()

    def resolve_platform(self):

        import sys

        self.micropython_version = sys.implementation.version

        if sys.platform == 'esp32':
            self.mcu = McuFamily.ESP32
            self.vendor = MicroPythonPlatform.Vanilla

        if sys.platform in ['WiPy', 'LoPy', 'GPy', 'FiPy']:
            self.mcu = McuFamily.ESP32
            self.vendor = MicroPythonPlatform.Pycom


class MicroPythonBootloader:

    def __init__(self):
        self.platform_info = PlatformInfo()

    @staticmethod
    def extend_syspath():
        """
        Extend Python module search path.
        Dependency modules are shipped through the "dist-packages" folder.
        Please populate this folder appropriately as shown above before
        expecting anything to work.
        """
        import sys

        # Vanilla Pycom MicroPython: ['', '/flash', '/flash/lib']

        # Extend by path containing frozen modules.
        sys.path[0:0] = ['/flash/lib-mpy']

        # Extend by all paths required for running the sandboxed firmware.
        sys.path.extend(['/flash/dist-packages', '/flash/terkin', '/flash/hiveeyes'])

        """
        # Experiments.
        sys.path[0:0] = ['/flash/terkin', '/flash/hiveeyes']
        #sys.path[0:0] = ['/flash/lib-mpy']
        sys.path.extend(['dist-packages2'])
        #sys.path.extend(['dist-packages2', 'terkin', 'hiveeyes'])
        #sys.path.extend(['dist-packages', 'terkin', 'hiveeyes'])
        #sys.path.extend(['terkin', 'hiveeyes'])
        """

        print('[mboot] INFO: Python module search path is:', sys.path)
