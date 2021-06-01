# -*- coding: utf-8 -*-

"""Tests for the mb_child module."""

from braincube_connector.memory_base.nested_resources import mb_child
from tests.mock import mbchild_obj


def test_initialize():
    child = mb_child.MbChild(
        "id1", "child", {"metadata": []}, "path/mb/11/child/id1", parent_entity="MB_obj"
    )
    assert child._name == "child"
    assert child._memory_base == "MB_obj"


def test_get_memorybase(mocker, mbchild_obj):
    assert mbchild_obj.get_memory_base() == "MB_obj"
