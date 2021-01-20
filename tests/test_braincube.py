# -*- coding: utf-8 -*-
"""Tests for the braincube module."""


import responses

from braincube_connector import braincube, parameters
from tests.mock import bc_obj, mock_client, mock_request_entity

MB_URL = "https://api.a.b/braincube/bcname/braincube/mb/{bcid}/extended"
MB_JSON = {"bcId": "1", "name": "abcd"}
NAME = "bcname1"


def test_path(bc_obj):
    assert bc_obj._path == "braincube/bcname"


def test_get_braincube(mock_client):
    bc = braincube.get_braincube(NAME)
    assert bc._name == NAME
    assert bc._bcid == NAME
    assert bc._product_id == "bc1"


def test_get_braincube_list(mock_client):
    bc_list = braincube.get_braincube_list()
    assert len(bc_list) == 2
    for i, bc in enumerate(bc_list):
        assert bc._name == "bcname{}".format(i + 1)
        assert bc._bcid == "bcname{}".format(i + 1)
        assert bc._product_id == "bc{}".format(i + 1)
    bc_list = braincube.get_braincube_list([NAME])
    assert bc_list[0]._name == NAME

    bc_list2 = braincube.get_braincube_list(["bcname1"])
    assert len(bc_list2) == 1
    assert bc_list2[0]._name == "bcname1"


@responses.activate
def test_get_memory_base(bc_obj, mock_client):
    responses.add(responses.GET, MB_URL.format(bcid="1"), json=MB_JSON, status=200)
    mb = bc_obj.get_memory_base("1")
    assert mb._name == "abcd"
    assert mb._path == "braincube/bcname/{webservice}/mb/1"


def test_get_memory_base_list(mocker, monkeypatch, bc_obj, mock_request_entity):
    parameters.set_parameter({"page_size": 2})
    mb_list = bc_obj.get_memory_base_list(page=10)
    mock_request_entity.assert_called_with(
        "braincube/bcname/braincube/mb/all/summary?offset=20&size=2"
    )


def test_get_uuid(bc_obj):
    assert bc_obj.get_uuid() == "id123"  # Id of the mock braincube
