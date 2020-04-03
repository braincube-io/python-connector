# -*- coding: utf-8 -*-

"""Module used to collect data from braindata."""

from typing import Dict, List, Any

from py_client import client
from py_client import variable
from py_client import tools
from py_client import parameters

import json
import datetime


DATA_PATH = "braindata/{mb_id}/LF"
DATACOL = "data"


def _combine_filters(filters: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Nest multiple filters in a series of AND gates.

    Args:
        filters: Filters to combine together.

    Returns:
        A list of string of the combine filters.
    """
    if len(filters) == 1:
        return filters[0]
    elif len(filters) == 2:
        return {"AND": [filters[0], filters[1]]}
    first_and = {"AND": [filters[0], filters[1]]}
    return _combine_filters([first_and] + filters[2:])


def _to_datetime(date: "str") -> Any:
    """Convert DATE str to a datetime object.

    Args:
        date: A braincube styled date string.

    Returns:
        A datetime object.
    """
    return datetime.datetime.strptime(date, "%Y%m%d_%H%M%S")


def _extract_format_data(raw_dataset: Dict[str, Any]) -> Dict[str, Any]:
    """Extract the requested data from the json.

    The function extracts the data keys and types and convert the columns
    using the types.

    Args:
        raw_dataset: An unformated dataset received from braindata.

    Returns:
        A formated dictionary {column_key: formated column data}
    """
    formatted_dataset = {}
    for col in raw_dataset["datadefs"]:
        col_id = col["id"].split("/d")[1]
        if col["type"] == "DATETIME" and parameters.get_parameter("parse_date"):
            formatted_dataset[col_id] = list(map(_to_datetime, col[DATACOL]))
        elif col["type"] == "NUMERIC":
            try:
                formatted_dataset[col_id] = list(map(int, col[DATACOL]))
            except ValueError:
                formatted_dataset[col_id] = list(map(float, col[DATACOL]))
        else:
            formatted_dataset[col_id] = col[DATACOL]
    return formatted_dataset


def collect_data(
    variable_ids: List[str],
    braincube_path: str,
    mb_metadata: Dict[str, str],
    filters: List[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Get data from the memory base.

    Args:
        variable_ids: bcIds of variables for which the data are collected.
        braincube_path: path of the braincube.
        mb_metadata: metadata of the memory base.
        filters: List of fileter to apply to the request.

    Returns:
        A dictionary of data list.
    """
    long_mb_id = "mb{bcid}".format(bcid=mb_metadata["bcId"])
    variable_ids = [variable.expand_var_id(long_mb_id, vv) for vv in variable_ids]
    data_path = tools.join_path([braincube_path, DATA_PATH.format(mb_id=long_mb_id)])
    body_data = {
        "order": variable.expand_var_id(long_mb_id, mb_metadata["referenceDate"]),
        "definitions": variable_ids,
        "context": {"dataSource": long_mb_id},
    }
    if filters:
        body_data["context"]["filter"] = _combine_filters(filters)  # type: ignore
    variable_data = client.request_ws(data_path, body_data=json.dumps(body_data), rtype="POST")
    return _extract_format_data(variable_data)
