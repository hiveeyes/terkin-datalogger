:orphan:

.. _setup-lorawan-ttn:

#################
LoRaWAN/TTN Setup
#################

*******
General
*******
In case of using the Terkin Datalogger firmware with the Hiveeyes.org
environment please follow this scheme for the TTN ``dev_id``:

``hiveeyes-USER-LOCATION-NAMEOFHIVE``

and replace upper case strings with your individual lower case namings
without additional dashes. ``hiveeyes-USER`` will become your InfluxDB
client data base and ``LOCATION-NAMEOFHIVE_sensors`` will be your InfluxDB
measurement name.

In ``settings.py`` networking section enter your TTN device credentials
(copy and paste from TTN console) and deactivate all telemetry targets
except ``CayenneLPP over TTN-LoRa``. ``datarate`` defines the
`bandwidth and spreading factor <https://www.thethingsnetwork.org/docs/lorawan/modulation-data-rate.html>`_
for the joining process while ``'adr' = True`` enables the
`Adaptive Data Rate <https://www.thethingsnetwork.org/docs/lorawan/adaptive-data-rate.html>`_
for subsequent data packages depending on the LoRa signal quality.

**********
CayenneLPP
**********
`CayenneLPP <https://developers.mydevices.com/cayenne/docs/lora/#lora-cayenne-low-power-payload>`_
is our sensor data encoding standard of choice in conjunction with LoRaWAN transmissions.
It ensures small data packages and consequently little air times for actually sending the data.

The `upstream CayenneLPP Python library <https://github.com/smlng/pycayennelpp>`_
has been extended to also encode ``load`` and ``voltage`` readings.
In order to forward those variables into your TTN payload you would need to insert
the given decoder.js code into your TTN App. In TTN console under Payload Formats
switch to Custom and paste the Javascript from
`decoder.js <https://github.com/hiveeyes/terkin-datalogger/blob/master/client/TTN/decoder.js>`_.
The decoder function is backwards compatible to the built-in CayenneLPP decoder.

*********************
PutsReq HTTP Endpoint
*********************
An instance of `PutsReq.com <https://putsreq.com>`_ hosted on hiveeyes.org
will serve as your HTTP endpoint in the `TTN HTTP integration <https://www.thethingsnetwork.org/docs/applications/http/>`_.

It's a free service for inspecting and rewriting HTTP POST requests to a
response that our data acquisition service (DAQ) at `swarm.hiveeyes.org <https://swarm.hiveeyes.org>`_
will be able to understand and process.

HTTP endpoint URLs for common use are already set up and can be requested from
@thiasB or @ClemensGruber but you can of course set up your own endpoint and use the
Javascript provided in

- `putsreq.hiveeyes.js <https://raw.githubusercontent.com/hiveeyes/terkin-datalogger/master/client/TTN/putsreq.hiveeyes.js>`_ for the Hiveeyes.org target, or
- `putsreq.bee-observer.js <https://raw.githubusercontent.com/hiveeyes/terkin-datalogger/master/client/TTN/putsreq.bee-observer.js>`_ for the bee-observer.org target, or
- `putsreq.beep.js <https://raw.githubusercontent.com/hiveeyes/terkin-datalogger/master/client/TTN/putsreq.beep.js>`_ for the beep.nl target

************
Telegram Bot
************
A Telegram bot for interacting with the device via LoRaWAN downlinks is
available from the `telegram_terkin_ttn_bot.py <https://github.com/hiveeyes/terkin-datalogger/blob/master/client/TTN/telegram_terkin_ttn_bot.py>`_ file.

Currently these two capabilities are implemented:

- ``/pause`` and ``/unpause`` for pausing and continuing the inclusion of
  sensor data into the payload, e.g for times when you are working on the bees hives.
- ``/sleep MIN`` for remotely setting the Deep Sleep interval in ``MIN`` minutes.
  Send ``/sleep 0`` to return to the interval defined in your device configuration.

Please see `Telegram bot documentation <https://core.telegram.org/bots>`_ for
how to get started with a bot at first. An always-on server under your control
will be needed to run the bot. Remember that downlink messages to the device
are not being sent immediately but shortly after an uplink message has been
successfully received by the network.
