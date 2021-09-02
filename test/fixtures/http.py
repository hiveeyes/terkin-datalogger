import pytest
from pytest_httpserver.pytest_plugin import Plugin, PluginHTTPServer


@pytest.fixture()
def httpserver_ipv4():

    if Plugin.SERVER:
        Plugin.SERVER.clear()
        yield Plugin.SERVER
        return

    server = PluginHTTPServer(host='127.0.0.1', port=8888)
    server.start()
    #time.sleep(0.1)
    yield server
    server.stop()
