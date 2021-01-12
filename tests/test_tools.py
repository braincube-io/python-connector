# -*- coding: utf-8 -*-

"""Tests for the common tools."""

import builtins
import json
from datetime import datetime, timezone

import pytest

from braincube_connector import constants, tools, instances

CONF_PATH = "~/mock/path/config.json"
DUMMY_CONFIG = {constants.PAT_KEY: "abcd", constants.DOMAIN_KEY: "https://mock.com"}


def test_read_config(mocker):
    """Test the read_read_config function."""
    mopen = mocker.mock_open(read_data=json.dumps(DUMMY_CONFIG))
    p_mock = mocker.patch("builtins.open", mopen, create=True)
    config = tools.read_config(CONF_PATH)
    p_mock.assert_called_once()
    assert config[constants.PAT_KEY] == "abcd"
    assert config[constants.DOMAIN_KEY] == "https://mock.com"
    p_mock.assert_called_once_with(CONF_PATH, "r")


def test_read_config_file_not_found(mocker):
    p_mock = mocker.patch("builtins.open", mocker.Mock(side_effect=FileNotFoundError))
    config_path = CONF_PATH
    with pytest.raises(
        FileNotFoundError, match="Token file {cpath} not found".format(cpath=config_path)
    ):
        KeyErrorconfig = tools.read_config(config_path)


def test_generate_header():
    """Test the generation of a headers for the requests."""
    header1 = tools.generate_header(authentication={"token": "a"}, content_type="b", accept="c")
    assert header1 == {"Content-Type": "b", "Accept": "c", "token": "a"}
    header2 = tools.generate_header(authentication={"token": "abc"})
    assert header2 == {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "token": "abc",
    }


def test_generate_header_multiple_token():
    """Test raising an error when authentication contains multiple tokens."""
    with pytest.raises(KeyError):
        tools.generate_header(
            authentication={"token1": "a", "token2": "b"}, content_type="b", accept="c"
        )


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
    "passed_param, existing_files, expected_dict",
    [
        (
            {"config_dict": DUMMY_CONFIG},
            [constants.DEFAULT_CONFIG, constants.DEFAULT_HOME_CONFIG],
            DUMMY_CONFIG,
        ),
        (
            {"config_file": "custom_file"},
            ["custom_file", constants.DEFAULT_HOME_CONFIG, constants.DEFAULT_CONFIG],
            {**DUMMY_CONFIG, "read_file": constants.DEFAULT_CONFIG},
        ),
        (
            {},
            [constants.DEFAULT_HOME_CONFIG, constants.DEFAULT_CONFIG],
            {**DUMMY_CONFIG, "read_file": constants.DEFAULT_CONFIG},
        ),
        (
            {},
            [constants.DEFAULT_HOME_CONFIG],
            {**DUMMY_CONFIG, "read_file": constants.DEFAULT_HOME_CONFIG},
        ),
    ],
)
def test_check_config_file(mocker, passed_param, existing_files, expected_dict):
    mocker.patch("os.path.exists", side_effect=lambda x: x == expected_dict.get("read_file"))
    mock_read_data = mocker.patch(
        "braincube_connector.tools.read_config",
        side_effect=lambda x: {**DUMMY_CONFIG, "read_file": x},
    )
    assert tools.check_config(**passed_param) == expected_dict


def test_check_config_file_no_file(mocker):
    mock_exists = check_conf_mock = mocker.patch("os.path.exists", mocker.Mock(return_value=False))
    with pytest.raises(FileNotFoundError, match=constants.NO_CONFIG_MSG):
        tools.check_config()


@pytest.mark.parametrize(
    "timestamp,output",
    [
        (datetime(2020, 4, 22, 10, 45, tzinfo=timezone.utc).timestamp() * 1000, "20200422_104500"),
        (None, None),
    ],
)
def test_to_datetime_str(timestamp, output):
    assert tools.to_datetime_str(timestamp) == output