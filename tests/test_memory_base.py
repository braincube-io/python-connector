# -*- coding: utf-8 -*-
"""Tests for the memory_base module."""

import responses
from py_client import parameters

from tests.mock import mb_obj, mock_client, mock_request_entity

VD_URL = "https://api.a.b/braincube/bcname/braincube/mb/1/variables/{var_id}/extended"
JOB_URL = "https://api.a.b/braincube/bcname/braincube/mb/1/jobs/{job_id}/extended"

ID1 = "1"
NAME = "abcd"
VD_JSON = {"bcId": ID1, "standard": NAME}
JOB_JSON = {"bcId": ID1, "name": NAME}


@responses.activate
def test_get_variable(mb_obj, mock_client):
    responses.add(responses.GET, VD_URL.format(var_id=ID1), json=VD_JSON, status=200)
    var = mb_obj.get_variable(ID1)
    assert var._name == NAME
    assert var._path == "braincube/bcname/braincube/mb/1/variables/1"


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
    responses.add(responses.GET, JOB_URL.format(job_id=ID1), json=JOB_JSON, status=200)
    job = mb_obj.get_job(ID1)
    assert job._name == NAME
    assert job._path == "braincube/bcname/braincube/mb/1/jobs/1"


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
