# -*- coding: utf-8 -*-

from braincube_connector.memory_base.nested_resources import mb_child


class RuleDescription(mb_child.MbChild):
    """RuleDescription object that stores the description of a rule."""

    entity_path = "rules/{bcid}"
    request_one_path = "summary"
    request_many_path = "rules/all/summary"
