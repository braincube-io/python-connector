# -*- coding: utf-8 -*-

"""Tests for the conditions module."""

from braincube_connector.data import conditions
from braincube_connector.memory_base.nested_resources import mb_child
from datetime import datetime, timezone
import pytest


@pytest.fixture
def create_mock_var(mocker):
    def create_mock(long_id, var_type="ANY"):
        var = mocker.Mock()
        var.get_long_id.return_value = long_id
        var.get_type.return_value = var_type
        return var

    return create_mock


@pytest.mark.parametrize(
    "filter_list, combined_filters",
    [
        ([], []),
        (None, []),
        (["condA"], ["condA"]),
        (["condA", "condB"], [{"AND": ["condA", "condB"]}]),
        (
            ["condA", "condB", "condC", "condD"],
            [{"AND": [{"AND": [{"AND": ["condA", "condB"]}, "condC"]}, "condD"]}],
        ),
    ],
)
def test_combine_filters(filter_list, combined_filters):
    assert conditions.combine_filters(filter_list) == combined_filters


def test_discrete_filter(mocker, create_mock_var):
    var_mock = create_mock_var("mb1/d1")
    cond = {"modalities": ["A", "B", "C"]}
    assert conditions._discrete_filter(var_mock, cond) == {
        "OR": [
            {"OR": [{"EQUALS": ["mb1/d1", ["A"]]}, {"EQUALS": ["mb1/d1", ["B"]]}]},
            {"EQUALS": ["mb1/d1", ["C"]]},
        ]
    }
    assert conditions._discrete_filter(var_mock, {}) is None


@pytest.mark.parametrize(
    "var_cond, var_type, filter",
    [
        ({"minimum": 0, "maximum": 10}, "NUMERIC", {"BETWEEN": ["mb1/d1", 0, 10]}),
        ({"minimum": None, "maximum": 10}, "NUMERIC", {"LESS": ["mb1/d1", 10]}),
        ({"minimum": 0, "maximum": None}, "NUMERIC", {"GREAT": ["mb1/d1", 0]}),
        ({"minimum": None, "maximum": None}, "DATETIME", None),
        (
            {
                "minimum": datetime(2020, 4, 22, 10, 45, tzinfo=timezone.utc).timestamp() * 1000,
                "maximum": datetime(2020, 4, 23, 13, 23, tzinfo=timezone.utc).timestamp() * 1000,
            },
            "DATETIME",
            {"BETWEEN": ["mb1/d1", "20200422_104500", "20200423_132300"]},
        ),
    ],
)
def test_mini_maxi_filter(mocker, create_mock_var, var_cond, var_type, filter):
    var_mock = create_mock_var("mb1/d1", var_type)
    assert conditions._mini_maxi_filter(var_mock, var_cond) == filter


@pytest.mark.parametrize(
    "type, to_patch, patch, positive, output",
    [
        ("DISCRETE", "_discrete_filter", "A", True, "A"),
        ("NUMERIC", "_mini_maxi_filter", "A", True, "A"),
        ("NUMERIC", "_mini_maxi_filter", None, True, None),
        ("NUMERIC", "_mini_maxi_filter", "A", False, {"NOT": ["A"]}),
    ],
)
def test_build_condition_filter(mocker, create_mock_var, type, to_patch, patch, positive, output):
    mock_var = create_mock_var("1", type)
    mocker.patch("braincube_connector.data.conditions.{0}".format(to_patch), return_value=patch)
    assert conditions.build_condition_filter(mock_var, {"positive": positive}) == output
