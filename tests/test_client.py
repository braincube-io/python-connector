# -*- coding: utf-8 -*-

"""Tests for the client module."""

import json
import os

import pytest
import responses
import requests
from requests.exceptions import HTTPError

from braincube_connector import client, constants, instances
from braincube_connector.bases import base
from tests.mock import mock_client
from tests.test_bases.test_base import LOAD_URL


@pytest.fixture(autouse=True)
def clean_client_instances():
    if client.INSTANCE_KEY in instances.instances:
        del instances.instances[client.INSTANCE_KEY]


@responses.activate
def test_request_ws_error(mock_client):
    """Test whether request_ws throws a HTTPError."""
    responses.add(responses.GET, LOAD_URL, status=400)
    with pytest.raises(HTTPError):
        mock_client.request_ws("path")


@responses.activate
def test_request_ws_succes_get(mock_client):
    """Test whether request_ws for a GET."""
    responses.add(responses.GET, LOAD_URL, json={"val": 1}, status=200)
    data = mock_client.request_ws("path", body_data={"data": 2})
    assert data["val"] == 1
    assert responses.calls[0].request.body == "data=2"
    assert (
        responses.calls[0].request.headers[constants.PAT_KEY]
        == mock_client._headers[constants.PAT_KEY]
    )
    data = mock_client.request_ws("path", headers={constants.PAT_KEY: "ijkl"})
    assert responses.calls[1].request.headers[constants.PAT_KEY] == "ijkl"


@responses.activate
def test_request_ws_succes_post(mock_client):
    """Test whether request_ws for a POST."""
    responses.add(responses.POST, LOAD_URL, json={"val": 1}, status=200)
    mock_client.request_ws("path", body_data={"data": 2}, rtype="POST")
    assert responses.calls[0].request.method == "POST"


@responses.activate
def test_request_ws_succes_no_json(mock_client):
    """Test whether request_ws can run without parsing the output."""
    responses.add(responses.GET, LOAD_URL, json={"val": 1}, status=200)
    result = mock_client.request_ws(
        "path", body_data={"data": 2}, rtype="GET", response_as_json=False
    )
    assert type(result) == requests.models.Response

@responses.activate
def test_request_ws_json_decode_error_with_content(mock_client):
    """Test whether request_ws includes response content in JSON decode error messages."""
    # Mock a response that returns non-JSON content
    responses.add(
        responses.GET, 
        LOAD_URL, 
        body="<html><body>Response content not JSON</body></html>",
        status=200
    )
    
    with pytest.raises(requests.exceptions.JSONDecodeError) as excinfo:
        mock_client.request_ws("path", response_as_json=True)
    
    # Check that the error message contains the response content
    error_message = str(excinfo.value)
    assert "Invalid JSON response" in error_message
    assert "Response content:" in error_message
    assert "<html><body>Response content not JSON</body></html>" in error_message


@responses.activate
def test_request_braincubes(mock_client):
    """Test the _request_braincubes method"""
    path = "sso-server/ws/user/me"
    mock_url = "https://a.b/" + path
    returned_json = {
        "accessList": [
            {
                "product": {
                    "productId": "id1234",
                    "name": "testbraincube",
                }
            }
        ],
    }
    mock_client._authentication = {"token": "abcd"}
    responses.add(responses.GET, mock_url, json=returned_json, status=200)
    braincubes = mock_client._request_braincubes()
    assert responses.calls[0].request.headers["token"] == "abcd"
    assert len(braincubes) == 1
    assert "testbraincube" in braincubes


@responses.activate
def test_build_authentication_oauth2(mock_client):
    """Test the build authentication function for an oauth2 token."""
    mock_url = "https://a.b/sso-server/ws/oauth2/session"
    responses.add(responses.GET, mock_url, status=200, json={"token": "abcd"})
    header = mock_client._build_authentication({constants.OAUTH2_KEY: "efgh"})
    assert header == {constants.SSO_TOKEN_KEY: "abcd"}


def test_build_authentication_pat(mock_client):
    """Test the build authentication function for an personal access token."""
    header = mock_client._build_authentication({constants.API_KEY: "abcd"})
    assert header == {constants.PAT_KEY: "abcd"}


def test_create_client_no_config(mocker):
    """Test the Client creation."""
    mocker.patch.object(os.path, "exists", return_value=False)
    with pytest.raises(FileNotFoundError, match=constants.NO_CONFIG_MSG):
        client.Client()


def test_str(mock_client):
    assert str(mock_client) == "Client(domain=https://a.b)"


def test_create_client(mocker, clean_client_instances):
    """Test the Client initialization."""
    check_conf_mock = mocker.patch("os.path.exists", mocker.Mock(return_value=False))
    sso_mock = mocker.patch.object(
        client.Client, "_request_braincubes", lambda x: [base.Base("test")]
    )
    mock_add_instance = mocker.patch(
        "braincube_connector.client.instances.add_instance", side_effect=instances.add_instance
    )
    test_client = client.get_instance(
        config_dict={constants.API_KEY: "abcd", constants.DOMAIN_KEY: "mock.com"}
    )
    assert test_client._sso_url == "https://mock.com"
    assert test_client._braincube_base_url == "https://api.mock.com"
    assert test_client._authentication == {constants.PAT_KEY: "abcd"}
    assert test_client._timeout == 60
    assert test_client._verify == True
    assert test_client._headers == {
        "Content-Type": "application/json",
        "Accept": "application/json",
        constants.PAT_KEY: "abcd",
    }

    test_client2 = client.get_instance()
    assert test_client is test_client2
    assert mock_add_instance.call_count == 1

    with pytest.raises(Exception, match="A client has already been inialized."):
        client.Client()


@pytest.mark.parametrize(
    "verify_cert_config, expected_verify",
    [(False, False), (None, True), (True, True)],
)
def test_client_verify(mocker, verify_cert_config, expected_verify, clean_client_instances):
    """Test the setting of the verify SSL certificate parameter."""
    sso_mock = mocker.patch.object(
        client.Client, "_request_braincubes", lambda x: [base.Base("test")]
    )
    config_dict = {
        constants.API_KEY: "abcd",
        constants.DOMAIN_KEY: "mock.com",
    }
    if verify_cert_config is not None:
        config_dict[constants.VERIFY_CERT] = verify_cert_config
    test_client = client.get_instance(
        config_dict=config_dict,
    )
    assert test_client._verify == expected_verify
