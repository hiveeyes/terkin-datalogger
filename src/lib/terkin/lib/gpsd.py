from gps import *
import time


class Gpsd():

    def read(self):
        gpsd = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)
        counter = 0
        while True:
            report = gpsd.next()
            lat = 0
            lon = 0
            alt = 0
            if report['class'] == 'TPV':
                lat = getattr(report, 'lat', 0.0)
                lon = getattr(report, 'lon', 0.0)
                alt = getattr(report, 'alt', 'nan')
            time.sleep(0.3)
            counter = counter + 1
            if isinstance(lat, float) and isinstance(lon, float) and (isinstance(alt, int) or isinstance(alt, float)):
                data = {'latitude': float(lat), 'longitude': float(lon), 'altitude': float(alt)}
                return data
            if counter > 100:
                break
