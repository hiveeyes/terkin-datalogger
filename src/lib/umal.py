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

    # RaspberryPi.
    RaspberryPi = 3

    # Odroid.
    Odroid = 4


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
        """ 
        Resolve MCU and vendor of this platform.
        """

        import sys

        self.micropython_version = sys.implementation.version

        if sys.platform == 'esp32':
            self.mcu = McuFamily.ESP32
            self.vendor = MicroPythonVendor.Vanilla

        if sys.platform in ['WiPy', 'LoPy', 'LoPy4', 'SiPy', 'GPy', 'FiPy']:
            self.mcu = McuFamily.ESP32
            self.vendor = MicroPythonVendor.Pycom

        if sys.platform in ['pyboard']:
            self.mcu = McuFamily.STM32
            self.vendor = MicroPythonVendor.Vanilla

        try:
            linux_firmware = open('/sys/firmware/devicetree/base/model').read()
            if 'Raspberry' in linux_firmware:
                self.mcu = McuFamily.STM32
                self.vendor = MicroPythonVendor.RaspberryPi
            elif 'Odroid' in linux_firmware:
                self.mcu = McuFamily.STM32
                self.vendor = MicroPythonVendor.Odroid
        except:
            pass

        self.device_name = sys.platform


class ApplicationInfo:
    """ 
    Collects various information. Most importantly transports the settings for further use in the Datalogger.
    """

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
    """ 
    Very basic tasks for running the system.
    """

    def __init__(self):
        self.platform_info = PlatformInfo()
        self.duty_chrono = GenericChronometer()

    def extend_syspath(self):
        """
        Extend Python module search path.

        Dependency modules are shipped through the "dist-packages" folder.
        Please populate this folder appropriately as shown above before
        expecting anything to work.

        The default ``PYTHONPATH`` as found on the different platforms is:
        - Vanilla MicroPython: ['', '/lib']
        - Pycom MicroPython: ['', '/flash', '/flash/lib']
        """
        import sys

        # Extend by path containing frozen modules.
        paths = ['lib', 'dist-packages', 'lib-mpy']
        if self.platform_info.vendor == self.platform_info.MICROPYTHON.Pycom:
            paths = ['/flash/{}'.format(path) for path in paths]

        elif self.platform_info.vendor == self.platform_info.MICROPYTHON.Vanilla:
            paths = ['/{}'.format(path) for path in paths]

        elif self.platform_info.vendor == self.platform_info.MICROPYTHON.RaspberryPi:
            paths = ['./dist-packages', './src/lib']

        else:
            print('[umal]    ERROR: MicroPython platform not supported:', self.platform_info.vendor)
            sys.exit(1)

        # Amend module search path.
        sys.path.clear()
        sys.path.extend(paths)

        # According to @poesel, empty directory designates frozen modules.
        # We want to put these at the end in order to be able to override
        # any module we would like to hack upon.
        sys.path.extend([''])

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
