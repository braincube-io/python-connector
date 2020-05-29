# -*- coding: utf-8 -*-

"""A set of tools to extract conditions from an entity."""

from typing import Dict, List, Any, Optional

from braincube_connector import tools

BCID = "bcId"
VAR_KEY = "variable"


def combine_filters(
    filters: "Optional[List[Any]]", operator: str = "AND"
) -> "List[Dict[str, Any]]":
    """Nest multiple filters in a series of AND gates.

    Args:
        filters: Filters to combine together.
        operator: operator to Returns

    Returns:
        A list containing a unique filter combining the passed filters.
    """
    if not filters:
        return []
    if len(filters) == 1:
        return filters
    elif len(filters) == 2:
        return [{operator: [filters[0], filters[1]]}]
    first_and = {operator: [filters[0], filters[1]]}
    return combine_filters([first_and] + filters[2:], operator=operator)


def build_condition_filter(
    var_obj: "Variable", var_cond: Dict[str, Any]  # type: ignore  # noqa
) -> Optional[Dict[str, Any]]:
    """Build a filter interpretable by the webservice from a variable condition.

    Args:
        var_obj: Entity to which the filter is associated.
        var_cond: Condition applied to the entity.

    Returns:
        A variable filter.
    """
    if var_obj.get_type() == "DISCRETE":
        new_filter = _discrete_filter(var_obj, var_cond)
    else:
        new_filter = _mini_maxi_filter(var_obj, var_cond)
    if not new_filter:
        return None
    if not var_cond["positive"]:
        new_filter = {"NOT": [new_filter]}
    return new_filter


def _discrete_filter(var_obj: "Variable", var_cond: "Dict[str, Any]") -> "Optional[Dict[str, Any]]":  # type: ignore  # noqa
    """Build a filter for a discrete variable.

    Args:
        var_obj: Entity to which the filter is associated.
        var_cond: Condition applied to the entity.

    Returns:
        A discrete variable filter.
    """
    filter_list = [
        {"EQUALS": [var_obj.get_long_id(), [modality]]}
        for modality in var_cond.get("modalities", [])
    ]
    if not filter_list:
        return None
    return combine_filters(filter_list, operator="OR")[0]


def _mini_maxi_filter(var_obj: "Variable", var_cond: "Dict[str, Any]") -> "Optional[Dict[str, Any]]":  # type: ignore  # noqa
    """Build a filter between a min and a max.

    Args:
        var_obj: Entity to which the filter is associated.
        var_cond: Condition applied to the entity.

    Returns:
        A filter for variable accepting a min and a max.
    """
    mini, maxi = var_cond.get("minimum"), var_cond.get("maximum")
    if var_obj.get_type() == "DATETIME":
        mini, maxi = tools.to_datetime_str(mini), tools.to_datetime_str(maxi)
    if (mini is not None) and (maxi is not None):
        return {"BETWEEN": [var_obj.get_long_id(), mini, maxi]}
    elif mini is not None:
        return {"GREAT": [var_obj.get_long_id(), mini]}
    elif maxi is not None:
        return {"LESS": [var_obj.get_long_id(), maxi]}
    return None
