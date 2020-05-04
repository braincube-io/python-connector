# -*- coding: utf-8 -*

from py_client.memory_base.nested_resources import condition_container, mb_child


class Event(mb_child.MbChild, condition_container.ConditionContainer):
    """Event object that stores a set of variables."""

    entity_path = "events/{bcid}"
    request_one_path = "extended"
    request_many_path = "events/all/extended"
