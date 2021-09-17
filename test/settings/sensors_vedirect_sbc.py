"""Datalogger configuration"""

# Sensor configuration.
sensors = {
    'environment': [
        {
            'id': 'vedirect-sbc-1',
            'description': 'Victron Energy SmartSolar Charge Controller MPPT 75|15',
            'type': 'vedirect',
            'enabled': True,
            # 'bus': 'serial:0',
            'device': '/dev/ttysdummy042',
        },
    ],
}
