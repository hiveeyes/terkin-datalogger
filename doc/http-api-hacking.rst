##############################
Hacking on the Terkin HTTP API
##############################


************
Introduction
************
This process describes how to hack efficiently on the HTTP API.

For hacking on the code in general, you should be able to
`operate the Terkin Datalogger Sandbox`_ and the
`MicroTerkin Agent`_ well. Knowing something about the
`Terkin Firmware maintenance mode`_ will also do no harm.

Steps outlined in this document assume you are running the
development sandbox successfully.


***********
Walkthrough
***********
1. For the baseline sandbox installation, please follow
   the documentation at `operate the Terkin Datalogger Sandbox`_.
2. Disable deep sleep and watchdog features in your ``settings.py``.
3. Provision source code and restart the device

::

    # Start MicroTerkin Agent
    make terkin-agent action=monitor

    # Watch console output
    make console

    # Upload files and restart the device
    make recycle-ng

4. Send requests to the HTTP API
::

    http "http://$(cat .terkin/floatip)/status"
    OK


*****
Spots
*****
The file ``terkin/api/http.py`` will be the right place to look at.

Have fun!



.. _operate the Terkin Datalogger Sandbox: https://community.hiveeyes.org/t/operate-the-terkin-datalogger-sandbox/2332
.. _MicroTerkin Agent: https://community.hiveeyes.org/t/the-microterkin-agent/2333
.. _Terkin Firmware maintenance mode: https://community.hiveeyes.org/t/wartungsmodus-fur-den-terkin-datenlogger/2274
