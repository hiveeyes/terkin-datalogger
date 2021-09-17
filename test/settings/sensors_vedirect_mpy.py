"""Datalogger configuration"""

# Sensor configuration.
sensors = {
    'environment': [
        {
            'id': 'vedirect-mpy-1',
            'description': 'Victron Energy SmartSolar Charge Controller MPPT 75|15',
            'type': 'vedirect',
            'enabled': True,
            # 'bus': 'serial:0',
            'device': '1',
            'port': '1',
        },
    ],
}
