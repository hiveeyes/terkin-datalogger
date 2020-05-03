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
import os
import sys
import click
import logging


# Configure CPython logger.
log_format = '%(asctime)-15s [%(name)-30s] %(levelname)-7s: %(message)s'
logging.basicConfig(
    format=log_format,
    stream=sys.stderr,
    level=logging.INFO)

log = logging.getLogger()

# Reconfigure module search path.
base = os.path.abspath('.')
sys.path = [os.path.join(base, 'dist-packages'), os.path.join(base, 'src')] + sys.path

# Make environment compatible with CPython.
log.info('Setting up CPython compatibility layer')
import cpython_compat
cpython_compat.monkeypatch()

# Fix: RuntimeError: Click will abort further execution because Python 3
#      was configured to use ASCII as encoding for the environment.
os.environ['LANG'] = 'en_US.UTF-8'


log.info('Loading settings')
import settings

# Global references to Bootloader and Datalogger objects.
bootloader = None
datalogger = None


@click.command()
@click.option("--daemon", is_flag=True, default=False, help="Run in daemon mode.")
def cli(daemon):
    """Start the data logger application."""

    global bootloader
    global datalogger

    log.info('Starting bootloader')
    bootloader = start_bootloader()

    log.info('Loading modules')
    from terkin.datalogger import TerkinDatalogger

    log.info('Setting up Terkin')
    datalogger = TerkinDatalogger(settings, platform_info=bootloader.platform_info)
    datalogger.setup()

    log.info('Starting Terkin')
    try:
        if daemon:
            datalogger.start()
        else:
            datalogger.duty_cycle()

    except KeyboardInterrupt:

        if datalogger.device.status.networking:
            datalogger.device.networking.stop_modeserver()
            datalogger.device.networking.wifi_manager.stop()

            # This helps the webserver to get rid of any listening sockets.
            # https://github.com/jczic/MicroWebSrv2/issues/8
            datalogger.device.networking.stop_httpserver()


def start_bootloader():
    """
    Invoke bootloader.
    """
    from umal import MicroPythonBootloader
    bootloader = MicroPythonBootloader()
    sys.modules['__main__'].bootloader = bootloader
    return bootloader
