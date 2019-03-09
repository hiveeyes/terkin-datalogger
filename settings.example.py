"""Datalogger configuration"""

# General settings.
main = {
    # Measurement interval.
    'interval': 1.0,
}

# Networking configuration.
networking = {
    'wifi': {
        # WiFi stations to connect to in STA mode.
        'stations': [

            # Variant 1: Using DHCP.
            {'ssid': 'FooBar', 'password': 'SECRET'},

            # Variant 2: Using static IP address.
            {
                'ssid': 'FooBar',
                'password': 'SECRET',
                # Use static network configuration (ip, subnet_mask, gateway, DNS_server).
                'ifconfig': ('192.168.42.42', '255.255.255.0', '192.168.42.1', '192.168.42.1'),
            },
        ],

        # The maximum time in milliseconds to wait for the connection to succeed.
        'timeout': 15000,
    },
    'LoRa': {
        'OTAA': [
            {'frequency': 868100000},
            {'region': 'LoRa.EU868'},
            {'datarate': 5},
            {'device_eui':'<GENERATED_FROM_LORA_MAC>'},
            {'application_eui': '<REGISTRATION NEEDED>'},
            {'application_key': '<REGISTRATION NEEDED>'}
        ],
        'antenna_attached': False,
    }
}

# Telemetry configuration.
telemetry = {
    'targets': [
        {
            #'endpoint': 'https://daq.example.org/api',
            #'endpoint': 'http://daq.example.org/api-notls',
            'endpoint': 'mqtt://daq.example.org',
            'address': {
                "realm": "acme",
                "network": "testdrive",
                "gateway": "area-42",
                "node": "node-1",
            }
        }
    ],
}
