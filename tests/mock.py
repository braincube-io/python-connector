# -*- coding: utf-8 -*-

"""Set of mocks for the tests."""

import pytest

from py_client import braincube
from py_client.bases import base, base_entity
from py_client import client
from py_client.memory_base import memory_base
from py_client.memory_base.nested_resources import variable, job, mb_child, datagroup, event


@pytest.fixture
def mock_client(mocker):
    """Create a mock client to test its methods."""
    mocker.patch.object(client.Client, "__init__", lambda x: None)
    instance = client.Client()
    instance._domain = "a.b"
    instance._oauth2_token = "abcd"
    instance._sso_token = "efgh"
    instance._timeout = 60
    instance._verify = True
    instance._headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "IPLSSOTOKEN": instance._sso_token,
    }
    instance._braincube_infos = {
        "bcname1": ("bc1", "bcname1", {"data": 1}),
        "bcname2": ("bc2", "bcname2", {"data": 2}),
    }
    mocker.patch("py_client.client.get_instance", mocker.Mock(return_value=instance))
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
        "py_client.client.request_ws",
        return_value={"items": [{"name": "name{}".format(i), "bcId": str(i)} for i in range(2)]},
    )
    return mock_request


@pytest.fixture
def bc_obj():
    """Create a mock of the Braincube object."""
    obj = braincube.Braincube(bcid="id123", name="bcname", metadata={"meta": 1},)
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
    def create_mock(bcid="1", name="", type="NUMERIC", mb=None):
        name = name if name else "var{0}".format(bcid)
        var = variable.VariableDescription(
            bcid=bcid, name=name, metadata={"type": type}, path="path", memory_base=mb
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
        bcid="1", name="", events={}, datagroups=[], conditions=[], modelEntries=[], mb=None
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
        job_obj = job.JobDescription(bcid, name, metadata, "path", mb)
        return job_obj

    return create_mock
