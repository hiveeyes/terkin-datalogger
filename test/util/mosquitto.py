import os

import pytest
from pytest_docker_fixtures.containers._base import BaseImage


from pytest_docker_fixtures import images
"""
images.settings['mosquitto'] = {}
images.configure(
    'mosquitto',
    'eclipse-mosquitto', '1.6.8',
    env={},
    options={
        'ports': {
            '1883': '1883'
        }
    })
"""
images.settings['mosquitto'] = {
    'image': 'eclipse-mosquitto',
    'version': '1.6.8',
    'options': {
        'publish_all_ports': False,
        'ports': {
            f'1883/tcp': '1883'
        }
    }
}


class Mosquitto(BaseImage):

    name = 'mosquitto'

    def check(self):
        return True


mosquitto_image = Mosquitto()


@pytest.fixture(scope='session')
def mosquitto():
    if os.environ.get('MOSQUITTO'):
        yield os.environ['MOSQUITTO'].split(':')
    else:
        yield mosquitto_image.run()
        mosquitto_image.stop()
