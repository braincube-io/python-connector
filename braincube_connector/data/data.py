# -*- coding: utf-8 -*-

"""Module used to collect data from braindata."""

from typing import Dict, List, Any

from braincube_connector import client
from braincube_connector import tools
from braincube_connector.data import conditions

from braincube_connector import parameters

import json
import datetime

DATA_PATH = "braindata/{mb_id}/LF"
DATACOL = "data"


def _expand_var_id(long_mb_id: str, var_id: str) -> str:
    """Extend a variable name to include its memory bases id.

    Args:
        long_mb_id: Memory bases bcId extended with the 'mb' keyword.
        var_id: Variable bcId.

    Returns:
        An extended variable id 'long_mb_id/dvar_id'.
    """
    return "{mb}/d{var}".format(mb=long_mb_id, var=var_id)


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
    """Get data from the memory bases.

    Args:
        variable_ids: bcIds of variables for which the data are collected.
        braincube_path: path of the braincube.
        mb_metadata: metadata of the memory bases.
        filters: List of fileter to apply to the request.

    Returns:
        A dictionary of data list.
    """
    long_mb_id = "mb{bcid}".format(bcid=mb_metadata["bcId"])
    variable_ids = [_expand_var_id(long_mb_id, vv) for vv in variable_ids]
    data_path = tools.join_path([braincube_path, DATA_PATH.format(mb_id=long_mb_id)])
    body_data = {
        "order": _expand_var_id(long_mb_id, mb_metadata["referenceDate"]),
        "definitions": variable_ids,
        "context": {"dataSource": long_mb_id},
    }
    filters = conditions.combine_filters(filters)  # Merge filters in one filter
    if len(filters) == 1:
        body_data["context"]["filter"] = filters[0]  # type: ignore
    return _extract_format_data(
        client.request_ws(data_path, body_data=json.dumps(body_data), rtype="POST")
    )
