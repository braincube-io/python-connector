# -*- coding: utf-8 -*-

"""Tests for the data module."""

import responses
from requests.exceptions import ConnectionError
import pytest
from datetime import datetime
import math
from tests_integration.mocks import patch_endpoints, custom_patch_endpoints
from braincube_connector import client, braincube, parameters

default_config = {
    "domain": "test.com",
    "api_key": "abcd",
}


@pytest.fixture(autouse=True)
def setup():
    # Write here any command to execute before each test
    client.instances.add_instance(client.INSTANCE_KEY, None)
    parameters.reset_parameter()
    yield
    # Write here any command to execute after each test


@responses.activate
def test_client(patch_endpoints, config=None):
    if config is None:
        config = default_config

    patch_endpoints()

    cli = client.get_instance(config_dict=config)
    return cli


@responses.activate
def test_braincube(patch_endpoints, config=None):
    patch_endpoints()
    cli = test_client(patch_endpoints, config)
    bc_list = braincube.get_braincube_list()
    assert len(bc_list) == 2
    for bc in bc_list:
        assert type(bc) == braincube.Braincube
    bc = braincube.get_braincube("demo")
    assert bc._name == "demo"
    assert bc._bcid == "demo"
    assert bc._product_id == "123"
    return bc


@responses.activate
def test_memorybase(patch_endpoints):
    bc = test_braincube(patch_endpoints)
    patch_endpoints()
    mb_list = bc.get_memory_base_list()
    assert len(mb_list) == 2
    mb = bc.get_memory_base(1)
    assert mb._name == "mb1"
    assert mb._bcid == 1
    return mb


@responses.activate
def test_memorybase_with_custom_domains(patch_endpoints, custom_patch_endpoints):
    custom_config = {
        "sso_base_url": "http://another.plop.com",
        "braincube_base_url": "http://braincube_api.plop.com/prefix/v1.0/",
        "api_key": "abcd",
    }

    with pytest.raises(ConnectionError):
        test_braincube(patch_endpoints, custom_config)

    bc = test_braincube(custom_patch_endpoints, custom_config)
    custom_patch_endpoints()
    mb = bc.get_memory_base(1)
    assert mb._name == "mb1"
    assert mb._bcid == 1


@responses.activate
def test_memorybase_with_custom_domains_and_placeholder(patch_endpoints, custom_patch_endpoints):
    custom_config = {
        "sso_base_url": "http://another.plop.com",
        "braincube_base_url": "http://{braincube-name}.plop.com/prefix/v1.0/",
        "api_key": "abcd",
    }

    with pytest.raises(ConnectionError):
        test_braincube(patch_endpoints, custom_config)

    bc = test_braincube(custom_patch_endpoints, custom_config)
    custom_patch_endpoints()
    mb = bc.get_memory_base(1)
    assert mb._name == "mb1"
    assert mb._bcid == 1
    mb.get_variable_list()


@responses.activate
def test_get_data(patch_endpoints):
    mb = test_memorybase(patch_endpoints)
    patch_endpoints()
    parameters.set_parameter({"parse_date": True})
    data = mb.get_data(["101", "102", "103"], label_type="name")
    expected_data = {
        "standard_101": [
            datetime.strptime("20201127_124000", "%Y%m%d_%H%M%S"),
            datetime.strptime("20201127_124001", "%Y%m%d_%H%M%S"),
            None,
            datetime.strptime("20201127_124002", "%Y%m%d_%H%M%S"),
        ],
        "standard_102": [1.1, 1.2, math.nan, 1.4],
        "standard_103": ["A", "B", "NaN", "D"],
    }
    for key, values in expected_data.items():
        for val_retreived, val_expected in zip(data[key], values):
            try:
                assert val_retreived == val_expected
            except AssertionError as err:
                # If a is Nan: a!=a
                if val_retreived == val_retreived or val_expected == val_expected:
                    raise err


@responses.activate
def test_get_braindata_memory_base_info_with_custom_domains(custom_patch_endpoints):
    custom_config = {
        "sso_base_url": "http://another.plop.com",
        "braincube_base_url": "http://{braincube-name}.plop.com/prefix/v1.0/",
        "api_key": "abcd",
    }

    bc = test_braincube(custom_patch_endpoints, custom_config)
    custom_patch_endpoints()
    mb = bc.get_memory_base(1)

    order_id = mb.get_order_variable_long_id()
    assert order_id == "100001"


@responses.activate
def test_variable(patch_endpoints):
    mb = test_memorybase(patch_endpoints)
    patch_endpoints()

    var = mb.get_variable("0")
    assert var.get_parameter_key("name") == "standard"
    assert var.get_name() == "standard_name"
    parameters.set_parameter({"VariableDescription_name_key": "tag"})
    assert var.get_parameter_key("name") == "tag"
    assert var.get_name() == "tag_name"
