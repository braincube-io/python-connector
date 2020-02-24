# -*- coding: utf-8 -*-

"""Tests for the client module."""

import os
import json

import py_client
from py_client import client

import pytest

import responses
from requests.exceptions import HTTPError


@pytest.fixture
def mock_client(mocker):
    """Create a mock client to test its methods."""
    m = mocker.patch.object(client.Client, "__init__", lambda x: None)
    mclient = client.Client()
    mclient._domain = "a.b"
    mclient._oauth2_token = "abcd"
    mclient._sso_token = "efgh"
    mclient._timeout = 60
    mclient._verify = True
    mclient._headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "IPLSSOTOKEN": mclient._sso_token,
    }
    return mclient


@pytest.mark.parametrize(
    "path, url", [("c", "https://a.b/c"), ("test/c", "https://a.b/test/c"), ("/c", "https://a.b/c")]
)
def test_generate_url(mock_client, path, url):
    """Test the _generate_url method."""
    assert mock_client._generate_url(path) == url


@responses.activate
def test_request_ws_error(mock_client):
    """Test whether request_ws throws a HTTPError."""
    responses.add(responses.GET, "https://a.b/path", status=400)
    with pytest.raises(HTTPError):
        mock_client.request_ws("path")


@responses.activate
def test_request_ws_succes_get(mock_client):
    """Test whether request_ws for a GET."""
    responses.add(responses.GET, "https://a.b/path", json={"val": 1}, status=200)
    data = mock_client.request_ws("path", body_data={"data": 2})
    assert data["val"] == 1
    assert responses.calls[0].request.body == "data=2"
    assert responses.calls[0].request.headers["IPLSSOTOKEN"] == mock_client._headers["IPLSSOTOKEN"]
    data = mock_client.request_ws("path", headers={"IPLSSOTOKEN": "ijkl"})
    assert responses.calls[1].request.headers["IPLSSOTOKEN"] == "ijkl"


@responses.activate
def test_request_ws_succes_post(mock_client):
    """Test whether request_ws for a POST."""
    responses.add(responses.POST, "https://a.b/path", json={"val": 1}, status=200)
    mock_client.request_ws("path", body_data={"data": 2}, rtype="POST")
    assert responses.calls[0].request.method == "POST"


@responses.activate
def test_request_sso_token(mock_client):
    """Test the _request_sso_token method"""
    path = "sso-server/rest/session/openWithToken"
    mock_url = "https://a.b/" + path
    sso_token = "efgh"
    responses.add(responses.GET, mock_url, json={"token": sso_token}, status=200)
    sso_token = mock_client._request_sso_token()
    assert sso_token == sso_token
    assert responses.calls[0].request.headers["Authorization"] == "Bearer {}".format(
        mock_client._oauth2_token
    )


def test_create_client_no_config(mocker):
    """Test the Client creation."""
    mocker.patch.object(os.path, "exists", return_value=False)
    with pytest.raises(FileNotFoundError, match=client.NO_CONFIG_MSG):
        client.Client()


def test_create_client(mocker):
    """Test the Client initialization."""
    mopen = mocker.mock_open(read_data=json.dumps({"oauth2_token": "abcd", "domain": "mock.com"}))
    p_mock = mocker.patch("builtins.open", mopen, create=True)
    sso_mock = mocker.patch.object(client.Client, "_request_sso_token", lambda x: "efgh")
    test_client = client.Client(config_file="conf.json")

    assert test_client._domain == "mock.com"
    assert test_client._oauth2_token == "abcd"
    assert test_client._sso_token == "efgh"
    test_client._timeout == 60
    test_client._verify = True
    test_client._headers == {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "IPLSSOTOKEN": "efgh",
    }
    print(test_client._sso_token)
