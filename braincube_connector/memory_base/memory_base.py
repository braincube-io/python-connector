# -*- coding: utf-8 -*-

from typing import Dict, List, Any, Union

import pandas as pd

from braincube_connector.bases import base_entity, resource_getter
from braincube_connector.data import data
from braincube_connector.memory_base.nested_resources import variable, event, datagroup, job, rule


class MemoryBase(base_entity.BaseEntity, resource_getter.ResourceGetter):
    """MemoryBase object that handles the feature of a braincube."""

    entity_path = "{webservice}/mb/{bcid}"
    request_one_path = "extended"
    request_many_path = "{webservice}/mb/all/summary"

    def get_variable(self, bcid: Union[str, int]) -> variable.VariableDescription:
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

    def get_job(self, bcid: Union[str, int]) -> job.JobDescription:
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

    def get_datagroup(self, bcid: Union[str, int]) -> datagroup.DataGroup:
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

    def get_event(self, bcid: Union[str, int]) -> event.Event:
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

    def get_rule(self, bcid: Union[str, int]) -> rule.RuleDescription:
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
        self,
        var_ids: "List[Union[int,str]]",
        filters: "List[Dict[str, Any]]" = None,
        label_type: "str" = "bcid",
        dataframe: "bool" = False,
    ) -> Union[pd.DataFrame, Dict[str, Any]]:
        """Get data from the memory bases.

        Args:
            var_ids: bcIds of variables for which the data are collected.
            filters: List of filters to apply to the request.
            label_type: "bcid" / "name"
            dataframe: True, return Dataframe; False, return Dict

        Returns:
            A dictionary of data list or a pandas DataFrame.
        """
        int_var_ids = [int(var_id) for var_id in var_ids]
        datasource = data.collect_data(int_var_ids, self, filters)

        if label_type == "name":
            mapping = {var_id: self.get_variable(var_id).get_name() for var_id in int_var_ids}
            datasource = {
                mapping[data_key]: data_value for data_key, data_value in datasource.items()
            }

        if dataframe:
            return pd.DataFrame(datasource)

        return datasource

    def get_order_variable_long_id(self) -> str:
        """Get the long id of the memory base order variable.

        Returns:
            A variable long id.
        """
        infos = data.get_braindata_memory_base_info(
            self.get_braincube_path(), self._bcid, self.get_braincube_name()
        )
        for order_key in ("reference", "order"):
            order_id = infos.get(order_key)
            if order_id:
                return order_id
        raise KeyError("The memory base contains neither a reference nor a order key.")
