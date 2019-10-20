# -*- coding: utf-8 -*-
# License: GNU General Public License, Version 3

from bluetooth import BLE, UUID, FLAG_NOTIFY, FLAG_READ, FLAG_WRITE
from micropython import const
from ble_advertising import advertising_payload
from terkin import logging

_IRQ_CENTRAL_CONNECT                 = const(1 << 0)
_IRQ_CENTRAL_DISCONNECT              = const(1 << 1)

# org.bluetooth.service.battery_service - BS
_BS_UUID = UUID(0x180F)
# org.bluetooth.characteristic.battery_level
_BS_CHAR = (UUID(0x2A19), FLAG_READ | FLAG_NOTIFY,)
_BS_SERVICE = (_BS_UUID, (_BS_CHAR,), )

# org.bluetooth.service.weight_scale - WS
_WS_UUID = UUID(0x181D)
# org.bluetooth.characteristic.weight_measurement
_WS_CHAR = (UUID(0x2A9D), FLAG_READ | FLAG_NOTIFY,)
_WS_SERVICE = (_WS_UUID, (_WS_CHAR,), )

# org.bluetooth.service.environmental_sensing - ES
_ES_UUID = UUID(0x181A)
# org.bluetooth.characteristic.humidity
_ES_CHAR_HUM = (UUID(0x2A6F), FLAG_READ | FLAG_NOTIFY,)
# org.bluetooth.characteristic.temperature
_ES_CHAR_TEMP = (UUID(0x2A6E), FLAG_READ | FLAG_NOTIFY,)
_ES_SERVICE = (_ES_UUID, (_ES_CHAR_HUM, _ES_CHAR_TEMP,), )

# org.bluetooth.service.generic_access - GA
_GA_UUID = UUID(0x1800)
# org.bluetooth.characteristic.gap.device_name
_GA_CHAR_NAME = (UUID(0x2A00), FLAG_READ | FLAG_NOTIFY,)
# org.bluetooth.characteristic.gap.appearance
_GA_CHAR_APP =  (UUID(0x2A01), FLAG_READ | FLAG_NOTIFY,)
_GA_SERVICE = (_GA_UUID, (_GA_CHAR_NAME, _GA_CHAR_APP,), )

# time TBD
# org.bluetooth.service.current_time - CT
#_CT_UUID = UUID(0x1805)
# org.bluetooth.characteristic.weight_measurement
#_CT_CHAR = (UUID(0x2A00), FLAG_READ | FLAG_NOTIFY,)
#_CT_SERVICE = (_CT_UUID, (_CT_CHAR,), )

SERVICES = (_BS_SERVICE, _WS_SERVICE, _ES_SERVICE, _GA_SERVICE,)

# set appearance - sets the icon
# org.bluetooth.characteristic.gap.appearance.xml
_ADV_APPEARANCE_GENERIC_WEIGHT_SCALE = const(3200)

log = logging.getLogger(__name__)

class BluetoothApiESP32:
    """
    
    """

    def __init__(self, ble, name='hiveeyes'):
        """
        """
        self._reading = reading  # last_reading from datalogger.storage
        self._ble = ble
        self.start()    
        self._ble.irq(handler=self._irq)
        ((self._handle,),) = self._ble.gatts_register_services(SERVICES)
        self._connections = set()
        # advertise that we are here and what services we provide
        self._payload = advertising_payload(name=name, services=([0x180F],[0x181A],[0x181D],[0x1800]), appearance=_ADV_APPEARANCE_GENERIC_THERMOMETER)
        self._advertise()


    def start(self):
        log.info('Starting Bluetooth')
        self._ble.active(True)

    def stop(self):
        log.info('Stopping Bluetooth')
        self._ble.active(False)

    def _advertise(self, interval_us=1000000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload)

    def set_battery_level(self, level=0, notify=False): 
        """
        level in [%]
        Data is uint8.
        """
        self._ble.gatts_write(self._handle, struct.pack('<B', int(level)))
        if notify:
            for conn_handle in self._connections:   # Notify connected centrals to issue a read.
                self._ble.gatts_notify(conn_handle, self._handle)        

    def set_weight(self, weight=0.0, notify=False): 
        """
        weight in [kg]
        Data is uint16. Unit is in kilograms with a resolution of 0.005.
        """
        self._ble.gatts_write(self._handle, struct.pack('<H', int(weight/0.005)))
        if notify:
            for conn_handle in self._connections:   # Notify connected centrals to issue a read.
                self._ble.gatts_notify(conn_handle, self._handle)

def demo():
    ble = bluetooth.BLE()
    ble32 = BluetoothApiESP32(ble)

    while True:
        print('loop')
        time.sleep_ms(1000)


if __name__ == '__main__':
    demo()