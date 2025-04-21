"""
Test the envoy.client module including the Client class and related helper functions.
"""

import pytest

from envoy.client import *


@pytest.mark.parametrize(
    "host,endpoint,query,expected",
    [
        ("trenvoy.io", "transactions", None, "https://trenvoy.io/v1/transactions"),
        (
            "trenvoy.io",
            "transactions",
            {"page": 42},
            "https://trenvoy.io/v1/transactions?page=42",
        ),
        ("trenvoy.io", "", None, "https://trenvoy.io/v1/"),
        (
            "trenvoy.io",
            ("users", "bob"),
            {"filter": "simple"},
            "https://trenvoy.io/v1/users/bob?filter=simple",
        ),
    ],
)
def test_make_endpoint(host, endpoint, query, expected):
    client = Client(host)
    if isinstance(endpoint, str):
        endpoint = (endpoint,)

    assert expected == client._make_endpoint(*endpoint, params=query)


@pytest.mark.parametrize(
    "arg,expected",
    [
        ("", ""),
        ("https://charlie.vaspbot.com", "charlie.vaspbot.com"),
        ("charlie.vaspbot.com", "charlie.vaspbot.com"),
        ("https://charlie.vaspbot.com/v1", "charlie.vaspbot.com"),
        ("charlie.vaspbot.com/v1", "charlie.vaspbot.com"),
        ("http://envoy.local:8000", "envoy.local:8000"),
        ("http://envoy.local:8000/v1", "envoy.local:8000"),
    ],
)
def test_parse_url_host(arg, expected):
    assert parse_url_host(arg) == expected


@pytest.mark.parametrize(
    "mime,expected",
    [
        ("application/json", "application/json"),
        ("application/json; charset=utf-8", "application/json"),
    ],
)
def test_parse_content_type(mime, expected):
    actual, _ = parse_content_type(mime)
    assert actual == expected
