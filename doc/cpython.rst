#############################
How to run Terkin on CPython?
#############################

Acquire 3rd-party packages::

    make setup
    rm -r dist-packages/collections dist-packages/types.py

Tests::

    make setup-tests
    apt-get install mosquitto
    make test

Invoke::

    # Create configuration.
    cp src/settings.example.py src/settings.py

    # Run src/main_cpython.py.
    make install-cpython
    make run-cpython
