# -*- coding: utf-8 -*

from py_client.memory_base.nested_resources import mb_child


class Event(mb_child.MbChild):
    """Event object that stores a set of variables."""

    entity_path = "events/{bcid}"
    request_one_path = "extended"
    request_many_path = "events/all/extended"
