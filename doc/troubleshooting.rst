########################################
Hiveeyes MPY data logger troubleshooting
########################################

1. Not connected to WiFi

Traceback (most recent call last):
  File "main.py", line 32, in <module>
  File "/flash/lib/telemetry.py", line 209, in transmit
  File "/flash/lib/telemetry.py", line 87, in transmit
  File "/flash/lib/telemetry.py", line 151, in __init__
  File "/flash/lib/mqtt.py", line 19, in __init__
OSError: Avialable Interfaces are down


2. Strange "no nic" error

https://github.com/pycom/pycom-micropython-sigfox/issues/196

Traceback (most recent call last):
  File "main.py", line 32, in <module>
  File "/flash/lib/telemetry.py", line 209, in transmit
  File "/flash/lib/telemetry.py", line 87, in transmit
  File "/flash/lib/telemetry.py", line 151, in __init__
  File "/flash/lib/mqtt.py", line 19, in __init__
OSError: no available NIC

=> Upgrade your firmware.


3. Building
make: *** No rule to make target `build/FIPY/release/frozen_mpy/frozen/Base/_main.mpy', needed by `build/FIPY/release/frozen_mpy.c'.  Stop.
- https://github.com/pycom/pycom-micropython-sigfox/issues/214
- https://github.com/pycom/pycom-micropython-sigfox/issues/220

Solution: https://github.com/pycom/pycom-micropython-sigfox/issues/220#issuecomment-431536064
::

    cd pycom-micropython-sigfox
    patch py/mkrules.mk < mkrules.patch


4. ImportError: No module named serial
::

    python /Users/amo/dev/hiveeyes/tools/pycom/pycom-esp-idf/components/esptool_py/esptool/esptool.py --chip esp32 elf2image --flash_mode dio --flash_freq 80m -o build/FIPY/release/bootloader/bootloader.bin build/FIPY/release/bootloader/bootloader.elf
    Pyserial is not installed for /usr/local/opt/python@2/bin/python2.7. Check the README for installation instructions.
    Traceback (most recent call last):
      File "/Users/amo/dev/hiveeyes/tools/pycom/pycom-esp-idf/components/esptool_py/esptool/esptool.py", line 37, in <module>
        import serial
    ImportError: No module named serial
    make: *** [build/FIPY/release/bootloader/bo


5. No connectivity

Starting TerkinTelemetry
Import MQTT client library
Channel URI:  mqtt://swarm.hiveeyes.org/hiveeyes/testdrive/area-23/node-1
mqtt connect: swarm.hiveeyes.org 1883
Traceback (most recent call last):
  File "main.py", line 56, in <module>
  File "/flash/lib/telemetry.py", line 211, in transmit
  File "/flash/lib/telemetry.py", line 89, in transmit
  File "/flash/lib/telemetry.py", line 155, in __init__
  File "/flash/lib/mqtt.py", line 60, in connect
OSError: Network card not available


