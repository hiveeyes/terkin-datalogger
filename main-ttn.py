import time
import socket
import ubinascii
from network import LoRa


def init_lora_wan(lora, timeout):
    app_eui = ubinascii.unhexlify('XXX')
    app_key = ubinascii.unhexlify('YYY')
    # #join a network using OTAA (Over the Air Activation)
    lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
    while not lora.has_joined():
        time.sleep(2.5)
        print('Not joined LoRa.OTAA yet ...')
    # #create a LoRa socket
    lorasocket = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    # set the LoRaWAN data rate
    lorasocket.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
    return lorasocket


def sent_lora_message(lorasocket, p):
    # Send LoRaWAN Message
    lorasocket.setblocking(True)
    lorasocket.send(p)
    # make the socket non-blocking
    # (because if there's no data received it will block forever...)
    lorasocket.setblocking(False)
    return lorasocket.recv(64)
