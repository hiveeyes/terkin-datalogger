# -*- coding: utf-8 -*-
# (c) 2005,2020 Andreas Motl <andreas@hiveeyes.org>
# (c) 2005,2020 Jan Hoffmann <jan.hoffmann@bergamsee.de>
# License: GNU General Public License, Version 3
import re
import json
import serial
import struct


class EPSolar:

    def __init__(self, device):
        self.config = device
        self.serial_data = []
        self.serial_params = '''
            {
                "serial-port": "''' + str(device) + '''",
                "serial-params": {
                    "bytesize": 8,
                    "baudrate": 9600,
                    "timeout": 2.0,
                    "parity": "N"
                    }
            }
            '''

        self.config = json.loads(self.serial_params)
        self.config['ser'] = serial.Serial(str(self.config.get('serial-port')), **self.config.get('serial-params'))

    def read_serial(self):
        string = b'\xAA\x55\xEB\x90\xEB\x90\xEB\x90\x16\xA0\x00\xB1\xA7\x7F'
        self.config.get('ser').write(string)
        payload = self.config.get('ser').readline()
        # 1. decode payload
        try:
            data_length = payload[8]
            pos_data_start = 9
            pos_data_stop = pos_data_start + data_length

            data = payload[pos_data_start:pos_data_stop]

        except Exception as exc:
            # print traceback.format_exc()
            print(exc)
            # self.output(exc)
            serial_read = False
            return False, serial_read

        # 2. decode data
        # http://docs.python.org/2/library/struct.html#format-characters
        try:
            serial_data = list(struct.unpack('hhhhhh???c????bh', data))
            serial_read = True
            # 15 Battery temp., there is 30 difference in value with the real value (spec)
            serial_data[14] -= 35
            # 35 seems to be the right value
            self.serial_data = serial_data
            return serial_data, serial_read

        except Exception as exc:
            serial_read = False
            return False, serial_read

    def decode_serial(self, payload):
        if payload[1] < 100:
            payload[1] = 0
        if isinstance(payload[0], str):
            payload[0] = self.compile_value(payload[0], 'volt')
        if isinstance(payload[1], str):
            payload[1] = self.compile_value(payload[1], 'volt')
        if isinstance(payload[3], str):
            payload[3] = self.compile_value(payload[3], 'ampere')
        if isinstance(payload[6], str):
            payload[6] = self.compile_value(payload[6], 'ampere')
        if isinstance(payload[9], str):
            try:
                payload[9] = float(payload[9])
            except Exception as exc:
                payload[9] = float(0)

        return payload

    def compile_value(self, value, unit):
        if 2 > 1:
            # try:
            if unit == "ampere":
                p = re.compile(r'^(.)(..)*')
            if unit == "volt":
                p = re.compile(r'^(..)(..)*')
            m = re.match(p, value)
            if m.group(1):
                int1 = m.group(1)
            else:
                int1 = 0
            if m.group(2):
                int2 = m.group(2)
            else:
                int2 = 0
            result = str(int1) + "." + str(int2)
            # except:
            # result = "False"
        return result

    def serial_data_prepare(self, payload):
        data = dict(
            battery_voltage=float(payload[0]/100),
            pv_voltage=float(payload[1]/100),
            reserved1=str(payload[2]),
            load_current=float(payload[3]),
            over_discharge_voltage=float(payload[4]/100),
            battery_full_voltage=float(payload[5]/100),
            load=str(payload[6]),
            overload=str(payload[7]),
            load_short_circuit=str(payload[8]),
            # reserved2=str(payload[9]),
            battery_overload=str(payload[10]),
            over_discharge=str(payload[11]),
            full_indicator=str(payload[12]),
            charging_indicator=str(payload[13]),
            battery_temperature=float(payload[14]),
            charging_current=str(payload[15]))

        for key, value in data.items():
            
            try:
                if self.isnumeric(value):
                    data[key] = float(value)
            except Exception as exc:
                pass

        return data


if __name__ == "__main__":
    config = ()
    epsolar = Epsolar(config)

    # Connect serial port
    serial_data, serial_read = epsolar.read_serial()
    print('Serial Data: ', format(serial_data))

    serial_data_converted = epsolar.decode_serial(serial_data)
    serial_data_decoded = epsolar.serial_data_prepare(serial_data_converted)
    serial_data_prepared = epsolar.serial_data_prepare(serial_data)

    print(serial_data_prepared)
    print(serial_data_decoded)
