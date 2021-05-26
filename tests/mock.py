# -*- coding: utf-8 -*-

"""Set of mocks for the tests."""

import pytest

from braincube_connector import braincube, client, constants, parameters
from braincube_connector.bases import base, base_entity
from braincube_connector.memory_base import memory_base
from braincube_connector.memory_base.nested_resources import (
    datagroup,
    event,
    job,
    mb_child,
    variable,
)


@pytest.fixture
def mock_client(mocker):
    """Create a mock client to test its methods."""
    mocker.patch.object(client.Client, "__init__", lambda x: None)
    instance = client.Client()
    instance._sso_url = "https://a.b"
    instance._braincube_base_url = "https://api.a.b"
    instance._pa_token = "abcd"
    instance._timeout = 60
    instance._verify = True
    instance._headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        constants.PAT_KEY: instance._pa_token,
    }
    instance._braincube_infos = {
        "bcname1": ("bc1", "bcname1", {"data": 1}),
        "bcname2": ("bc2", "bcname2", {"data": 2}),
    }
    mocker.patch("braincube_connector.client.get_instance", mocker.Mock(return_value=instance))
    return instance


@pytest.fixture
def base_obj():
    """Create a mock of the bases object."""
    obj = base.Base("abcd")
    return obj


@pytest.fixture
def entity_obj(base_obj):
    """Create a mock of the Base object."""
    obj = base_entity.BaseEntity(
        bcid="id123", name="entity", metadata={"meta": 1}, path="path/{bcid}"
    )
    return obj


@pytest.fixture
def mock_request_entity(mocker, monkeypatch):
    mock_request = mocker.patch(
        "braincube_connector.client.request_ws",
        return_value={"items": [{"name": "name{}".format(i), "bcId": str(i)} for i in range(2)]},
    )
    return mock_request


@pytest.fixture
def bc_obj(mock_client):
    """Create a mock of the Braincube object."""
    obj = braincube.Braincube(product_id="id123", name="bcname", metadata={"meta": 1},)
    return obj


@pytest.fixture
def mb_obj():
    """Create a mock of the MemoryBase object."""
    obj = memory_base.MemoryBase(
        bcid="1", name="mb1", metadata={"meta": 1}, path="braincube/bcname/{webservice}/mb/1"
    )
    return obj


@pytest.fixture
def mbchild_obj():
    child = mb_child.MbChild("id1", "child", {"metadata": []}, "path/mb/10/child/id1", "MB_obj")
    return child


@pytest.fixture
def create_mock_var():
    def create_mock(bcid="1", name="", metadata={"type": "NUMERIC"}, mb=None):
        name = name if name else "var{0}".format(bcid)
        var = variable.VariableDescription(
            bcid=bcid, name=name, metadata=metadata, path="path", memory_base=mb
        )
        return var

    return create_mock


@pytest.fixture
def create_mock_datagroup():
    def create_mock(bcid="1", name="", variables=[], mb=None):
        name = name if name else "datagroup{0}".format(bcid)
        metadata = {"variables": [{"bcId": var} for var in variables]}
        dgroup = datagroup.DataGroup(bcid, name, metadata, "path", mb)
        return dgroup

    return create_mock


@pytest.fixture
def create_mock_event():
    def create_mock(bcid="1", name="", variables=[], mb=None):
        name = name if name else "event{0}".format(bcid)
        metadata = {
            "conditions": [
                {"variable": {"bcId": var_id}, "minimum": 0, "maximum": 1} for var_id in variables
            ]
        }
        return event.Event(bcid, name, metadata, "path", mb)

    return create_mock


@pytest.fixture
def create_mock_job():
    def create_mock(
        bcid="1",
        name="",
        events={},
        datagroups=[],
        conditions=[],
        modelEntries=[],
        mb=None,
        path="path",
    ):
        metadata = {}
        if modelEntries:
            entries = {
                "modelEntries": [
                    {"conditions": [{"variable": {"bcId": var_id}, "minimum": 0, "maximum": 1}]}
                    for var_id in modelEntries
                ]
            }
            metadata.update(entries)
        if conditions:
            conditions = {
                "conditions": [
                    {"variable": {"bcId": var_id}, "minimum": 0, "maximum": 1}
                    for var_id in conditions
                ]
            }
            metadata.update(conditions)
        if events:
            pos, neg = events["positive"], events["negative"]
            events = {
                "events": {
                    "positiveEvents": [{"bcId": eid} for eid in pos],
                    "negativeEvents": [{"bcId": eid} for eid in neg],
                }
            }
            metadata.update(events)
        if datagroups:
            datagroups = {"dataGroups": [{"bcId": did} for did in datagroups]}
            metadata.update(datagroups)
        name = name if name else "job{0}".format(bcid)
        job_obj = job.JobDescription(bcid, name, metadata, path, mb)
        return job_obj

    return create_mock
