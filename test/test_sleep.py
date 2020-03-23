# -*- coding: utf-8 -*-
# (c) 2020 Richard Pobering <richard@hiveeyes.org>
# (c) 2020 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import re
import mock
import pytest
from test.util.terkin import invoke_datalogger_pycom


@pytest.mark.sleep
@mock.patch('sys.platform', 'WiPy')
def test_timesleep(mocker, caplog):
    """
    Check normal "time.sleep()" behavior without any machine.sleep methods.
    """

    # Acquire minimal settings.
    from test.settings import sleep as sleep_settings

    # Invoke datalogger for a single duty cycle.
    datalogger = invoke_datalogger_pycom(caplog, settings=sleep_settings)

    # Patch machinery to mock the sleep method.
    import time
    mocker.patch('time.sleep', create=True)

    # Invoke sleep.
    datalogger.sleep()

    # Proof the "time.sleep" function has been invoked.
    time.sleep.assert_called_once()

    # Capture log output.
    captured = caplog.text

    # Proof it works by verifying log output.
    assert re.match('.*Waiting for .+ seconds.*', captured, flags=re.DOTALL), captured


@pytest.mark.sleep
@mock.patch('sys.platform', 'WiPy')
def test_lightsleep(mocker, caplog):
    """
    Check lightsleep behavior.
    """

    # Acquire minimal settings.
    from test.settings import sleep as sleep_settings

    # Set lightsleep mode.
    sleep_settings.main['lightsleep'] = True

    # Invoke datalogger for a single duty cycle.
    datalogger = invoke_datalogger_pycom(caplog, settings=sleep_settings)

    # Patch machinery to mock the sleep method.
    import machine
    mocker.patch('machine.sleep', create=True)

    # Invoke sleep.
    datalogger.sleep()

    # Proof the "machine.sleep" function has been invoked.
    machine.sleep.assert_called_once()

    # Capture log output.
    captured = caplog.text

    # Proof it works by verifying log output.
    assert re.match('.*Entering light sleep for .+ seconds.*', captured, flags=re.DOTALL), captured


@pytest.mark.sleep
@mock.patch('sys.platform', 'WiPy')
def test_deepsleep(mocker, caplog):
    """
    Check deepsleep behavior.
    """

    # Acquire minimal settings.
    from test.settings import sleep as sleep_settings

    # Set deepsleep mode.
    sleep_settings.main['deepsleep'] = True

    # Invoke datalogger for a single duty cycle.
    datalogger = invoke_datalogger_pycom(caplog, settings=sleep_settings)

    # Patch machinery to mock the sleep method.
    import machine
    mocker.patch('machine.deepsleep', create=True)

    # Invoke sleep.
    datalogger.sleep()

    # Proof the "machine.deepsleep" function has been invoked.
    machine.deepsleep.assert_called_once()

    # Capture log output.
    captured = caplog.text

    # Proof it works by verifying log output.
    assert re.match('.*Entering deep sleep for .+ seconds.*', captured, flags=re.DOTALL), captured


@pytest.mark.sleep
@mock.patch('sys.platform', 'WiPy')
def test_maintenance(mocker, caplog):
    """
    Check maintenance mode.

    When the device is in maintenance mode, a different duty cycle
    will apply and the sleep method will resort to "time.sleep" in
    order to keep the appliance "online", even when deepsleep mode
    is enabled through the configuration.
    """

    # Acquire minimal settings.
    from test.settings import sleep as sleep_settings

    # Set deepsleep mode.
    sleep_settings.main['deepsleep'] = True

    # Invoke datalogger for a single duty cycle.
    datalogger = invoke_datalogger_pycom(caplog, settings=sleep_settings)

    # Enable maintenance mode.
    datalogger.device.status.maintenance = True

    # Patch machinery to mock the sleep method.
    import time
    mocker.patch('time.sleep', create=True)

    # Invoke sleep.
    datalogger.sleep()

    # Proof the "time.sleep" function has been invoked.
    time.sleep.assert_called_once()

    # Capture log output.
    captured = caplog.text

    # Proof it works by verifying log output.
    assert re.match('.*Device is in maintenance mode. Skipping deep sleep and adjusting sleep time to .+ seconds..*', captured, flags=re.DOTALL), captured
    assert re.match('.*Waiting for .+ seconds.*', captured, flags=re.DOTALL), captured
