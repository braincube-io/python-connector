# -*- coding: utf-8 -*-

from py_client.memory_base.nested_resources import mb_child


class JobDescription(mb_child.MbChild):
    """JobDescription object that stores the description of a job."""

    entity_path = "jobs/{bcid}"
    request_one_path = "extended"
    request_many_path = "jobs/all/extended"
