# -*- coding: utf-8 -*-

from typing import Dict, List, Any

from braincube_connector.bases import base_entity, resource_getter
from braincube_connector.data import data
from braincube_connector.memory_base.nested_resources import variable, event, datagroup, job, rule


class MemoryBase(base_entity.BaseEntity, resource_getter.ResourceGetter):
    """MemoryBase object that handles the feature of a braincube."""

    entity_path = "{webservice}/mb/{bcid}"
    request_one_path = "extended"
    request_many_path = "{webservice}/mb/all/summary"

    def get_variable(self, bcid: str) -> variable.VariableDescription:
        """Get a variable description from its bcId.

        Args:
            bcid: Variable bcid.

        Returns:
            A variable description.
        """
        return self._get_resource(variable.VariableDescription, bcid)

    def get_variable_list(self, **kwargs) -> List[variable.VariableDescription]:
        """Get a list a of variable descriptions from a list of ids.

        Args:
            **kwargs: Optional page and page_size.

        Returns:
            A list of Variable descriptions.
        """
        return self._get_resource_list(variable.VariableDescription, **kwargs)

    def get_job(self, bcid: str) -> job.JobDescription:
        """Get a job description from its bcId.

        Args:
            bcid: Job bcid.

        Returns:
            A job description.
        """
        return self._get_resource(job.JobDescription, bcid)

    def get_job_list(self, **kwargs) -> List[job.JobDescription]:
        """Get a list a of job descriptions from a list of ids.

        Args:
            **kwargs: Optional page and page_size.

        Returns:
            A list of Job descriptions.
        """
        return self._get_resource_list(job.JobDescription, **kwargs)

    def get_datagroup(self, bcid: str) -> datagroup.DataGroup:
        """Get a DataGroup from its bcId.

        Args:
            bcid: Data group bcid.

        Returns:
            A data group description.
        """
        return self._get_resource(datagroup.DataGroup, bcid)

    def get_datagroup_list(self, **kwargs) -> List[datagroup.DataGroup]:
        """Get a list a of data groups from a list of ids.

        Args:
            **kwargs: Optional page and page_size.

        Returns:
            A list of data groups.
        """
        return self._get_resource_list(datagroup.DataGroup, **kwargs)

    def get_event(self, bcid: str) -> event.Event:
        """Get a Event from its bcId.

        Args:
            bcid: Event bcid.

        Returns:
            A event description.
        """
        return self._get_resource(event.Event, bcid)

    def get_event_list(self, **kwargs) -> List[event.Event]:
        """Get a list a of events from a list of ids.

        Args:
            **kwargs: Optional page and page_size.

        Returns:
            A list of events.
        """
        return self._get_resource_list(event.Event, **kwargs)

    def get_rule(self, bcid: str) -> rule.RuleDescription:
        """Get a variable description from its bcId.

        Args:
            bcid: Rule bcid.

        Returns:
            A Rule description.
        """
        return self._get_resource(rule.RuleDescription, bcid)

    def get_rule_list(self, **kwargs) -> rule.RuleDescription:
        """Get a list a of rule descriptions from a list of ids.

        Args:
            **kwargs: Optional page and page_size.

        Returns:
            A list of Rule descriptions.
        """
        return self._get_resource_list(
            rule.RuleDescription, collection_path="rules/all/selector", **kwargs
        )

    def get_data(
        self, var_ids: "List[str]", filters: "List[Dict[str, Any]]" = None
    ) -> Dict[str, Any]:
        """Get data from the memory bases.

        Args:
            var_ids: bcIds of variables for which the data are collected.
            filters: List of filters to apply to the request.

        Returns:
            A dictionary of data list.
        """
        bc_path = (self._path.split("{webservice}"))[0]
        return data.collect_data(var_ids, bc_path, self._metadata, filters)

    def _get_resource(self, resource_class: Any, bcid: str):  # type: ignore
        """Get a resource from its bcId.

        Args:
            resource_class: Class of the resource to get.
            bcid: Event bcid.

        Returns:
            A resource description.
        """
        return super()._get_resource(resource_class, bcid, memory_base=self)

    def _get_resource_list(self, resource_class: Any, **kwargs):  # type: ignore
        """Get a list a of resources from a list of ids.

        Args:
            resource_class: Class of the resources to get.
            **kwargs: Optional page and page_size or parent (memory_base).

        Returns:
            A list of resources.
        """
        return super()._get_resource_list(resource_class, memory_base=self, **kwargs)
