# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst'), encoding="utf-8").read()

requires = [

    # 3rd-party libraries
    'terkin-micropython-libraries==0.10.0',

    # Runtime
    'mock==4.0.2',

    # Mocks some HAL modules not available on CPython.
    'esp32-machine-emulator==1.1.3',

    # Command line interface
    'click==7.1.2',

    # UART access.
    'pyserial==3.4',

    # GPSD client library.
    'gps==3.19',

    # Adafruit CircuitPython libraries.
    'Adafruit-Blinka==4.6.0',
    'adafruit-circuitpython-busdevice==4.3.1',
    'adafruit-circuitpython-bme280==2.4.1',
    'adafruit-circuitpython-ads1x15==2.2.1',
    'adafruit-circuitpython-si7021==3.2.1',
    'adafruit-circuitpython-bmp280==3.2.1',
    'adafruit-circuitpython-ina219==3.4.2',


    # Victron Energy VE.Direct text protocol driver.
    #'git+https://github.com/karioja/vedirect@f74c0f2',

]

extras = {
    'sbc': [

        # I2C SMBus HAL module.
        'smbus==1.1.post2',

        # SPI HAL module.
        'spidev==3.4',

        # RPI USV+ Raspberry Pi - USV+
        'rpi-piusv==0.1.0',

        # Raspberry Pi utilities.
        'gpiozero==1.5.1',
    ],
    'lorawan': [
        # Required for LoRaWAN.
        'pycrypto==2.6.1',
    ],
}

setup(name='terkin',
      version='0.10.0',
      description='A flexible data logger for MicroPython and CPython',
      long_description=README,
      license="AGPL 3, EUPL 1.2",
      classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: MicroPython",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Telecommunications Industry",
        "Topic :: Communications",
        "Topic :: Internet",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
        "Topic :: Software Development :: Embedded Systems",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Archiving",
        "Topic :: System :: Networking :: Monitoring",
        "Topic :: Utilities",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS"
        ],
      author='Andreas Motl',
      author_email='andreas.motl@terkin.org',
      url='https://github.com/hiveeyes/terkin-datalogger',
      keywords='sensor networks data acquisition transformation daq routing '
               'telemetry m2m iot mqtt http',
      package_dir={
          '': 'src/lib',
      },
      packages=find_packages('src/lib'),
      py_modules=[
          'umal',
          'mininet',
      ],
      include_package_data=True,
      package_data={
      },
      zip_safe=False,
      test_suite='test',
      install_requires=requires,
      extras_require=extras,
      #tests_require=extras['test'],
      dependency_links=[
      ],
      entry_points={
          'console_scripts': [
              'terkin = terkin_cpython.main:cli',
          ],
      },
)
