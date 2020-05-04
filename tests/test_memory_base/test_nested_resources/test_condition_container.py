# -*- coding: utf-8 -*-

"""Tests for the mb_child module."""

from py_client.memory_base.nested_resources import condition_container
from tests.mock import create_mock_var


def test_get_conditions(mocker, create_mock_var):
    mock_mb = mocker.Mock()
    mock_mb.get_bcid.return_value = "1"
    var_mocks = [
        create_mock_var(bcid=str(var_ind), type=var_type, mb=mock_mb)
        for var_ind, var_type in [(0, "NUMERIC"), (1, "NUMERIC"), (2, "DISCRETE")]
    ]
    mock_mb.get_variable.side_effect = lambda bcid: var_mocks[int(bcid)]
    metadata = {
        "conditions": [
            {"minimum": 0, "maximum": 10, "variable": {"bcId": "0"}, "positive": True},
            {"minimum": None, "maximum": None, "variable": {"bcId": "1"}, "positive": True},
            {"modalities": ["A"], "variable": {"bcId": "2"}, "positive": False},
        ]
    }
    entity = condition_container.ConditionContainer()
    entity._metadata = metadata
    entity._memory_base = mock_mb
    # condition_container.ConditionContainer("53", "entity", metadata, "path/mb/1/entity/53", mock_mb)
    filters = entity.get_conditions()
    assert filters == [{"BETWEEN": ["mb1/d0", 0, 10]}, {"NOT": [{"EQUALS": ["mb1/d2", ["A"]]}]}]
    entity._metadata = {}
    assert entity.get_conditions() == []
