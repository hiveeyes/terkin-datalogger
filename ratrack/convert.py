import array

mandatory_fields = [
    'latitude', 'longitude', 'roll', 'pitch', 'speed', 'cog',
    'temperature', 'pressure', 'humidity', 'battery_voltage',
]


def create_payload(data):
    #print('DATA:', data)

    # Sanity checks
    for field in mandatory_fields:
        if field not in data or data[field] is None:
            raise KeyError('Mandatory field "{}" required'.format(field))

    lat, lon = convert_latlon(data.get('latitude'), data.get('longitude'))
    roll, pitch, bat = convert_pytrack_sensors(data.get('roll'), data.get('pitch'), data.get('battery_voltage'))
    speedkmh, cog = convert_speed(data.get('speed'),data.get('cog'))
    temp, pressure, humidity = convert_bme280(data.get('temperature'), data.get('pressure'), data.get('humidity'))

    # payload = array.array('B', [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    payload = array.array('B', [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    payload[0] = lat
    payload[1] = (lat >> 8)
    payload[2] = (lat >> 16)

    payload[3] = lon
    payload[4] = (lon >> 8)
    payload[5] = (lon >> 16)

    payload[6] = roll
    payload[7] = (roll >> 8)
    payload[8] = (roll >> 16)

    payload[9] = pitch
    payload[10] = (pitch >> 8)
    payload[11] = (pitch >> 16)

    payload[12] = bat
    payload[13] = (bat >> 8)
    payload[14] = (bat >> 16)

    payload[15] = cog
    payload[16] = (cog >> 8)
    payload[17] = (cog >> 16)

    payload[18] = speedkmh
    payload[19] = (speedkmh >> 8)
    payload[20] = (speedkmh >> 16)

    payload[21] = temp
    payload[22] = (temp >> 8)
    payload[23] = (temp >> 16)

    payload[24] = pressure
    payload[25] = (pressure >> 8)
    payload[26] = (pressure >> 16)

    return payload


def convert_pytrack_sensors(r, p, b):
    r = int((r + 360) * 10000)
    p = int((p + 360) * 10000)
    b = int(b * 10000)
    return r, p, b


def convert_speed(s, c):
    s = int((float(s) + 999) * 1000)
    c = int((float(c) + 999) * 1000)
    return s, c


def convert_bme280(t, p, h):
    t = int((float(t) + 999) * 1000)
    p = int((float(p) + 999) * 1000)
    h = int((float(h) + 999) * 1000)
    return t, p, h


def convert_latlon(lat, lon):
    lat = int((float(lat) + 90)*10000)
    lon = int((float(lon) + 180)*10000)
    # alt = int((altitude) * 10)
    # hdop = int((hdop) * 10)
    return lat, lon
