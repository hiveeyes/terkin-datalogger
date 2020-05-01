# -*- coding: utf-8 -*-
# (c) 2019 Jan Hoffmann <jan.hoffmann@bergamsee.de>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
from terkin import logging
from terkin.model import SensorReading
from terkin.sensor import SensorManager, AbstractSensor

log = logging.getLogger(__name__)


def includeme(sensor_manager: SensorManager, sensor_info):
    """
    Create BME280 sensor object.

    :param sensor_manager:
    :param sensor_info:

    :return: sensor_object
    """
    sensor_object = PytrackSensor(settings=sensor_info)
    sensor_bus = sensor_manager.get_bus_by_name(sensor_info.get('bus'))
    sensor_object.acquire_bus(sensor_bus)

    return sensor_object


class PytrackSensor(AbstractSensor):
    """A Pytrack sensor component."""

    def __init__(self, settings=None):

        super().__init__(settings=settings)

        # The driver instance.
        self.readings = None
        self.bus = None

        self.sensor = None
        self.l76 = None
        self.lis2hh12 = None

    def start(self):
        """Getting the bus"""
        if self.bus is None:
            raise KeyError("I2C bus missing")

        # Initialize the hardware driver.
        try:
            from pytrack import Pytrack
            self.sensor = Pytrack(i2c=self.bus.adapter)
        except Exception as ex:
            log.exc(ex, 'Pytrack hardware driver failed')
            raise

        # Initialize the L76GNS sensor driver.
        try:
            from L76GNSV4 import L76GNSS
            self.l76 = L76GNSS(pytrack=self.sensor, timeout=5)
        except Exception as ex:
            log.exc(ex, 'Pytrack L76GNSS hardware driver failed')
            raise

        # Initialize the LIS2HH12 sensor driver.
        try:
            from LIS2HH12 import LIS2HH12
            self.lis2hh12 = LIS2HH12(pysense=self.sensor)
        except Exception as ex:
            log.exc(ex, 'Pytrack LIS2HH12 hardware driver failed')
            raise

    def read(self):
        """ """
        data = {'battery_voltage': float(self.sensor.read_battery_voltage())}
        # log.info('Acquire reading from Pytrack')

        # TODO: Add more data here.
        l76_data = self.read_l76gns()
        data.update(l76_data)
        lis2hh12_data = self.read_lis2hh12()
        data.update(lis2hh12_data)

        log.info("Pytrack data: {}".format(data))

        reading = SensorReading()
        reading.sensor = self
        reading.data = data

        return reading

    def read_lis2hh12(self):
        """ """

        data = {}

        try:
            data['roll'] = float(self.lis2hh12.roll())
            data['pitch'] = float(self.lis2hh12.pitch())
        except Exception as ex:
            log.exc(ex, 'No Roll/Pitch Data:')

        try:
            # Returns (self.x[0] * _mult, self.y[0] * _mult, self.z[0] * _mult)
            acceleration = self.lis2hh12.acceleration()
            data['acceleration_x'] = float(acceleration[0])
            data['acceleration_y'] = float(acceleration[1])
            data['acceleration_z'] = float(acceleration[2])
        except Exception as ex:
            log.exc(ex, 'No Acceleration Data')

        # TODO: Enable enable_activity_interrupt
        # try:
        #    data['activity'] = self.lis2hh12.activity()
        # except Exception as ex:
        #    log.exc(ex, 'No Acitivity Data')

        # TODO: Enable enable_activity_interrupt
        # try:
        #    self.lis2hh12.enable_activity_interrupt(self.settings['threshold'], self.settings['duration'])
        # except Exception as e:
        #    log.info('No enable_activity_interrupt Data:', e)

        return data

    def read_l76gns(self):
        """ """

        data = {}

        # returns the info about sattelites in view at this moment
        # even without the gps being fixed
        #try:
            #print(self.l76.gps_message('GSV', debug=False))
            # {'Elevation2': '', 'Elevation3': '', 'SNR2': '', 'SNR3': '', 'Elevation1': '10', 'SNR1': '',
            # 'Elevation4': '', 'Azimuth3': '', 'Azimuth2': '', 'Azimuth1': '086', 'SatelliteID3': '',
            # 'SatelliteID2': '', 'SatelliteID1': '82', 'SatellitesInView': '09', 'NofMessage': '3', 'Azimuth4': '',
            # 'SequenceNr': '3', 'NMEA': 'GLGSV', 'SatelliteID4': '', 'SNR4': ''}
        #except Exception as ex:
        #    log.exc(ex, 'No gps_messages')

        try:
            data['satellites_count'] = self.l76.gps_message('GGA', debug=False)['NumberOfSV']
        except Exception as ex:
            log.exc(ex, "No satellites Data")

        # Call this to start the machinery and actually get a fix.
        try:
            self.l76.get_fix()
        except Exception as ex:
            log.exc(ex, "No Fix Data")
        # Only read values when having a fix.
        if not self.l76.fixed():
            return data

        try:
            self.l76.coordinates()
        except Exception as ex:
            log.exc(ex, "No coordinates")
            # log.exc(ex, "Could not read coordinates")
            # raise

        # Read speed and orientation.
        try:
            speed = self.l76.get_speed()
            data['speed'] = float(speed.get('speed'))
            data['cog'] = float(speed.get('COG'))
        except Exception as ex:
            log.exc(ex, "Could not read Speed. Error")

        # Read position.
        try:
            # location = self.l76.get_location(MSL=True)
            location = self.l76.get_location()
            try:
                data['longitude'] = float(location.get('longitude'))
                data['latitude'] = float(location.get('latitude'))
                data['altitude'] = float(location.get('altitude'))
            except Exception as ex:
                log.exc(ex, 'No GPS Data')
        except Exception as ex:
            log.exc(ex, "Could not read location from L76 GNSS")

        try:
            utctime = self.l76.getUTCTime()
            if utctime:
                data['UTCTime'] = utctime
            utcdatetime = self.l76.getUTCDateTime()
            if utcdatetime:
                data['UTCDateTime'] = utcdatetime
            # TODO Needed?
            utcdatetimetuple = self.l76.getUTCDateTimeTuple()
            # if utcdatetimetuple:
            #    data['UTCDateTimeTuple'] = utcdatetimetuple
            log.info('DateTimeTuple: ' + str(utcdatetimetuple))
        except Exception as ex:
            log.exc(ex, 'No Time Data')

        # TODO: Sort into Sensor Metadata?
        #try:
            #data['chip_version'] = str(self.l76.get_chip_version())
            # {'ChipVersionID': 'L76LNR01A03S', 'time': '17:40', 'date': '2016/05/16',
            # 'command': 'R', 'PMTK': 'PERNO'}
            #data['dt_release'] = str(self.l76.get_dt_release())
            # {'ProductModel': 'Quectel-L76', 'ReleaseString''AXN_3.8_3333_16042918',
            # 'PMTK': 'PMTK705', 'BuildID': '0006', 'SDK': '1.0'}
        #except Exception as ex:
        #    log.exc(ex, 'No Chip Data')

        return data
