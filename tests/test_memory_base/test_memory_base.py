# -*- coding: utf-8 -*-
"""Tests for the memory_base module."""

import responses
from braincube_connector import parameters
from braincube_connector.memory_base import memory_base

from tests.mock import mb_obj, mock_client, mock_request_entity

import pytest

VD_URL = "https://api.a.b/braincube/bcname/braincube/mb/1/variables/{var_id}/extended"
JOB_URL = "https://api.a.b/braincube/bcname/braincube/mb/1/jobs/{job_id}/extended"
DG_URL = "https://api.a.b/braincube/bcname/braincube/mb/1/dataGroups/{group_id}/extended"
EVENT_URL = "https://api.a.b/braincube/bcname/braincube/mb/1/events/{event_id}/extended"
RULE_URL = "https://api.a.b/braincube/bcname/braincube/mb/1/rules/{event_id}/summary"

ID1 = "1"
NAME = "abcd"
VD_JSON = {"bcId": ID1, "standard": NAME}
BASIC_JSON = {"bcId": ID1, "name": NAME}


@responses.activate
def test_get_variable(mb_obj, mock_client):
    responses.add(responses.GET, VD_URL.format(var_id=ID1), json=VD_JSON, status=200)
    var = mb_obj.get_variable(ID1)
    assert var._name == NAME
    assert var._path == "braincube/bcname/{webservice}/mb/1/variables/1"


@responses.activate
def test_get_variable_list(mocker, monkeypatch, mb_obj, mock_request_entity):
    mock_request_entity.return_value = {
        "items": [{"standard": "name{}".format(i), "bcId": str(i)} for i in range(3)]
    }
    parameters.set_parameter({"page_size": 2})
    var_list = mb_obj.get_variable_list(page=0)
    assert var_list[0]._name == "name0"

    request_path = "braincube/bcname/braincube/mb/1/variables/summary?offset=0&size=2"
    mock_request_entity.assert_called_with(request_path)
    mock_request_entity.reset_mock()
    parameters.set_parameter({"page_size": 4})
    var_list = mb_obj.get_variable_list(page=0, page_size=2)
    mock_request_entity.assert_called_with(request_path)


@responses.activate
def test_get_job(mb_obj, mock_client):
    responses.add(responses.GET, JOB_URL.format(job_id=ID1), json=BASIC_JSON, status=200)
    job = mb_obj.get_job(ID1)
    assert job._name == NAME
    assert job._path == "braincube/bcname/{webservice}/mb/1/jobs/1"


@responses.activate
def test_get_job_list(mocker, monkeypatch, mb_obj, mock_request_entity):
    parameters.set_parameter({"page_size": 2})
    job_list = mb_obj.get_job_list(page=0)
    assert job_list[0]._name == "name0"
    request_path = "braincube/bcname/braincube/mb/1/jobs/all/summary?offset=0&size=2"
    mock_request_entity.assert_called_with(request_path)
    mock_request_entity.reset_mock()
    parameters.set_parameter({"page_size": 4})
    job_list = mb_obj.get_job_list(page=0, page_size=2)
    mock_request_entity.assert_called_with(request_path)


@responses.activate
def test_get_datagroup(mb_obj, mock_client):
    responses.add(responses.GET, DG_URL.format(group_id=ID1), json=BASIC_JSON, status=200)
    group = mb_obj.get_datagroup(ID1)
    assert group._name == NAME
    assert group._path == "braincube/bcname/{webservice}/mb/1/dataGroups/1"


@responses.activate
def test_get_datagroup_list(mocker, monkeypatch, mb_obj, mock_request_entity):
    parameters.set_parameter({"page_size": 2})
    group_list = mb_obj.get_datagroup_list(page=0)
    assert group_list[0]._name == "name0"
    request_path = "braincube/bcname/braincube/mb/1/dataGroups/summary?offset=0&size=2"
    mock_request_entity.assert_called_with(request_path)
    mock_request_entity.reset_mock()
    parameters.set_parameter({"page_size": 4})
    group_list = mb_obj.get_datagroup_list(page=0, page_size=2)
    mock_request_entity.assert_called_with(request_path)


@responses.activate
def test_get_event(mb_obj, mock_client):
    responses.add(responses.GET, EVENT_URL.format(event_id=ID1), json=BASIC_JSON, status=200)
    event = mb_obj.get_event(ID1)
    assert event._name == NAME
    assert event._path == "braincube/bcname/{webservice}/mb/1/events/1"


@responses.activate
def test_get_events_list(mocker, monkeypatch, mb_obj, mock_request_entity):
    parameters.set_parameter({"page_size": 2})
    event_list = mb_obj.get_event_list(page=0)
    assert event_list[0]._name == "name0"
    request_path = "braincube/bcname/braincube/mb/1/events/all/extended?offset=0&size=2"
    mock_request_entity.assert_called_with(request_path)
    mock_request_entity.reset_mock()
    parameters.set_parameter({"page_size": 4})
    event_list = mb_obj.get_event_list(page=0, page_size=2)
    mock_request_entity.assert_called_with(request_path)


@responses.activate
def test_rule_event(mb_obj, mock_client):
    responses.add(responses.GET, RULE_URL.format(event_id=ID1), json=BASIC_JSON, status=200)
    rule = mb_obj.get_rule(ID1)
    assert rule._name == NAME
    assert rule._path == "braincube/bcname/{webservice}/mb/1/rules/1"


@responses.activate
def test_get_rule_list(mocker, monkeypatch, mb_obj, mock_request_entity):
    parameters.set_parameter({"page_size": 2})
    rule_list = mb_obj.get_rule_list(page=0)
    assert rule_list[0]._name == "name0"
    request_path = "braincube/bcname/braincube/mb/1/rules/all/selector?offset=0&size=2"
    mock_request_entity.assert_called_with(request_path)
    mock_request_entity.reset_mock()
    parameters.set_parameter({"page_size": 4})
    rule_list = mb_obj.get_rule_list(page=0, page_size=2)
    mock_request_entity.assert_called_with(request_path)


def test_get_data(mocker, mb_obj):
    mock_collect = mocker.patch("braincube_connector.data.data.collect_data")
    var_ids = ["1", "2"]
    filters = ["A"]
    mb_obj.get_data(var_ids, filters)
    mock_collect.assert_called_with(var_ids, "braincube/bcname/", mb_obj._metadata, filters)
    NotImplemented
