#################
TTN/LoRaWAN Setup
#################

*******
General
*******

In case of using the Terkin Datalogger firmware with the Hiveeyes.org environment please follow this scheme for the TTN ``dev_id``:

``hiveeyes-USER-LOCATION-NAMEOFHIVE``

and replace upper case strings with your individual lower case namings without additional dashes. ``hiveeyes-USER`` will becomce your  InfluxDB client data base and ``LOCATION-NAMEOFHIVE_sensors`` your InfluxDB measurement name.

In ``settings.py`` networking section enter your TTN device credentials (copy and paste from TTN console) and deactivate all telemetry targets except ``CayenneLPP over TTN-LoRa``. ``datarate`` defines the `bandwidth and spreading factor <https://www.thethingsnetwork.org/docs/lorawan/modulation-data-rate.html>`_ for the joining process while ``'adr' = True`` enables the `Adaptive Data Rate <https://www.thethingsnetwork.org/docs/lorawan/adaptive-data-rate.html>`_.

**********
CayenneLPP
**********

`CayenneLPP <https://developers.mydevices.com/cayenne/docs/lora/#lora-cayenne-low-power-payload>`_ is our sensor data encoding standard of choice in conjuntion with LoRaWAN transmissions. It ensures small data packages and consequently little air times for actually sending the data. The `upstream CayenneLPP Python library <https://github.com/smlng/pycayennelpp>`_ has been extended to also encode ``load`` and ``voltage`` readings. In order to forward those variables into your TTN payload you would need to insert the given decoder.js code into your TTN App. In TTN console under Payload Formats switch to Custom and paste the Javascript from `decoder.js <https://github.com/hiveeyes/terkin-datalogger/blob/master/client/TTN/decoder.js>`_. The decoder function is backward compatible to the build-in CayenneLPP decoder.

***********
PutsReq.com
***********

`PutsReq.com <https://putsreq.com>`_ will serve as your HTTP endpoint in the `TTN HTTP integration <https://www.thethingsnetwork.org/docs/applications/http/>`_. It's a free service for inspecting and rewriting HTTP POST requests to a response that our data aquisition service (DAQ) at `swarm.hiveeyes.org <https://swarm.hiveeyes.org>`_ will be able to understand and process. An endpoint for common use is already set up and can be requested from @thiasB but you can of course set up your own endpoint and use the Javascript provided in `putsreq.com.js <https://github.com/hiveeyes/terkin-datalogger/blob/master/client/TTN/putsreq.com.js>`_ for the payload rewrite.

************
Telegram Bot
************

A Telegram bot for interactinhg with the device via LoRaWAN downlinks is available from the `telegram_terkin_ttn_bot.py <https://github.com/hiveeyes/terkin-datalogger/blob/master/client/TTN/telegram_terkin_ttn_bot.py>`_ file.

Currently these two capabilities are implemented:

-  ``/pause`` and ``/unpause`` for pausing and continuing the inclusion of sensor data into the payload, e.g for times when you are working on the bees hives
-  ``/sleep MIN`` for remotely setting the Deep Sleep interval in MIN minutes

Please see `Telegram bot documentation <https://core.telegram.org/bots>`_ for how to get started with a bot at first. An always on server under your control will be needed to run the bot. Remember that downlink messages to the device are not being sent immediately but always shortly after an uplink message has been successfully received by the network. 
