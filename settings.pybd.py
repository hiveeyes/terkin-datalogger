"""Datalogger configuration"""

# General settings.
main = {

    # Measurement intervals in seconds.
    'interval': {

        # Apply this interval if device is in field mode.
        'field': 15.0,

        # Apply this interval if device is in maintenance mode.
        # https://community.hiveeyes.org/t/wartungsmodus-fur-den-terkin-datenlogger/2274
        'maintenance': 15.0,
    },

    # Whether to use light sleep between measurement cycles.
    'lightsleep': False,

    # Whether to use deep sleep between measurement cycles.
    'deepsleep': False,

    # Configure logging.
    'logging': {

        # Enable or disable logging completely.
        'enabled': True,

        # Log configuration settings at system startup.
        'configuration': True,

    },

    # Configure Watchdog.
    'watchdog': {

        # Enable or disable Watchdog completely.
        'enabled': False,

        # Watchdog timeout in milliseconds.
        'timeout': 60000,
    },

    # Configure backup.
    'backup': {
        # How many backup files to keep around.
        'file_count': 7,
    },

    # Whether to skip LTE modem deinit on startup. This will save ~6 seconds.
    'fastboot': True,

    # Configure RGB-LED.
    'rgb_led': {

        # Use the builtin heartbeat blink pattern. Default: True.
        'heartbeat': False,

        # Activate the Terkin blink pattern. Will disable the builtin heartbeat pattern when enabled.
        'terkin': True,
    },

}

# Control the services offered by the device.
services = {
    'api': {
        'modeserver': {
            'enabled': False,
        },
        'http': {
            'enabled': False,
        },
    },
}

# Interface settings.
interfaces = {
    'uart0': {
        'terminal': True,
    }
}

# Networking configuration.
networking = {
    'wifi': {

        # WiFi interface configuration.
        'phy': {
            'antenna_external': False,
            'antenna_pin': 'P12',
        },

        # WiFi stations to connect to in STA mode.
        'stations': [
            #{'ssid': 'hiveeyes_5g', 'password': 'hiveeyes'},
            #{'ssid': 'hiveeyes_24g', 'password': 'hiveeyes'},
            #{'ssid': 'GartenNetzwerk', 'password': 'geheimespasswort', 'dhcp_hostname': 'hotzenplotz'},
            #{'ssid': 'GartenNetzwerk2', 'password': 'geheimespasswort', 'timeout': 10.0},
            #{'ssid': 'K2', 'password': 'geheimespasswort', 'timeout': 15.0},
            {'ssid': 'GartenNetzwerk', 'password': 'geheimespasswort', 'timeout': 15.0},
            #{
            #    'ssid': 'GartenNetzwerk',
            #    'password': 'geheimespasswort',
            #    # Use static network configuration (ip, subnet_mask, gateway, DNS_server).
            #    'ifconfig': ('192.168.178.42', '255.255.255.0', '192.168.178.1', '192.168.178.1'),
            #},
            #{'ssid': 'GartenNetzwerk', 'password': 'geheimespasswort'},
            #{'ssid': 'BKA Ueberwachungswagen', 'password': 'geheimespasswort'},
        ],
    },

}

# Telemetry configuration.
telemetry = {
    'targets': [

        # JSON over MQTT: Kotori/MqttKit
        {
            # Enable/disable this telemetry target.
            'enabled': True,

            # Define telemetry endpoint and address information.
            #'endpoint': 'mqtt://test:12345@swarm.hiveeyes.org',
            'endpoint': 'mqtt://swarm.hiveeyes.org',
            'topology': 'mqttkit',
            'address': {
                "realm": "hiveeyes",
                "network": "testdrive",
                "gateway": "area-38",
                "node": "pybd-sf2",
            },

            # Whether to prettify telemetry payload on log output.
            #'prettify_log': True,

        },

    ],
}

# Sensor configuration.
sensors = {

    # Whether to prettify sensor log output.
    'prettify_log': False,

}
