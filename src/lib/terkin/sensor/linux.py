import os
import time
import binascii

from terkin import logging

log = logging.getLogger(__name__)


class LinuxSysfsOneWireBus:
    """
    dtoverlay w1-gpio gpiopin=4 pullup=0

    cat /sys/bus/w1/devices/w1_bus_master1/w1_master_slaves
    28-0517c482cfff
    """
    def __init__(self, sysfs):
        self.sysfs = sysfs
        self.roms = []
        log.info('Starting LinuxSysfsOneWireBus on {}'.format(self.sysfs))

    def scan(self):
        with open(os.path.join(self.sysfs, 'w1_master_slaves'), 'r') as f:
            items = f.readlines()
            self.roms = []
            for item in items:
                # Decode 1-Wire device address on sysfs like "28-0517c482cfff".
                prefix, address = item.split('-')
                rom = bytes.fromhex(prefix) + bytes.fromhex(address)
                self.roms.append(rom)
            return self.roms


class LinuxSysfsDS18B20:
    """
    cat /sys/bus/w1/devices/w1_bus_master1/28-0517c482cfff/w1_slave
    36 01 4b 46 7f ff 0c 10 9a : crc=9a YES
    36 01 4b 46 7f ff 0c 10 9a t=19375
    """
    def __init__(self, bus):
        self.bus = bus

    def convert_temp(self):
        # Noop
        pass

    def read_temp(self, address):
        address = insert(binascii.hexlify(address).decode(), '-', 2)
        log.info('DS18B20 read_temp: %s', address)
        device_file = os.path.join(self.bus.sysfs, address, 'w1_slave')
        log.info('DS18B20 device_file: %s', device_file)
        temp_c, temp_f = self.read_temp_raw(device_file)
        return temp_c

    def read_temp_raw(self, device_file):
        # https://www.waveshare.com/wiki/Raspberry_Pi_Tutorial_Series:_1-Wire_DS18B20_Sensor

        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()

        # Analyze if the last 3 characters are 'YES'.
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw(device_file)
        # Find the index of 't=' in a string.
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            # Read the temperature .
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            return temp_c, temp_f


def insert(source_str, insert_str, pos):
    # https://stackoverflow.com/a/25978101
    return source_str[:pos] + insert_str + source_str[pos:]
