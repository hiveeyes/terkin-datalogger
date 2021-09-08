# -*- coding: utf-8 -*-
# (c) 2020 Richard Pobering <richard@hiveeyes.org>
# (c) 2020 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import os
import socket
import pytest
from pytest_docker_fixtures.containers._base import BaseImage


from pytest_docker_fixtures import images
images.settings['mosquitto'] = {
    'image': 'eclipse-mosquitto',
    'version': '2.0.11',
    'options': {
        'command': 'mosquitto -c /mosquitto-no-auth.conf',
        'publish_all_ports': False,
        'ports': {
            f'1883/tcp': '1883'
        }
    },
}


class Mosquitto(BaseImage):

    name = 'mosquitto'

    def check(self):
        return True


mosquitto_image = Mosquitto()


def is_port_reachable(host, port):
    """
    Test if a host is up.
    https://github.com/lovelysystems/lovely.testlayers/blob/0.7.0/src/lovely/testlayers/util.py#L6-L13
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ex = s.connect_ex((host, port))
    if ex == 0:
        s.close()
        return True
    return False


def is_mosquitto_running():
    return is_port_reachable('localhost', 1883)


@pytest.fixture(scope='session')
def mosquitto():

    # Gracefully skip spinning up the Docker container if Mosquitto is already running.
    if is_mosquitto_running():
        yield
        return

    # Spin up Mosquitto container.
    if os.environ.get('MOSQUITTO'):
        yield os.environ['MOSQUITTO'].split(':')
    else:
        yield mosquitto_image.run()
        mosquitto_image.stop()
