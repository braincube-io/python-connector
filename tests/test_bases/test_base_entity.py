# -*- coding: utf-8 -*-

"""Tests for the bases module."""

import re
import responses

from py_client import parameters
from py_client.bases import base_entity
from tests.mock import entity_obj, mock_client, base_obj
import pytest


def test_create_base_entity(entity_obj):
    assert entity_obj._name == "entity"
    assert entity_obj._bcid == "id123"
    assert entity_obj._metadata == {"meta": 1}
    assert entity_obj._path == "path/id123"


def test_get_bcid(entity_obj):
    assert entity_obj.get_bcid() == "id123"


def test_entity_repr(entity_obj):
    assert re.search(r"<BaseEntity\(name=entity, id=id123\) at .*?>", repr(entity_obj),)


def test_get_metadata(entity_obj):
    assert entity_obj.get_metadata() == {"meta": 1}


def test_create_from_json():
    json_dict = {"bcId": "1", "name": "abcd"}
    obj = base_entity.BaseEntity.create_from_json(json_dict, "path/{bcid}")
    assert obj._name == "abcd"
    assert obj._bcid == "1"
    assert obj._path == "path/1"
    assert obj._metadata == json_dict


@responses.activate
def test_create_one_from_path(mock_client):
    json_data = {"name": "abcd", "bcId": "1"}
    responses.add(responses.GET, "https://api.a.b/braincube/path", json=json_data, status=200)
    entity = base_entity.BaseEntity.create_one_from_path(
        "{webservice}/path", "{webservice}/path/{bcid}"
    )
    assert entity._name == "abcd"
    assert entity._bcid == "1"
    assert entity._path == "{webservice}/path/1"


@pytest.mark.parametrize(
    "page, page_size, length, entity_name, call_params",
    [
        (0, 3, 3, "name2", ["?offset=0&size=3"]),
        (1, 2, 2, "name3", ["?offset=2&size=2"]),
        (-1, 2, 4, "name3", ["?offset=0&size=2", "?offset=2&size=2", "?offset=4&size=2"]),
    ],
)
def test_create_many_from_path(
    mock_client, monkeypatch, mocker, page, page_size, length, entity_name, call_params
):
    """Test create_many_from_path for different pagination settings"""
    items = [{"name": "name{}".format(i), "bcId": str(i)} for i in range(4)]

    def mock_request_ws(path):
        path, param = path.split("?")
        params = {key: int(val) for key, val in [pp.split("=") for pp in param.split("&")]}
        assert path == "braincube/path/all/summary"
        return {"items": items[params["offset"] : (params["offset"] + params["size"])]}

    rpatch = mocker.patch("py_client.client.request_ws", side_effect=mock_request_ws)
    parameters.set_parameter({"page_size": page_size})
    entities = base_entity.BaseEntity.create_many_from_path(
        "{webservice}/path/all/summary", "{webservice}/path/{bcid}", page=page
    )

    calls = [
        mocker.call("braincube/path/all/summary{param}".format(param=pp)) for pp in call_params
    ]
    rpatch.assert_has_calls(calls)
    assert len(entities) == length
    entities[-1]._name = entity_name
