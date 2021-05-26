# -*- coding: utf-8 -*-

"""Mock the braindata and braincube webservice server."""
import math
from datetime import datetime

import pytest
import responses

available_calls = [
    {
        "method": "GET",
        "url": "https://test.com/sso-server/ws/user/me",
        "status": 200,
        "json": {
            "accessList": [
                {"product": {"name": "demo", "productId": "123"},},
                {"product": {"name": "other", "productId": "456"},},
            ]
        },
    },
    {
        "method": "GET",
        "url": "https://api.test.com/braincube/demo/braincube/mb/1/variables/0/extended",
        "status": 200,
        "json": {"bcId": 0, "tag": "tag_name", "local": "local_name", "standard": "standard_name"},
    },
    {
        "method": "GET",
        "url": "https://api.test.com/braincube/demo/braincube/mb/all/summary?offset=0&size=150",
        "status": 200,
        "json": {"items": [{"name": "mb1", "bcId": 1,}, {"name": "mb2", "bcId": 2,},]},
    },
    {
        "method": "GET",
        "url": "https://api.test.com/braincube/demo/braincube/mb/all/summary?offset=150&size=150",
        "status": 200,
        "json": {"items": []},
    },
    {
        "method": "GET",
        "url": "https://api.test.com/braincube/demo/braincube/mb/1/extended",
        "status": 200,
        "json": {"referenceDateVariable": {"bcId": 101, "id": 101}, "name": "mb1", "bcId": 1,},
    },
    {
        "method": "GET",
        "url": "https://api.test.com/braincube/demo/braindata/mb1/simple",
        "status": 200,
        "json": {"name": "mb1", "order": "mb1/d101",},
    },
    {
        "method": "POST",
        "url": "https://api.test.com/braincube/demo/braindata/mb1/LF",
        "status": 200,
        "json": {
            "datadefs": [
                {
                    "data": ["20201127_124000", "20201127_124001", "null", "20201127_124002"],
                    "id": "mb1/d101",
                    "type": "DATETIME",
                },
                {"data": ["1.1", "1.2", "nan", "1.4"], "id": "mb1/d102", "type": "NUMERIC"},
                {"data": ["A", "B", "NaN", "D"], "id": "mb1/d103", "type": "NUMERICAL"},
            ]
        },
    },
]

custom_calls = [
    {
        "method": "GET",
        "url": "http://another.plop.com/sso-server/ws/user/me",
        "status": 200,
        "json": {
            "accessList": [
                {"product": {"name": "demo", "productId": "123"},},
                {"product": {"name": "other", "productId": "456"},},
            ]
        },
    },
    {
        "method": "GET",
        "url": "http://braincube_api.plop.com/prefix/v1.0/braincube/demo/braincube/mb/1/extended",
        "status": 200,
        "json": {"referenceDateVariable": {"bcId": 101, "id": 101}, "name": "mb1", "bcId": 1,},
    },
    # Expected call for test_memorybase_with_custom_domains_and_placeholder
    {
        "method": "GET",
        "url": "http://demo.plop.com/prefix/v1.0/braincube/mb/1/extended",
        "status": 200,
        "json": {"referenceDateVariable": {"bcId": 101, "id": 101}, "name": "mb1", "bcId": 1,},
    },
    {
        "method": "GET",
        "url": "http://demo.plop.com/prefix/v1.0/braincube/mb/1/variables/summary?offset=0&size=150",
        "status": 200,
        "json": {"items": [],},
    },
]

for bcid in ["101", "102", "103"]:
    available_calls.append(
        {
            "method": "GET",
            "url": "https://api.test.com/braincube/demo/braincube/mb/1/variables/{0}/extended".format(
                bcid
            ),
            "status": 200,
            "json": {
                "bcId": bcid,
                "tag": "tag_{0}".format(bcid),
                "local": "local_{0}".format(bcid),
                "standard": "standard_{0}".format(bcid),
            },
        }
    )


@pytest.fixture
def patch_endpoints():
    def func():
        for kwargs in available_calls:
            responses.add(**kwargs)

    return func


@pytest.fixture
def custom_patch_endpoints():
    def func():
        for kwargs in custom_calls:
            responses.add(**kwargs)

    return func
