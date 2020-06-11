# -*- coding: utf-8 -*-

from typing import Any, Dict, List

from braincube_connector.memory_base.nested_resources import mb_child


class DataGroup(mb_child.MbChild):
    """DataGroup object that stores a set of variables."""

    entity_path = "dataGroups/{bcid}"
    request_one_path = "extended"
    request_many_path = "dataGroups/summary"

    def get_variable_ids(self) -> List[str]:
        """Get the bcIds for the variables in the group.

        Returns:
            The list of the group variable ids.
        """
        return [var_meta["bcId"] for var_meta in self._metadata["variables"]]

    def get_variable_list(self) -> "List[VariableDescription]":  # type: ignore  # noqa
        """Get a list a of the variable descriptions in the group.

        Returns:
            A list of Variables description.
        """
        return [self._memory_base.get_variable(bcid) for bcid in self.get_variable_ids()]

    def get_data(self, filters: "List[Dict[str, Any]]" = None) -> Dict[str, Any]:
        """Get data from the data group.

        Args:
            filters: List of filters to apply to the request.

        Returns:
            A dictionary of data list.
        """
        return self._memory_base.get_data(self.get_variable_ids(), filters)
