# -*- coding: utf-8 -*-
"""Tests for the memory_base module."""

from tests.mock import var_obj


def test_get_type(var_obj):
    assert var_obj.get_type() == "TYPE"
