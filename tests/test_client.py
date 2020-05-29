# -*- coding: utf-8 -*-

"""Tests for the client module."""

import os
import json

from braincube_connector import client
from braincube_connector.bases import base
from braincube_connector import constants
from tests.mock import mock_client

import pytest

import responses
from requests.exceptions import HTTPError

from tests.test_bases.test_base import LOAD_URL


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
    assert responses.calls[0].request.headers["IPLSSOTOKEN"] == mock_client._headers["IPLSSOTOKEN"]
    data = mock_client.request_ws("path", headers={"IPLSSOTOKEN": "ijkl"})
    assert responses.calls[1].request.headers["IPLSSOTOKEN"] == "ijkl"


@responses.activate
def test_request_ws_succes_post(mock_client):
    """Test whether request_ws for a POST."""
    responses.add(responses.POST, LOAD_URL, json={"val": 1}, status=200)
    mock_client.request_ws("path", body_data={"data": 2}, rtype="POST")
    assert responses.calls[0].request.method == "POST"


@responses.activate
def test_request_access(mock_client):
    """Test the _request_sso_token method"""
    path = "sso-server/rest/session/openWithToken"
    mock_url = "https://a.b/" + path
    sso_token = "efgh"
    returned_json = {
        "token": sso_token,
        "accessList": [{"product": {"productId": "id1234", "name": "testbraincube",}}],
    }
    responses.add(responses.GET, mock_url, json=returned_json, status=200)
    sso_token, braincubes = mock_client._request_access()
    assert sso_token == sso_token
    assert responses.calls[0].request.headers["Authorization"] == "Bearer {}".format(
        mock_client._oauth2_token
    )
    assert len(braincubes) == 1
    assert "testbraincube" in braincubes


def test_create_client_no_config(mocker):
    """Test the Client creation."""
    mocker.patch.object(os.path, "exists", return_value=False)
    with pytest.raises(FileNotFoundError, match=constants.NO_CONFIG_MSG):
        client.Client()


def test_str(mock_client):
    assert str(mock_client) == "Client(domain=a.b)"


def test_create_client(mocker):
    """Test the Client initialization."""
    mopen = mocker.mock_open(read_data=json.dumps({"oauth2_token": "abcd", "domain": "mock.com"}))
    p_mock = mocker.patch("builtins.open", mopen, create=True)
    check_conf_mock = mocker.patch("os.path.exists", mocker.Mock(return_value=True))
    sso_mock = mocker.patch.object(
        client.Client, "_request_access", lambda x: ("efgh", [base.Base("test")])
    )
    test_client = client.get_instance(config_file="conf.json")

    assert test_client._domain == "mock.com"
    assert test_client._oauth2_token == "abcd"
    assert test_client._sso_token == "efgh"
    assert test_client._timeout == 60
    assert test_client._verify == True
    assert test_client._headers == {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "IPLSSOTOKEN": "efgh",
    }

    test_client2 = client.get_instance()
    assert test_client is test_client2
    assert mopen.call_count == 1

    with pytest.raises(Exception, match="A client has already been inialized."):
        client.Client()
