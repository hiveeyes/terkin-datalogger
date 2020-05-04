#######################
Setup Terkin on CPython
#######################


*************
Prerequisites
*************
::

    apt-get install git python-virtualenv python3-virtualenv
    virtualenv --python=python3 .venv3
    source .venv3/bin/activate


*******
Install
*******
::

    pip install terkin

When installing on SBC machines like the Raspberry Pi, you might want
to install Terkin along with additional modules::

    pip install terkin[sbc,lorawan]


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
