# -*- coding: utf-8 -*


from typing import Any, Dict, List

from braincube_connector.data import conditions


class ConditionContainer(object):
    """A ConditionContainer is a type of MbChild that contains conditions."""

    def get_conditions(self) -> List[Dict[str, Any]]:
        """Build the entity's list of filters.

        Returns:
            a list of filters
        """
        filters = []
        condition_list = self._metadata.get("conditions", [])  # type: ignore
        for cond in condition_list:
            var_obj = self._memory_base.get_variable(cond["variable"]["bcId"])  # type: ignore
            new_filter = conditions.build_condition_filter(var_obj, cond)
            if new_filter:
                filters.append(new_filter)
        return filters
