# -*- coding: utf-8 -*-

"""Tests for the base module."""

import re

from tests.mock import base_obj, base_entity, mock_client

BASE_STR = "Base(name=abcd)"
LOAD_URL = "https://api.a.b/path"


def test_create_base(base_obj):
    assert base_obj._name == "abcd"


def test_get_str(base_obj):
    assert base_obj._get_str({"name": "abcd"}) == BASE_STR


def test_str(base_obj):
    assert str(base_obj) == BASE_STR


def test_repr(base_obj):
    assert re.search(r"<Base\(name=abcd\) at .*?>", repr(base_obj))
