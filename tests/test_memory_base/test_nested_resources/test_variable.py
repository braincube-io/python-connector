# -*- coding: utf-8 -*-
"""Tests for the variable module."""
from braincube_connector import parameters
from tests.mock import create_mock_var

import pytest


def test_get_type(create_mock_var):
    var_obj = create_mock_var(metadata={"type": "TYPE"})
    assert var_obj.get_type() == "TYPE"


def test_get_long_id(mocker, create_mock_var):
    mock_mb = mocker.Mock()
    mock_mb.get_bcid.return_value = "12"
    mock_var = create_mock_var(bcid="30", mb=mock_mb)
    assert mock_var.get_long_id() == "mb12/d30"


def test_get_name(mocker, create_mock_var):
    mocker.patch(
        "braincube_connector.instances.instances", {"parameter_set": {}}
    )  # Uses a temporary instance for the test.
    var = create_mock_var(name="any", metadata={"standard": "name_standard", "tag": "name_tag"})
    assert var.get_name() == "name_standard"
    parameters.set_parameter({"VariableDescription_name_key": "tag"})
    assert var.get_name() == "name_tag"


def test_get_uuid(mocker, create_mock_var):
    mock_mb = mocker.Mock()
    mock_mb.get_bcid.return_value = "12"
    mock_var = create_mock_var(bcid="30", mb=mock_mb)
    with pytest.warns(UserWarning):
        uuid = mock_var.get_uuid()
    assert uuid == "mb12/d30"
