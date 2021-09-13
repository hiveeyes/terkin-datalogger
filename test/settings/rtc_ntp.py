"""Datalogger configuration"""

# General settings.
main = {

    # Measurement intervals in seconds.
    'interval': {

        # Apply this interval if device is in field mode.
        'field': 0.0,

    },

    # Configure logging.
    'logging': {

        # Enable or disable logging completely.
        'enabled': True,

        # Log configuration settings at system startup.
        'configuration': False,

    },

}

# Networking configuration.
networking = {
    'ntp': {
        # Must have networking enabled. Unsure if functional over LoRaWAN/TTN
        'enabled': True,
        'server': 'pool.example.org'
    },
    'wifi': {
        # Enable/disable WiFi completely.
        'enabled': True,
        # WiFi stations to connect to in STA mode.
        'stations': [
            {'ssid': 'FooBarWiFi', 'password': 'secret', 'timeout': 15.0},
        ],
    },
}
