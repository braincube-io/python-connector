# -*- coding: utf-8 -*-

from py_client.memory_base.nested_resources import mb_child


class DataGroup(mb_child.MbChild):
    """DataGroup object that stores a set of variables."""

    entity_path = "dataGroups/{bcid}"
    request_one_path = "extended"
    request_many_path = "dataGroups/extended"
