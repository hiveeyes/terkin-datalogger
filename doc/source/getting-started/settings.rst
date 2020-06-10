########
Settings
########


************
Introduction
************
The main Terkin Datalogger configuration is represented through
the ``settings.py`` file located in the root directory of the device.

The configuration settings from the user-specific configuration
file ``settings-user.json`` will be merged into this to yield
the configuration settings effective at runtime.


********************
Static configuration
********************
You are free to manipulate the ``settings.py`` and ``settings-user.json``
files in any way. Respective blueprints for both files can be found inside
the ``src/`` directory of this repository.


*********************
Runtime configuration
*********************
Configuration settings can be set at runtime.

By code::

    self.settings['main.interval.field'] = 42.42

By HTTP::

    echo 42.42 | http PUT "http://$(cat .terkin/floatip)/api/v1/setting?name=main.interval.field"
