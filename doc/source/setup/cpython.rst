################
Setup on CPython
################


*************
Prerequisites
*************
::

    apt-get install python3


*******
Install
*******
::

    pip install --user terkin

When installing on SBC machines like the Raspberry Pi, you might want
to install Terkin along with additional modules::

    pip install --user terkin[sbc,lorawan]


*************
Configuration
*************
Create configuration from blueprint::

    wget https://raw.githubusercontent.com/hiveeyes/terkin-datalogger/master/src/settings.raspberrypi.py


***
Run
***
Invoke::

    terkin --config settings.raspberrypi.py
