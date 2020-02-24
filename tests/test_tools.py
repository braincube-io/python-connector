# -*- coding: utf-8 -*-

"""Tests for the common tools."""

import json
import builtins

from py_client import tools

import pytest


def test_read_config(mocker):
    """Test the read_oauth_token function."""
    mopen = mocker.mock_open(read_data=json.dumps({"oauth2_token": "abcd", "domain": "mock.com"}))
    p_mock = mocker.patch("builtins.open", mopen, create=True)
    config = tools.read_config("~/mock/path/config.json")
    print(config)
    print(p_mock.mock_calls)
    p_mock.assert_called_once()
    assert config["oauth2_token"] == "abcd"
    assert config["domain"] == "mock.com"
    p_mock.assert_called_once_with("~/mock/path/config.json", "r")


def test_generate_header():
    """Test the generation of a headers for for the requests."""
    header1 = tools.generate_header(sso_token="a", content_type="b", accept="c")
    assert header1 == {"Content-Type": "b", "Accept": "c", "IPLSSOTOKEN": "a"}
    header2 = tools.generate_header(sso_token="abc")
    assert header2 == {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "IPLSSOTOKEN": "abc",
    }


@pytest.mark.parametrize(
    "raw_str, expected_str", [("a.b/", "a.b"), ("/a", "a"), ("/a.b", "a.b"), ("/a/b", "a/b")]
)
def test_strip_path(raw_str, expected_str):
    assert tools.strip_domain(raw_str) == expected_str


@pytest.mark.parametrize(
    "raw_str, expected_str",
    [("https://a.b", "a.b"), ("https://a.b/", "a.b"), ("https://www.a.b/", "www.a.b")],
)
def test_strip_domain(raw_str, expected_str):
    assert tools.strip_domain(raw_str) == expected_str
