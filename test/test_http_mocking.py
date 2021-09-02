# -*- coding: utf-8 -*-
# (c) 2020 Richard Pobering <richard@hiveeyes.org>
# (c) 2020 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import time
import json
import socket

import pytest
import requests
import httpretty
from mocket import mocketize, Mocket
from mocket.mockhttp import Entry
from urllib.parse import urlparse, splitport
from pytest_httpserver.pytest_plugin import Plugin, PluginHTTPServer


@mocketize
@pytest.mark.httpmock
def test_mocket_cpython_requests():
    """
    Using the ``requests`` module works perfectly.
    """

    # Define HTTP request details.
    url = 'http://127.0.0.1/api/data'
    data = {'hello': 'world'}

    # Mock HTTP conversation.
    Entry.single_register(Entry.POST, url)

    # Invoke HTTP request.
    requests.post(url, json=data)

    # Proof that worked.
    assert Mocket.last_request().body == json.dumps(data)


@mocketize
@pytest.mark.httpmock
@pytest.mark.xfail(raises=ValueError)
def test_mocket_socket():
    """
    Demonstrate HTTP streaming to Mocket's "mockhttp".

    The error is::

        self = <mocket.mockhttp.Request object at 0x108cf74c0>, data = b'POST /api/data HTTP/1.0\r\n'

            def __init__(self, data):
        >       _, self.body = decode_from_bytes(data).split('\r\n\r\n', 1)
        E       ValueError: not enough values to unpack (expected 2, got 1)

        .venv/lib/python3.8/site-packages/mocket/mockhttp.py:23: ValueError

    The reason is that ``data`` is essentially::

        b'POST /api/data HTTP/1.0\r\n'

    which well fails on being split by ``\r\n\r\n`` appropriately.
    So, when receiving a streamed response, Mocket's "mockhttp"
    should not expect the data to be sent en bloc.
    """

    # Define HTTP request details.
    method = 'POST'
    url = 'http://127.0.0.1/api/data'
    data = {'hello': 'world'}

    # Mock HTTP conversation.
    Entry.single_register(Entry.POST, url)

    # Invoke HTTP request.
    send_request(url, method, json=data)

    # Proof that worked.
    assert Mocket.last_request().body == json.dumps(data)


@httpretty.activate
@pytest.mark.httpmock
def test_httpretty_cpython_requests():
    """
    Using the ``requests`` module works perfectly.
    """

    # Define HTTP request details.
    url = 'http://127.0.0.1/api/data'
    data = {'hello': 'world'}

    # Mock HTTP conversation.
    httpretty.register_uri(
        httpretty.POST,
        url,
        body=json.dumps({'status': 'ok'})
    )

    # Invoke HTTP request.
    response = requests.post(url, json=data)

    # Proof everything is in place.

    # Check response.
    assert response.json() == {'status': 'ok'}

    # Check request.
    assert len(httpretty.latest_requests()) == 1
    assert httpretty.last_request() == httpretty.latest_requests()[0]
    assert httpretty.last_request().body == json.dumps(data).encode()


@httpretty.activate
@pytest.mark.httpmock
@pytest.mark.xfail(raises=RuntimeError)
def test_httpretty_socket():
    """
    Using raw sockets will also fail with ``httpretty``.
    """

    # Define HTTP request details.
    method = 'POST'
    url = 'http://127.0.0.1/api/data'
    data = {'hello': 'world'}

    # Mock HTTP conversation.
    httpretty.register_uri(
        httpretty.POST,
        url,
        body=json.dumps({'status': 'ok'})
    )

    # Invoke HTTP request.
    send_request(url, method, json=data)

    # Proof everything is in place.

    # Check response.
    #assert response.json() == {'status': 'ok'}

    # Check request.
    assert len(httpretty.latest_requests()) == 1
    assert httpretty.last_request() == httpretty.latest_requests()[0]
    assert httpretty.last_request().body == json.dumps(data).encode()


@pytest.mark.httpmock
def test_httpserver_cpython_requests(httpserver_ipv4):
    """
    Using the ``requests`` module works perfectly.
    """

    httpserver = httpserver_ipv4

    # Define HTTP conversation details.
    request_data = {'hello': 'world'}
    response_data = {'status': 'ok'}

    # Mock HTTP conversation.
    httpserver.expect_request("/api/data").respond_with_json(response_data)

    # Invoke HTTP request.
    url = httpserver.url_for("/api/data")
    requests.post(url, json=request_data)

    # Proof that worked.
    request, response = httpserver.log[0]
    assert request.get_data() == json.dumps(request_data).encode()
    assert response.get_data() == json.dumps(response_data, indent=4).encode()


@pytest.mark.httpmock
def test_httpserver_socket(httpserver_ipv4):
    """
    This works better, but occasionally still fails with::

        AssertionError: pytest-httpserver didn't capture any request
    """

    httpserver = httpserver_ipv4

    # Define HTTP request details.
    method = 'POST'
    data = {'hello': 'world'}

    # Mock HTTP conversation.
    httpserver.expect_request("/api/data").respond_with_json({'status': 'ok'})

    # Invoke HTTP request.
    url = httpserver.url_for("/api/data")
    send_request(url, method, json=data)

    time.sleep(0.2)

    # Proof that worked.
    assert len(httpserver.log) == 1, "pytest-httpserver didn't capture any request"
    request, response = httpserver.log[0]
    assert request.get_data() == json.dumps(data).encode()


def send_request(url, method, data=None, json=None):

    #socket.setdefaulttimeout(2.0)

    uri = urlparse(url)
    host, port = splitport(uri.netloc)
    port = port or 80
    path = uri.path

    address = socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM)[0]
    sock = socket.socket(address[0], address[1], address[2])
    sock.connect(address[-1])

    if json is not None:
        import json as json_module
        data = json_module.dumps(json)

    method = method.encode()
    host = host.encode()
    path = path.encode()
    data = data.encode()

    sock.send(b"%s %s HTTP/1.0\r\n" % (method, path))
    sock.send(b"Host: %s\r\n" % host)
    sock.send(b"Content-Type: application/json\r\n")
    sock.send(b"Content-Length: %d\r\n" % len(data))
    sock.send(b"Connection: close\r\n\r\n")
    sock.send(data)


def send_request_stream(url, method, data):

    uri = urlparse(url)
    host, port = splitport(uri.netloc)
    port = port or 80
    path = uri.path

    address = socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM)[0]
    sock = socket.socket(address[0], address[1], address[2])
    sock.connect(address[-1])

    method = method.encode()
    host = host.encode()
    path = path.encode()
    data = data.encode()

    sock.makefile(mode='rwb')
    sock.write(b"%s %s HTTP/1.0\r\n" % (method, path))
    sock.write(b"Host: %s\r\n" % host)
    sock.write(b"Content-Type: application/json\r\n")
    sock.write(b"Content-Length: %d\r\n" % len(data))
    sock.write(b"Connection: close\r\n\r\n")
    sock.write(data)
