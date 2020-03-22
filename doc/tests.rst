#######################
Terkin Datalogger Tests
#######################


*****
About
*****
- The Terkin Datalogger tests suite is executed within
  a ``pytest`` environment on regular CPython 3.x.
- The environment provides a fake filesystem and other
  infrastructure to invoke integration tests.
- Docker is used to spin up infrastructure services
  like Mosquitto in the background.


*****
Setup
*****

==============
Install Docker
==============
- https://docs.docker.com/install/linux/docker-ce/debian/
- https://docs.docker.com/docker-for-mac/install/
- https://docs.docker.com/docker-for-windows/wsl-tech-preview/

===================
Install environment
===================
Install 3rd-party MicroPython modules::

    make setup

Install pytest modules and addons::

    make setup-tests


*******
Operate
*******

=====
Basic
=====
Invoke whole test suite::

    make test

Invoke specific tests, with markers::

    make test marker="esp32"

With log output::

    make test-verbose

With coverage report::

    make test-coverage

========
Advanced
========
Prepare::

    source .venv3/bin/activate

Invoke specific tests, with names::

    pytest test --capture=no -k test_basic_esp32

Display detailed coverage report::

    coverage report --show-missing
