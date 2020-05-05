from terkin import logging
from terkin.model import DataFrame

log = logging.getLogger(__name__)


def to_cayenne_lpp_hiveeyes(dataframe: DataFrame):
    """
    Serialize dataframe to binary CayenneLPP format.

    :param dataframe:
    """

    from cayennelpp import LppFrame
    frame = LppFrame()

    channel = {}
    channel['temp']   = 10
    channel['volt']   = 2
    channel['pres']   = 1
    channel['scal']   = 6

    # TODO: Iterate ``dataframe.readings`` to get more metadata from sensor configuration.
    # It is a list of ``SensorReading`` instances, each having a ``sensor`` and ``data`` attribute.

    # log.info('dataframe.data_out.items : %s', dataframe.data_out.items())

    for key, value in dataframe.data_out.items():

        #log.debug('-' * 42)

        # TODO: Maybe implement different naming conventions.
        name = key.split("_")[0]
        #     channel = 0

        if "system" in name:
            if "voltage" in name:
                # treat voltage as system sensors
                # put battery voltage to channel 0
                # put solar voltage to channel 1
                # put other voltages to channel 2++
                if "battery" in name:
                    chan = 0
                elif "solar" in name:
                    chan = 1
                else:
                    chan = channel['volt']
                    channel['volt'] += 1
                frame.add_voltage(chan, value)
            elif "temperature" in name:
                frame.add_temperature(0, value)
        elif "i2c" in name:
            # assume BME280 on I2C bus as outside sensor and assign the variables to channel 5
            if "temperature" in name:
                frame.add_temperature(5, value)
            elif "humidity" in name:
                frame.add_humidity(5, value)
            elif "pressure" in name:
                frame.add_barometer(5, value)
        elif "weight" in name:
            # treat weight as outside sensor and assign to channel 5-9
            # Channel 5 for single reading (weight.0))
            # Channel 6-9 for multiple readings (weight.[1-4])
            if name == "weight.0":
                chan = 5
            else:
                chan = channel['scal']
                channel['scal'] += 1
            frame.add_load(chan, value)
        elif "onewire" in name:
            # assume DS18B20 as inside sensors and assign to channel 10++
            if "temperature" in name:
                frame.add_temperature(channel['temp'], value)
                channel['temp'] += 1
        elif "analog-output" in name:
            frame.add_analog_output(channel, value)
        elif "analog-input" in name:
            frame.add_analog_input(channel, value)
        elif "digital-input" in name:
            frame.add_digital_input(channel, value)
        elif "digital_output" in name:
            frame.add_digital_output(channel, value)
        elif "illuminance" in name:
            frame.add_luminosity(channel, value)
        elif "barometer" in name:
            frame.add_barometer(channel, value)
        elif "presence" in name:
            frame.add_presence(channel, value)
        elif "accelerometer" in name:
            frame.add_accelerometer(channel, value)
        elif "gyrometer" in name:
            frame.add_gyrometer(channel, value)
        #elif "gps" in name:
        #    frame.add_gps(channel, value)


        # TODO: Fork cayenneLPP and implement load cell telemetry.
        # TODO: Add load encoder as ID 122 (3322)
        # http://openmobilealliance.org/wp/OMNA/LwM2M/LwM2MRegistry.html#extlabel
        # http://www.openmobilealliance.org/tech/profiles/lwm2m/3322.xml

        # elif False and "load" in name:
        #     frame.add_load(channel, value)

        # TODO: Map memfree and other baseline sensors appropriately.

        else:
            # TODO: raise Exception here?
            log.info('[CayenneLPP] Sensor type "{}" not found in CayenneLPP'.format(name))

    return frame.bytes()


def to_cayenne_lpp_ratrack(dataframe: DataFrame):
    """
    Serialize dataframe to binary CayenneLPP format.

    :param dataframe:
    """

    from cayennelpp import LppFrame
    frame = LppFrame()

    channel = {}
    channel['temp']   = 10

    if ('alt' or 'altitude') and ('lat' or 'longitude') and ('lon' or 'longitude') in dataframe.data_out.keys():
        log.info('GOT GPS!')
        frame.add_gps(0, dataframe.data_out.get('lat'), dataframe.data_out.get('lon'), dataframe.data_out.get('alt'))

    if 'batterie_volt' in dataframe.data_out.keys():
        frame.add_analog_input(14, dataframe.data_out.get('batterie_volt'))

    for key, value in dataframe.data_out.items():

        name = key

        if "system" in name:
            pass
        elif "i2c" in name:
            # assume BME280 on I2C bus as outside sensor and assign the variables to channel 5
            if "temperature" in name:
                frame.add_temperature(5, value)
            elif "humidity" in name:
                frame.add_humidity(5, value)
            elif "pressure" in name:
                frame.add_barometer(5, value)
        elif "onewire" in name:
            # assume DS18B20 as inside sensors and assign to channel 10++
            if "temperature" in name:
                frame.add_temperature(channel['temp'], value)
                channel['temp'] += 1
        else:
            # TODO: raise Exception here?
            #log.info('[CayenneLPP] Sensor type "{}" not found in CayenneLPP'.format(name))
            hu1 = 2

    return frame.bytes()
