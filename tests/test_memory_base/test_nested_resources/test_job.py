# -*- coding: utf-8 -*-
"""Tests for the job module."""
from tests.mock import create_mock_job, create_mock_var, create_mock_event, create_mock_datagroup


def test_get_events(mocker, create_mock_job):
    mock_mb = mocker.Mock()
    mock_mb.get_event.side_effect = lambda e_id: "event{}".format(e_id)

    job = create_mock_job(events={"negative": ["1", "2"], "positive": ["3", "4"]}, mb=mock_mb)
    assert job.get_events() == {
        "negativeEvents": ["event1", "event2"],
        "positiveEvents": ["event3", "event4"],
    }


def test_get_conditions(mocker, create_mock_job, create_mock_var, create_mock_event):
    mock_mb = mocker.Mock()

    mock_mb.get_variable.side_effect = lambda var_id: create_mock_var(bcid=str(var_id))

    events = {
        "1": create_mock_event(variables=["3"], mb=mock_mb),
        "2": create_mock_event(variables=["4"], mb=mock_mb),
        "3": create_mock_event(variables=["5"], mb=mock_mb),
    }
    mock_mb.get_event.side_effect = lambda e_id: events[e_id]

    mocker.patch(
        "py_client.data.conditions.build_condition_filter",
        side_effect=lambda var, cond: "cond{}".format(var.get_bcid()),
    )

    job = create_mock_job(
        conditions=[1, 2], events={"negative": ["1", "2"], "positive": ["3"]}, mb=mock_mb
    )
    assert job.get_conditions() == ["cond1", "cond2"]
    assert job.get_conditions(combine=True) == [{"AND": ["cond1", "cond2"]}]
    assert job.get_conditions(include_events=True) == [
        "cond1",
        "cond2",
        {"NOT": ["cond3"]},
        {"NOT": ["cond4"]},
        "cond5",
    ]


def test_get_variable_ids(mocker, create_mock_datagroup, create_mock_job):
    mock_mb = mocker.Mock()
    mock_mb.get_datagroup.return_value = create_mock_datagroup(variables=["3", "4"])
    job = create_mock_job(modelEntries=["1", "1", "2"], datagroups=["1"], mb=mock_mb)
    assert sorted(job.get_variable_ids()) == ["1", "2", "3", "4"]


def test_get_data(mocker, create_mock_job):
    mock_mb = mocker.Mock()
    job = create_mock_job(mb=mock_mb)
    variables = ["var1", "var2"]
    conditions = ["cond1", "cond2"]
    filters = ["cond3"]
    mocker.patch.object(
        job, "get_conditions", return_value=conditions,
    )
    mocker.patch.object(
        job, "get_variable_ids", return_value=variables,
    )
    job.get_data()
    job.get_data(filters)
    calls = [mocker.call(variables, conditions), mocker.call(variables, filters + conditions)]
    mock_mb.get_data.assert_has_calls(calls)
