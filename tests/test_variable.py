# -*- coding: utf-8 -*-
"""Tests for the memory_base module."""

from tests.mock import var_obj

from py_client import variable


def test_get_type(var_obj):
    assert var_obj.get_type() == "TYPE"


def test_expand_var_id():
    assert variable.expand_var_id("mb20", "2001") == "mb20/d2001"
