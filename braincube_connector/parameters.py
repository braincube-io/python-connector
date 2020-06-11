# -*- coding: utf-8 -*-

"""Customizable parameters used by the client."""

from typing import Any, Dict

from braincube_connector import constants, instances

_default_parameters = {
    "page_size": constants.DEFAULT_PAGE_SIZE,
    "parse_date": constants.DEFAULT_PARSE_DATE,
}


def set_parameter(param_dict: Dict[str, Any]):
    """Set a braincube_connector parameter to a new value.

    Args:
        param_dict: dictionary of parameters to be updated {param_key: new_value}.
    """
    pset = instances.get_instance("parameter_set")
    pset.update(param_dict)


def get_parameter(param_key: str) -> Any:
    """Get the value of a braincube_connector parameter.

    Args:
        param_key: Name of the parameter to update.

    Returns:
        The value of the selected parameter.
    """
    pset = instances.get_instance("parameter_set")
    return pset.get(param_key, _default_parameters[param_key])


def reset_parameter():
    """Reset all the customizable parameters to default."""
    pset = instances.get_instance("parameter_set")
    pset.clear()
