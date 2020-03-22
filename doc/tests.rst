#######################
Terkin Datalogger Tests
#######################


*****
About
*****
- The Terkin Datalogger tests are executed within a ``pytest``
  environment on regular CPython 3.x.
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
::

    make setup-virtualenv3


*******
Operate
*******

Invoke::

    make test

Invoke, with log output::

    make test-verbose

Invoke specific tests, with markers::

    make test marker="esp32"

Invoke specific tests, with names::

    pytest test --capture=no -k test_basic_esp32
