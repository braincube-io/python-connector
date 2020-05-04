# -*- coding: utf-8 -*-

from py_client.memory_base.nested_resources import condition_container, mb_child


class JobDescription(mb_child.MbChild, condition_container.ConditionContainer):
    """JobDescription object that stores the description of a job."""

    entity_path = "jobs/{bcid}"
    request_one_path = "extended"
    request_many_path = "jobs/all/extended"
