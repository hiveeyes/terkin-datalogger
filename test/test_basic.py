import os
import sys
import logging

from pyfakefs.fake_filesystem_unittest import Patcher as FakeFS

from test.util.terkin import start_umal


def test_basic_esp32(monkeypatch, caplog):

    # Define platform and start bootloader.
    monkeypatch.setattr(sys, 'platform', 'esp32')
    bootloader = start_umal()

    # Use very basic settings without networking.
    import test.settings.basic as settings

    # Start datalogger with a single duty cycle on a fake filesystem.
    from terkin.datalogger import TerkinDatalogger
    with FakeFS():

        with caplog.at_level(logging.DEBUG):
            datalogger = TerkinDatalogger(settings, platform_info=bootloader.platform_info)
            datalogger.setup()
            datalogger.duty_task()

            # Capture log output.
            captured = caplog.text

            # Proof it works by verifying log output.
            assert "Starting Terkin datalogger" in captured, captured
            assert "platform: esp32" in captured, captured
            assert "[WiFi] interface disabled in settings" in captured, captured
            assert "[LoRa] This is not a LoRa capable device" in captured, captured
            assert "[GPRS] Interface disabled in settings" in captured, captured
            assert "Reading 0 sensor ports" in captured, captured
            assert "Sensor data:  {}" in captured, captured
            assert "Telemetry status: SUCCESS (0/0)" in captured, captured


def test_basic_wipy(monkeypatch, caplog):

    # Define platform and start bootloader.
    monkeypatch.setattr(sys, 'platform', 'WiPy')
    bootloader = start_umal()

    # Use very basic settings without networking.
    import test.settings.basic as settings

    # Start datalogger with a single duty cycle on a fake filesystem.
    from terkin.datalogger import TerkinDatalogger
    with FakeFS():
        # Pycom mounts the main filesystem at "/flash".
        os.mkdir('/flash')

        with caplog.at_level(logging.DEBUG):
            datalogger = TerkinDatalogger(settings, platform_info=bootloader.platform_info)
            datalogger.setup()
            datalogger.duty_task()

            # Capture log output.
            captured = caplog.text

            # Proof it works by verifying log output.
            assert "Starting Terkin datalogger" in captured, captured
            assert "platform: WiPy" in captured, captured


def test_basic_cpython(monkeypatch, caplog):

    # Define platform and start bootloader.
    monkeypatch.setattr(sys, 'platform', 'linux2')
    bootloader = start_umal()

    # Use very basic settings without networking.
    import test.settings.basic as settings

    # Start datalogger with a single duty cycle on a fake filesystem.
    from terkin.datalogger import TerkinDatalogger
    with FakeFS():

        with caplog.at_level(logging.DEBUG):
            datalogger = TerkinDatalogger(settings, platform_info=bootloader.platform_info)
            datalogger.setup()
            datalogger.duty_task()

            # Capture log output.
            captured = caplog.text

            # Proof it works by verifying log output.
            assert "Starting Terkin datalogger" in captured, captured
            assert "platform: linux2" in captured, captured
