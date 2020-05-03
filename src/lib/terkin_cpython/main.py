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
import click
import logging
from terkin_cpython.util import setup_logging, configure_pythonpath, patch_system, start_bootloader, load_settings

# Configure logging.
setup_logging()
log = logging.getLogger()


@click.command()
@click.option("--config", required=True, help="Path to settings file.")
@click.option("--site-packages", help="Path to additional Python modules.")
@click.option("--daemon", is_flag=True, default=False, help="Run in daemon mode.")
@click.option("--ui", is_flag=True, default=False, help="Start user interface.")
def cli(**options):

    # Reconfigure module search path.
    if 'site_packages' in options and options['site_packages']:
        search_path = options['site_packages']
    else:
        search_path = os.path.abspath(os.path.join('.', 'dist-packages'))
    configure_pythonpath(search_path)

    # Bootstrap datalogger application.
    app = TerkinApplication(config=options['config'], daemon=options['daemon'])
    if options['ui']:
        app.start_ui()
    else:
        app.start()


class TerkinApplication:
    """Start the data logger application."""

    def __init__(self, config=None, daemon=False):
        self.config = config
        self.daemon = daemon
        self.bootloader = None
        self.datalogger = None

    def start(self):

        # Make environment compatible with CPython.
        patch_system()

        log.info('Starting bootloader')
        self.bootloader = start_bootloader()

        log.info('Loading modules')
        from terkin.datalogger import TerkinDatalogger

        settings = load_settings(settings_file=self.config)

        log.info('Setting up Terkin')
        self.datalogger = TerkinDatalogger(settings, platform_info=self.bootloader.platform_info)
        self.datalogger.setup()

        log.info('Starting Terkin')
        try:
            if self.daemon:
                self.datalogger.start()
            else:
                self.datalogger.duty_cycle()

        except KeyboardInterrupt:
            self.shutdown()

    def shutdown(self):

        log.info('Shutting down Terkin')

        if self.datalogger.device.status.networking:
            self.datalogger.device.networking.stop()

    def start_ui(self):

        # Make environment compatible with CPython.
        patch_system()

        from terkin.ui import TerkinUi

        ui = TerkinUi()
        try:
            ui.start()
            ui.example_listbox()
            #ui.example_menu()

        finally:
            ui.stop()
