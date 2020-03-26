# -*- coding: utf-8 -*-

"""Tests for the common tools."""

import json
import builtins

from py_client import tools
from py_client import constants

import pytest

OAUTH2 = "oauth2_token"
CONF_PATH = "~/mock/path/config.json"


def test_read_config(mocker):
    """Test the read_oauth_token function."""
    mopen = mocker.mock_open(read_data=json.dumps({OAUTH2: "abcd", "domain": "mock.com"}))
    p_mock = mocker.patch("builtins.open", mopen, create=True)
    config = tools.read_config(CONF_PATH)
    p_mock.assert_called_once()
    assert config[OAUTH2] == "abcd"
    assert config["domain"] == "mock.com"
    p_mock.assert_called_once_with(CONF_PATH, "r")


@pytest.mark.parametrize("config_key", [OAUTH2, "domain"])
def test_read_config_missing_key(mocker, config_key):
    """Test the read_oauth_token function."""
    config = {OAUTH2: "abcd", "domain": "mock.com"}
    config.pop(config_key)
    mopen = mocker.mock_open(read_data=json.dumps(config))
    p_mock = mocker.patch("builtins.open", mopen, create=True)
    with pytest.raises(KeyError):
        KeyErrorconfig = tools.read_config(CONF_PATH)


def test_read_config_file_not_found(mocker):
    p_mock = mocker.patch("builtins.open", mocker.Mock(side_effect=FileNotFoundError))
    config_path = CONF_PATH
    with pytest.raises(
        FileNotFoundError, match="Token file {cpath} not found".format(cpath=config_path)
    ):
        KeyErrorconfig = tools.read_config(config_path)


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


def test_join_path():
    path_elmts = ["/a", "/b/c/", "d", "e/"]
    assert tools.join_path(path_elmts) == "a/b/c/d/e"


@pytest.mark.parametrize(
    "path, url", [("c", "https://a.b/c"), ("test/c", "https://a.b/test/c"), ("/c", "https://a.b/c")]
)
def test_generate_url(path, url):
    """Test the _generate_url method."""
    assert tools.generate_url("a.b", path) == url


@pytest.mark.parametrize(
    "passed_path, existing_files, selected_file",
    [
        (
            "myconfig.json",
            ["myconfig.json", constants.DEFAULT_CONFIG, constants.DEFAULT_HOME_CONFIG],
            "myconfig.json",
        ),
        (
            "",
            ["myconfig.json", constants.DEFAULT_CONFIG, constants.DEFAULT_HOME_CONFIG],
            constants.DEFAULT_CONFIG,
        ),
        ("", ["myconfig.json", constants.DEFAULT_HOME_CONFIG], constants.DEFAULT_HOME_CONFIG),
    ],
)
def test_check_config_file(mocker, passed_path, existing_files, selected_file):
    mock_exists = mocker.patch("os.path.exists", lambda x: x in existing_files)
    assert tools.check_config_file(passed_path) == selected_file


def test_check_config_file_no_file(mocker):
    mock_exists = check_conf_mock = mocker.patch("os.path.exists", mocker.Mock(return_value=False))
    with pytest.raises(FileNotFoundError, match=constants.NO_CONFIG_MSG):
        tools.check_config_file("config.json")
