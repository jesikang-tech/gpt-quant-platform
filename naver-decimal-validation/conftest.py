"""Network-denial guard for isolated synthetic NAVER tests.

This is a Python-level defense, not an OS network sandbox.
"""

import socket


def _network_denied(*args, **kwargs):
    raise RuntimeError("NETWORK_ACCESS_DENIED_IN_SYNTHETIC_TESTS")


def pytest_configure(config):
    socket.socket.connect = _network_denied
    socket.socket.connect_ex = _network_denied
    socket.create_connection = _network_denied
    socket.getaddrinfo = _network_denied