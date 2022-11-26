# -*- coding: utf-8 -*-
# (c) 2020 Richard Pobering <richard@hiveeyes.org>
# (c) 2020 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import json
import pytest
import requests
import werkzeug
from pytest_httpserver.pytest_plugin import Plugin, PluginHTTPServer


@pytest.mark.urequests
def test_urequests_basic(httpserver_ipv4):
    """
    A basic test showing that the "urequests" module works properly.
    """

    httpserver = httpserver_ipv4

    # Define HTTP conversation details.
    request_data = {'hello': 'world'}
    response_data = {'status': 'ok'}

    # Mock HTTP conversation.
    httpserver.expect_request("/api/data").respond_with_json(response_data)

    # Get URL to be invoked.
    url = httpserver.url_for("/api/data")

    # Invoke HTTP request.
    import urequests
    response = urequests.post(url, json=request_data)

    # Proof that worked.

    # Investigate the real response.
    assert response.content == json.dumps(response_data, indent=4).encode()

    # Investigate within the HTTP server.
    assert len(httpserver.log) == 1, "pytest-httpserver didn't capture any request"
    request, response = httpserver.log[0]
    assert request.get_data() == json.dumps(request_data).encode()


@pytest.mark.urequests
def test_redirect_cpython_requests(httpserver_ipv4):
    """
    Proof that HTTP redirects work.

    This is the reference implementation using the CPython "requests" module.
    """

    httpserver = httpserver_ipv4

    # Define HTTP conversation details.
    request_data = {'hello': 'world'}
    response_data = {'status': 'ok'}

    # Mock HTTP conversation.
    def handler(request: werkzeug.Request):
        response = werkzeug.Response(status=307)
        response.headers.add('Location', '/api/v2/data')
        return response

    httpserver.expect_request("/api/v1/data").respond_with_handler(handler)
    httpserver.expect_request("/api/v2/data").respond_with_json(response_data)

    # Get URL to be invoked.
    url = httpserver.url_for("/api/v1/data")

    # Invoke HTTP request.
    requests.post(url, json=request_data)

    # Proof that worked.
    request, response = httpserver.log[0]
    assert request.get_data() == json.dumps(request_data).encode()
    assert response.status_code == 307
    assert response.get_data() == b''

    request, response = httpserver.log[1]
    assert request.get_data() == json.dumps(request_data).encode()
    assert response.status_code == 200
    assert response.get_data() == json.dumps(response_data, indent=4).encode()


@pytest.mark.urequests
def test_redirect_urequests(httpserver_ipv4):
    """
    Proof that HTTP redirects work, now based on urequests.
    """

    httpserver = httpserver_ipv4

    # Define HTTP conversation details.
    request_data = {'hello': 'world'}
    response_data = {'status': 'ok'}

    # Mock HTTP conversation.
    def handler(request: werkzeug.Request):
        response = werkzeug.Response(status=307)
        response.headers.add('Location', '/api/v2/data')
        return response

    httpserver.expect_request("/api/v1/data").respond_with_handler(handler)
    httpserver.expect_request("/api/v2/data").respond_with_json(response_data)

    # Get URL to be invoked.
    url = httpserver.url_for("/api/v1/data")
    print("\nurl:", url)

    # Invoke HTTP request.
    import urequests
    response = urequests.post(url, json=request_data)

    # Proof that worked.

    # Investigate the real response.
    assert response.content == json.dumps(response_data, indent=4).encode()

    # Investigate within the HTTP server.
    request, response = httpserver.log[0]
    assert request.get_data() == json.dumps(request_data).encode()
    assert response.status_code == 307
    assert response.get_data() == b''

    request, response = httpserver.log[1]
    assert request.get_data() == json.dumps(request_data).encode()
    assert response.status_code == 200
    assert response.get_data() == json.dumps(response_data, indent=4).encode()
