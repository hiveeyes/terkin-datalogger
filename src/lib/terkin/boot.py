import sys

# Invoke bootloader.
def start_bootloader():
    from umal import MicroPythonBootloader
    bootloader = MicroPythonBootloader()
    sys.modules['__main__'].bootloader = bootloader
    return bootloader
