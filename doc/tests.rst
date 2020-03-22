#######################
Terkin Datalogger Tests
#######################

Invoke::

    make test

Invoke, with log output::

    make test-verbose

Invoke specific tests, with markers::

    make test marker="esp32"

Invoke specific tests, with names::

    pytest test --capture=no -k test_basic_esp32
