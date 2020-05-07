# -*- coding: utf-8 -*-
"""Tests for the datagroup module."""

from tests.mock import create_mock_datagroup


def test_get_variable_ids(create_mock_datagroup):
    variables = [str(i) for i in range(3)]
    dgroup = create_mock_datagroup(variables=variables)
    assert dgroup.get_variable_ids() == variables


def test_get_variable_list(mocker, create_mock_datagroup):
    variables = [str(i) for i in range(3)]
    expected_variables = ["Variable{}".format(var) for var in variables]
    mock_mb = mocker.Mock()
    mock_mb.get_variable.side_effect = lambda var_id: "Variable{}".format(var_id)
    dgroup = create_mock_datagroup(variables=variables, mb=mock_mb)
    assert dgroup.get_variable_list() == expected_variables


def test_get_data(mocker, create_mock_datagroup):
    variables = [str(i) for i in range(3)]
    mock_mb = mocker.Mock()
    dgroup = create_mock_datagroup(variables=variables, mb=mock_mb)
    filters = ["A", "B"]
    dgroup.get_data(filters)
    mock_mb.get_data.assert_called_once_with(variables, filters)
