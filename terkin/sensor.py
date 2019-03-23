# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3


class SensorManager:
    def __init__(self):
        self.sensors = []
        pass

    def register_sensor(self, sensor):
        self.sensors.append(sensor)


    def get_sensor_by_name(self, name):
       pass


class AbstractSensor:
    """
    Abstract sensor container, containing meta data as readings
    """
    def __init__(self):
        self.name = None
        self.family = None
        self.driver = None

        """
        e.g. multiple onewire sensors are address indexed on a bus.
        """
        self.address = None
        self.bus = None
        self.pins = {}
        self.parameter = {}

    def start(self):
        raise NotImplementedError()
        pass

    def register_pin(self, name, pin):
        self.pins[name] = pin

        raise NotImplementedError()
        pass

    def register_parameter(self, name, parameter):
        self.parameter[name] = parameter

        raise NotImplementedError()
        pass


    def power_off(self):
        pass

    def power_on(self):
        pass


    def read(self):
        raise NotImplementedError()
        pass



class MemoryFree:

    def read(self):
        import gc
        return {'memfree': gc.mem_free()}

