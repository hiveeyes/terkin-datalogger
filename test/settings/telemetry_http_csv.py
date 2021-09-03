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
}

# Telemetry configuration.
telemetry = {
    'targets': [

        # CSV over HTTP
        {
            # Enable/disable this telemetry target.
            'enabled': True,

            # Define telemetry endpoint and address information.
            'endpoint': 'http://127.0.0.1:8888/foobar',
            'format': 'csv',
        },

    ],
}

# Sensor configuration.
sensors = {

    # Whether to prettify sensor log output.
    'prettify_log': True,

    'system': [

        {
            # Sensor which reports free system memory.
            'type': 'system.memfree',
            'enabled': True,
        },
        {
            # Sensor which reports system temperature.
            'type': 'system.temperature',
            'enabled': True,
        },
        {
            # Sensor which reports system uptime metrics.
            'type': 'system.uptime',
            'enabled': True,
        },

    ],
}
