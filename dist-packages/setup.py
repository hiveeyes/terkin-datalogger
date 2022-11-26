# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(name='terkin-micropython-libraries',
      version='0.14.0',
      description='Terkin MicroPython runtime libraries',
      long_description='This package contains all MicroPython runtime libraries '
                       'required to run Terkin on CPython.',
      license="MIT, Apache 2.0",
      classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: MicroPython",
        "License :: OSI Approved :: Apache Software License",
        "License :: OSI Approved :: MIT License",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "Development Status :: 4 - Beta",
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

      # find_packages only finds packages in directories with __init__.py files.
      # py_modules lists top-level single file packages to include.
      packages=find_packages('.'),
      py_modules=[
          "umqtt",
          "urequests",
      ],

      include_package_data=True,
      package_data={
      },
      zip_safe=False,
      test_suite='test',
      install_requires=[],
      extras_require={},
      dependency_links=[
      ],
      entry_points={
      },
)
