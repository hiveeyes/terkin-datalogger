#########################
Running Terkin on CPython
#########################


*************
Prerequisites
*************
::

    apt-get install git python-virtualenv python3-virtualenv
    git clone https://github.com/hiveeyes/terkin-datalogger.git
    cd terkin-datalogger

Acquire 3rd-party packages::

    make setup
    make setup-tests
    make setup-cpython
    make setup-raspberrypi
    make setup-gpsd

Some adjustments::

    rm -r dist-packages/collections dist-packages/types.py


*************
Configuration
*************
Create configuration from blueprint::

    cp src/settings.raspberrypi.py src/settings.py


***
Run
***
Invoke ``src/main_cpython.py``::

    make run-cpython
