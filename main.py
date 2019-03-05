# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
from application import Application
from radio import NetworkManager


# Application metadata.
NAME = 'Hiveeyes MPY data logger'
VERSION = '0.0.0'

# Main application object.
app = Application(NAME, VERSION)

# Disable this if you don't want serial access.
app.enable_serial()

# Hello world.
app.print_bootscreen()

# Read configuration.
# TODO: Encapsulate into configuration file.
from config import *
from config_local import *


def start_networking():
    app.tlog('Starting networking')

    nm = NetworkManager(known_wifi_APs)

    # Start WiFi
    nm.start_wifi()

    # Wait for network interface to come up.
    nm.wait_for_nic()

    # Inform about networking status.
    nm.print_status()


def start_telemetry():
    app.tlog('Starting telemetry')

    # Create a "Node API" telemetry client object
    from telemetry import TelemetryNode, TelemetryTopologies
    telemetry = TelemetryNode(
        #"https://swarm.hiveeyes.org/api",
        #"http://swarm.hiveeyes.org/api-notls",
        "mqtt://swarm.hiveeyes.org",
        address={
            "realm":    "hiveeyes",
            "network":  "testdrive",
            "gateway":  "area-23",
            "node":     "node-1",
        },
        topology=TelemetryTopologies.KotoriWanTopology
    )

    # Setup telemetry object
    telemetry.setup()

    return telemetry


def start_sensors(telemetry):

    app.tlog('Starting sensors')

    # Fake measurement.
    data = {"temperature": 42.84, "humidity": 83}

    """
    TODO: Add more sensors.
    - Metadata from NetworkManager.station
    """

    # Transmit data
    success = telemetry.transmit(data)
    print('Telemetry success:', success)
    print()


if __name__ == '__main__':
    start_networking()
    telemetry = start_telemetry()
    start_sensors(telemetry)
