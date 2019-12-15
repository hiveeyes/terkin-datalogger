# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
"""
Universal MicroPython Application Loader.
"""


class McuFamily:
    """
    Constants for designating different MCU families.
    """

    # STMicroelectronics
    # STM32 32-bit Arm Cortex MCUs.
    # https://en.wikipedia.org/wiki/STM32
    # https://www.st.com/en/microcontrollers-microprocessors/stm32-32-bit-arm-cortex-mcus.html
    STM32 = 1

    # Espressif
    # System on a chip microcontrollers with integrated Wi-Fi and dual-mode Bluetooth.
    # https://en.wikipedia.org/wiki/ESP32
    # https://www.espressif.com/en/products/hardware/esp32/overview
    ESP32 = 2


class MicroPythonVendor:
    """
    Constants for designating different vendors of the MicroPython platform.
    """

    # Vanilla/Genuine MicroPython.
    # https://github.com/micropython/micropython
    Vanilla = 1

    # Pycom MicroPython.
    # https://github.com/pycom/pycom-micropython-sigfox
    Pycom = 2


class PlatformInfo:
    """
    Platform info object bundling the combination of MCU family
    and MicroPython vendor to assist in platform switching
    mechanics throughout the program.
    """

    MCU = McuFamily
    MICROPYTHON = MicroPythonVendor

    def __init__(self):

        self.mcu = None
        self.vendor = None
        self.micropython_version = None
        self.device_name = None

        self.resolve_platform()

    def resolve_platform(self):
        """ """

        import sys

        self.micropython_version = sys.implementation.version

        if sys.platform == 'esp32':
            self.mcu = McuFamily.ESP32
            self.vendor = MicroPythonVendor.Vanilla

        if sys.platform in ['WiPy', 'LoPy', 'LoPy4', 'GPy', 'FiPy']:
            self.mcu = McuFamily.ESP32
            self.vendor = MicroPythonVendor.Pycom

        if sys.platform in ['pyboard']:
            self.mcu = McuFamily.STM32
            self.vendor = MicroPythonVendor.Vanilla

        self.device_name = sys.platform


class ApplicationInfo:
    """ """

    def __init__(self, name=None, version=None, settings=None, application=None, platform_info: PlatformInfo = None):
        self.name = name
        self.version = version

        self.platform_info = platform_info

        self.settings = settings
        self.application = application

    @property
    def fullname(self):
        """ """
        return '{} {}'.format(self.name, self.version)


class MicroPythonBootloader:
    """ """

    def __init__(self):
        self.platform_info = PlatformInfo()
        self.duty_chrono = GenericChronometer()

    def extend_syspath(self):
        """
        Extend Python module search path.

        Dependency modules are shipped through the "dist-packages" folder.
        Please populate this folder appropriately as shown above before
        expecting anything to work.

        The ``PYTHONPATH`` as found on the different platforms is:
        - Vanilla MicroPython: ['', '/lib']
        - Pycom MicroPython: ['', '/flash', '/flash/lib']
        """
        import sys

        # Extend by path containing frozen modules.
        if self.platform_info.vendor == self.platform_info.MICROPYTHON.Pycom:
            if self.platform_info.micropython_version >= (1, 11):
                bytecode_path = 'lib-mpy-1.11-pycom'
            else:
                bytecode_path = 'lib-mpy-1.9.4-pycom'
        else:
            bytecode_path = 'lib-mpy-1.11-bytecode'

        # Extend by all paths required for running the sandboxed firmware.
        if '/flash' in sys.path:
            sys.path[0:0] = ['/flash/{}'.format(bytecode_path)]
            sys.path.extend(['/flash/dist-packages', '/flash/terkin'])
        else:
            sys.path[0:0] = ['/{}'.format(bytecode_path)]
            sys.path.extend(['/dist-packages', '/terkin'])

        print('[umal]    INFO: Python module search path is:', sys.path)


class GenericChronometer:
    """
    A millisecond chronometer implemented with vanilla MicroPython.
    https://micropython.readthedocs.io/en/latest/pyboard/tutorial/timer.html#making-a-microsecond-counter
    """

    def __init__(self):
        import time
        self.start = time.ticks_ms()

    def read(self):
        """ """
        import time
        return time.ticks_diff(time.ticks_ms(), self.start) / 1000.0

    def reset(self):
        """ """
        import time
        self.start = time.ticks_ms()
