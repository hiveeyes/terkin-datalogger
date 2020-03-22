#######################
Terkin Datalogger Tests
#######################

Invoke::

    make test

Invoke, with log output::

    pytest test --verbose --capture=no

Invoke specific tests::

    pytest test --capture=no -k test_basic_esp32
