# -*- coding: utf-8 -*-
"""Tests for the variable module."""

from py_client.memory_base.nested_resources import variable
from tests.mock import create_mock_var


def test_get_type(create_mock_var):
    var_obj = create_mock_var(type="TYPE")
    assert var_obj.get_type() == "TYPE"


def test_get_long_id(mocker, create_mock_var):
    mock_mb = mocker.Mock()
    mock_mb.get_bcid.return_value = "12"
    mock_var = create_mock_var(bcid="30", mb=mock_mb)
    assert mock_var.get_long_id() == "mb12/d30"
