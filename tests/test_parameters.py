# -*- coding: utf-8 -*-

"""Tests for the data module."""

from py_client import parameters
from py_client import instances


def test_set_parameters(mocker):
    mocker.patch.dict("py_client.instances.instances", {"parameter_set": {}})
    parameters.set_parameter({"page_size": 30})
    assert instances.get_instance("parameter_set")["page_size"] == 30


def test_get_parameters(mocker):
    mocker.patch.dict("py_client.parameters._default_parameters", {"page_size": 8})
    mocker.patch.dict("py_client.instances.instances", {"parameter_set": {}})
    assert parameters.get_parameter("page_size") == 8
    parameters.set_parameter({"page_size": 5})
    assert parameters.get_parameter("page_size") == 5
    assert instances.instances["parameter_set"]["page_size"] == 5


def test_reset(mocker):
    mocker.patch.dict("py_client.parameters._default_parameters", {"page_size": 8})
    mocker.patch.dict("py_client.instances.instances", {"parameter_set": {}})
    parameters.set_parameter({"page_size": 5})
    parameters.reset_parameter()
    assert parameters.get_parameter("page_size") == 8
    assert instances.instances["parameter_set"] == {}
