# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import utime
import machine
import ubinascii
from network import Bluetooth
from terkin.network.ble.util import BluetoothUuid, sint16, uint16, encode_temperature_2a1c


class BluetoothApi:
    """Many examples integrated from
    https://microchipdeveloper.com/wireless:ble-gatt-data-organization
    https://development.pycom.io/firmwareapi/pycom/network/bluetooth/
    https://github.com/sandeepmistry/arduino-BLEPeripheral
    https://github.com/kriswiner/nRF52832DevBoard/blob/master/BMP280_nRF52.ino
    
    https://forum.pycom.io/topic/2826/how-to-send-data-to-characteristic-over-ble/17


    """

    def __init__(self):
        self.bt = None

    def start(self):
        """ """

        print('Starting Bluetooth')
        self.bt = Bluetooth()

        # Default
        #self.bt.init(id=0, mode=Bluetooth.BLE, antenna=Bluetooth.INT_ANT, modem_sleep=True)
        #self.bt.init(id=0, antenna=Bluetooth.INT_ANT, modem_sleep=False)
        self.bt.init(modem_sleep=False)

        return

        print('Entering main loop')
        while True:
            print('--- loop ---')

            adv = self.bt.get_adv()
            print('adv:', adv)

            # Give the system some breath.
            print('machine.idle()')
            machine.idle()

            utime.sleep(10.0)
            continue

    def scan(self, duration):
        """

        :param duration: 

        """
        duration = int(duration)
        print('Starting Bluetooth scan for {} seconds'.format(duration))
        self.bt.start_scan(duration)
        while self.bt.isscanning():
            #print('is-scanning')
            adv = self.bt.get_adv()
            if adv:
                # try to get the complete name
                name_short = self.bt.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_SHORT)
                name_complete = self.bt.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL)
                print('names:', name_short, name_complete)

                service_data = self.bt.resolve_adv_data(adv.data, Bluetooth.ADV_SERVICE_DATA)
                print('service_data:', service_data)

                mfg_data = self.bt.resolve_adv_data(adv.data, Bluetooth.ADV_MANUFACTURER_DATA)
                if mfg_data:
                    # try to get the manufacturer data (Apple's iBeacon data is sent here)
                    data = ubinascii.hexlify(mfg_data)
                    print('data:', data)

        print('Bluetooth scanning stopped')

    def find_heart_rate(self):
        """ """
        adv = self.bt.get_adv()
        if adv and self.bt.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL) == 'Heart Rate':
            try:
                conn = self.bt.connect(adv.mac, timeout=5000)
                services = conn.services()
                for service in services:
                    utime.sleep(0.050)
                    if type(service.uuid()) == bytes:
                        print('Reading chars from service = {}'.format(service.uuid()))
                    else:
                        print('Reading chars from service = %x' % service.uuid())
                    chars = service.characteristics()
                    for char in chars:
                        if (char.properties() & Bluetooth.PROP_READ):
                            print('char {} value = {}'.format(char.uuid(), char.read()))
                conn.disconnect()
            except:
                print("Error while connecting or reading from the BLE device")
        else:
            utime.sleep(0.050)

        utime.sleep(10.0)

    def advertise(self):
        """https://development.pycom.io/firmwareapi/pycom/network/bluetooth/"""

        device_name = get_device_name()
        print('Advertising device {}'.format(device_name))
        # TODO: Get from settings
        self.bt.set_advertisement(name=device_name, service_uuid=b'1234567890123456')

        def conn_cb(bt_o):
            """

            :param bt_o: 

            """
            print("Callback happened")
            # Returns flags and clear internal registry
            events = bt_o.events()
            if events & Bluetooth.CLIENT_CONNECTED:
                print("Client connected:", events)
            elif events & Bluetooth.CLIENT_DISCONNECTED:
                print("Client disconnected")

        self.bt.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED, handler=conn_cb)

        self.bt.advertise(True)

    def start_service(self):
        """https://development.pycom.io/firmwareapi/pycom/network/bluetooth/gattsservice/
        https://development.pycom.io/firmwareapi/pycom/network/bluetooth/gattscharacteristic/
        
        https://www.bluetooth.com/specifications/gatt/characteristics/
        https://docs.python.org/3/library/struct.html
        
        The format field determines how a single value contained in the Characteristic Value is formatted.
        The information contained on this page is referenced in Bluetooth® Core Specification Volume 3, Part G, Section 3.3.3.5.2.
        https://www.bluetooth.com/specifications/assigned-numbers/format-types/


        """
        print('Starting service')

        # A. Battery Service
        # UUID: 180F
        # Abstract: The Battery Service exposes the state of a battery within a device
        # https://github.com/oesmith/gatt-xml/blob/master/org.bluetooth.service.battery_service.xml
        battery = self.bt.service(uuid=0x180F, isprimary=True, nbr_chars=1, start=True)

        # Battery Level
        # UUID: 2A19
        # Abstract: The current charge level of a battery.
        #           100% represents fully charged while 0% represents fully discharged
        # Format: uint8
        # https://github.com/oesmith/gatt-xml/blob/master/org.bluetooth.characteristic.battery_level.xml
        battery_level = battery.characteristic(uuid=0x2A19, value=78)

        # B. Environmental Sensing Service (ESS)
        # https://github.com/oesmith/gatt-xml/blob/master/org.bluetooth.service.environmental_sensing.xml
        # https://www.bluetooth.com/specifications/assigned-numbers/environmental-sensing-service-characteristics/
        # https://github.com/sandeepmistry/arduino-BLEPeripheral/issues/215
        # https://github.com/sandeepmistry/arduino-nRF5/issues/248
        environment = self.bt.service(uuid=0x181A, isprimary=True, nbr_chars=5, start=True)

        # Temperature
        # UUID: 2A6E
        # InformativeText: Unit is in degrees Celsius with a resolution of 0.01 degrees Celsius
        # Format: sint16
        # https://github.com/oesmith/gatt-xml/blob/master/org.bluetooth.characteristic.temperature.xml
        # https://github.com/oesmith/gatt-xml/blob/master/org.bluetooth.characteristic.temperature_measurement.xml
        # https://github.com/oesmith/gatt-xml/blob/master/org.bluetooth.characteristic.temperature_type.xml
        # https://github.com/ARMmbed/ble/blob/master/ble/services/HealthThermometerService.h
        # https://github.com/ARMmbed/ble/blob/master/ble/services/EnvironmentalService.h

        # Temperature Celsius
        # UUID: 2A1F
        # Format: sint16
        # https://www.bluetooth.com/wp-content/uploads/Sitecore-Media-Library/Gatt/Xml/Characteristics/org.bluetooth.characteristic.temperature_celsius.xml
        self.temp = 42.42
        temperature = environment.characteristic(uuid=0x2A1F)
        def temp_getter(chr):
            """

            :param chr: 

            """
            print('Getting characteristic:', chr)
            value = sint16(self.temp * 10)
            print('Value:', value)
            self.temp += 1
            return value
        print('Adding characteristic callback')
        temperature_callback = temperature.callback(trigger=Bluetooth.CHAR_READ_EVENT, handler=temp_getter)

        # Temperature Measurement
        # UUID: 2A1C
        # Format: Variable length structure
        # Value Format: FLOAT (IEEE-11073 32-bit FLOAT)
        # Abstract: The Temperature Measurement characteristic is a variable length structure
        # containing a Flags field, a Temperature Measurement Value field and, based upon the
        # contents of the Flags field, optionally a Time Stamp field and/or a Temperature Type field.
        # https://www.bluetooth.com/wp-content/uploads/Sitecore-Media-Library/Gatt/Xml/Characteristics/org.bluetooth.characteristic.temperature_measurement.xml
        print('Adding Temperature Measurement')
        temperature_measurement = environment.characteristic(uuid=0x2A1C, value=encode_temperature_2a1c(42.428423))

        # Scientific Temperature
        # UUID: 2A3C
        # Format: float64 (IEEE-754 64-bit floating point)
        # https://www.bluetooth.com/wp-content/uploads/Sitecore-Media-Library/Gatt/Xml/Characteristics/org.bluetooth.characteristic.scientific_temperature_celsius.xml
        # http://forum.espruino.com/conversations/306536/
        # https://stackoverflow.com/questions/36655172/how-to-read-a-ble-characteristic-float-in-swift

        # For the 'f', 'd' and 'e' conversion codes, the packed representation uses the IEEE 754
        # binary32, binary64 or binary16 format (for 'f', 'd' or 'e' respectively), regardless of
        # the floating-point format used by the platform.
        # https://docs.python.org/3/library/struct.html
        #print('Adding Scientific Measurement')
        #temperature_sci = environment.characteristic(uuid=0x2A3C, value=float64(42.42))

        # Humidity
        # UUID: 2A6F
        # InformativeText: Unit is in percent with a resolution of 0.01 percent
        # Format: uint16
        # https://github.com/oesmith/gatt-xml/blob/master/org.bluetooth.characteristic.humidity.xml
        humidity1 = environment.characteristic(uuid=0x2A6F, value=uint16(86.86 * 100))
        humidity2 = environment.characteristic(uuid=0x2A6F, value=uint16(50.55 * 100))

        # Pressure
        # UUID: 2A6D
        # InformativeText: Unit is in pascals with a resolution of 0.1 Pa
        # Format: uint32
        # https://www.bluetooth.com/wp-content/uploads/Sitecore-Media-Library/Gatt/Xml/Characteristics/org.bluetooth.characteristic.pressure.xml

        # Weight
        # UUID: 2A98
        # InformativeText: Unit is in kilograms with a resolution of 0.005
        # Format: uint16
        # https://www.bluetooth.com/wp-content/uploads/Sitecore-Media-Library/Gatt/Xml/Characteristics/org.bluetooth.characteristic.weight.xml
        # https://www.bluetooth.com/wp-content/uploads/Sitecore-Media-Library/Gatt/Xml/Characteristics/org.bluetooth.characteristic.weight_measurement.xml
        # https://www.bluetooth.com/wp-content/uploads/Sitecore-Media-Library/Gatt/Xml/Characteristics/org.bluetooth.characteristic.weight_scale_feature.xml
        # https://github.com/oesmith/gatt-xml/blob/master/org.bluetooth.characteristic.weight.xml
        # https://github.com/oesmith/gatt-xml/blob/master/org.bluetooth.characteristic.weight_measurement.xml
        # https://github.com/oesmith/gatt-xml/blob/master/org.bluetooth.characteristic.weight_scale_feature.xml
        weight = environment.characteristic(uuid=0x2A98, value=uint16(25.44 * 2 * 100))

        # GPS
        # https://forum.pycom.io/topic/5012/can-only-see-value-of-first-gatt-characteristic
        """
        lan = bt.service(0x1819, nbr_chars=3)
        # 0.001 precision
        lan.characteristic(uuid=0x2AAE, value=int(gps.lat * 1000))
        lan.characteristic(uuid=0x2AAF, value=int(gps.lon * 1000))
        lan.characteristic(uuid=0x2AB3, value=int(gps.alt * 1000))
        """

        # Generic Access
        # UUID: 1800
        # Abstract: The generic_access service contains generic information
        # about the device. All available Characteristics are readonly.
        # https://www.bluetooth.com/wp-content/uploads/Sitecore-Media-Library/Gatt/Xml/Services/org.bluetooth.service.generic_access.xml

        # Generic Attribute Service
        # UUID: 1801
        # https://www.bluetooth.com/wp-content/uploads/Sitecore-Media-Library/Gatt/Xml/Services/org.bluetooth.service.generic_attribute.xml
        # String Characteristic
        # UUID: 2A3D
        # A generic UTF8 string which may be used in Services requiring strings.
        # https://www.bluetooth.com/wp-content/uploads/Sitecore-Media-Library/Gatt/Xml/Characteristics/org.bluetooth.characteristic.string.xml
        srv1 = self.bt.service(uuid=BluetoothUuid.to_bytes_le('15ECCA29-0B6E-40B3-9181-BE9509B53200'), isprimary=True, nbr_chars=2, start=True)
        #generic_attribute = self.bt.service(uuid=0x1800, isprimary=True, nbr_chars=2, start=True)
        #wifi_ssid = generic_attribute.characteristic(uuid=0x2A3D, properties=Bluetooth.PROP_BROADCAST | Bluetooth.PROP_INDICATE | Bluetooth.PROP_NOTIFY | Bluetooth.PROP_READ | Bluetooth.PROP_WRITE, value="default")
        #wifi_ssid = generic_attribute.characteristic(uuid=0x2A3D, properties=Bluetooth.PROP_NOTIFY | Bluetooth.PROP_READ | Bluetooth.PROP_WRITE, value="default")
        wifi_ssid = srv1.characteristic(uuid=0x2A3D)
        #wifi_password = generic_attribute.characteristic(uuid=0x2A3D, properties=Bluetooth.PROP_READ | Bluetooth.PROP_WRITE)
        #print('wifi_ssid:', wifi_ssid, dir(wifi_ssid))
        #cfg = wifi_ssid.config()
        #print('cfg:', cfg)
        #wifi_ssid.config(name='hallodri')

        print('wifi_ssid:', wifi_ssid)
        print('wifi_ssid:', dir(wifi_ssid))

        def wifi_callback(characteristic):
            """

            :param characteristic: 

            """
            print('Characteristic callback:', characteristic)
            #print('attr_obj:', characteristic.attr_obj)
            events = characteristic.events()
            if events & Bluetooth.CHAR_WRITE_EVENT:
                print("Write request with value = {}".format(characteristic.value()))
            else:
                pass
            value = characteristic.value()
            print('Reading characteristic:', value)

        print('Adding characteristic callback')
        wifi_ssid_callback = wifi_ssid.callback(trigger=Bluetooth.CHAR_READ_EVENT | Bluetooth.CHAR_WRITE_EVENT, handler=wifi_callback)
        #wifi_password_callback = wifi_password.callback(trigger=Bluetooth.CHAR_READ_EVENT | Bluetooth.CHAR_WRITE_EVENT, handler=wifi_callback)

        #print('instance:', wifi_ssid.instance())

        # Characteristic User Description
        # UUID: 0x2901,0x2902
        print(wifi_ssid_callback)
        print(dir(wifi_ssid_callback))
        srv1.characteristic(uuid=0x2901, value="hello world 1")
        #wifi_ssid_callback.characteristic(uuid=0x2901, value="hello world 2")

        # Automation IO
        # UUID: 1815
        # Abstract: The Automation IO service is used to expose the analog
        # inputs/outputs and digital input/outputs of a generic IO module (IOM).
        # https://www.bluetooth.com/wp-content/uploads/Sitecore-Media-Library/Gatt/Xml/Services/org.bluetooth.service.automation_io.xml

        # User Data
        # UUID: 181C
        # Abstract: This service exposes user-related data in the sports and fitness environment.
        # This allows remote access and update of user data by a Client as well as the synchronization
        # of user data between a Server and a Client.
        # https://www.bluetooth.com/wp-content/uploads/Sitecore-Media-Library/Gatt/Xml/Services/org.bluetooth.service.user_data.xml
        #user_data = self.bt.service(uuid=0x0123456789ABCDEF, isprimary=True, nbr_chars=1, start=True)


def get_device_id():
    """ """
    import machine
    from ubinascii import hexlify
    return hexlify(machine.unique_id()).decode()


def get_device_name():
    """ """
    import os
    osname = os.uname().sysname
    sysid = get_device_id()
    name = 'Terkin-{}-{}'.format(osname, sysid)
    return name


if __name__ == '__main__':
    """Main application entrypoint."""
    global btapi
    btapi = BluetoothApi()
    btapi.start()
    #btapi.scan(2)
    btapi.advertise()
    btapi.start_service()

    #print('Sleeping for 20 seconds')
    #utime.sleep(20)
