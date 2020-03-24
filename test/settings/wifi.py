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
    'wifi': {

        # Enable/disable WiFi completely.
        'enabled': True,

        # WiFi interface configuration.
        'phy': {
            'antenna_external': False,
            'antenna_pin': 'P12',
        },

        # WiFi stations to connect to in STA mode.
        'stations': [
            {'ssid': 'FooBarWiFi', 'password': 'secret', 'timeout': 15.0},
        ],
    },
}
