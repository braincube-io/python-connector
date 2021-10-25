# -*- coding: utf-8 -*-

"""Module used to collect data from braindata."""

import json
from typing import Any, Dict, List

import pandas as pd

from braincube_connector import client, parameters, tools
from braincube_connector.data import conditions

DATA_PATH = "braindata/{mb_id}/LF"
DATACOL = "data"


def _expand_var_id(long_mb_id: str, var_id: int) -> str:
    """Extend a variable name to include its memory bases id.

    Args:
        long_mb_id: Memory bases bcId extended with the 'mb' keyword.
        var_id: Variable bcId.

    Returns:
        An extended variable id 'long_mb_id/dvar_id'.
    """
    return "{mb}/d{var}".format(mb=long_mb_id, var=var_id)


def _to_datetime(dates: List["str"]):
    """Convert DATE str to a datetime object.

    Args:
        dates: A braincube styled date string.

    Returns:
        A datetime object.
    """
    dates = pd.to_datetime(dates, errors="coerce", format="%Y%m%d_%H%M%S").to_series()
    return [pandas_timestamp_to_datetime(timestamp) for timestamp in dates]


def pandas_timestamp_to_datetime(timestamp):
    """Convert pandas timestamp to datetime, with NaT handling.

    Args:
        timestamp: Pandas timestamp to convert to a python datetime.

    Returns:
        A python datetime object.
    """
    if pd.isnull(timestamp):
        return None
    return pd.Timestamp.to_pydatetime(timestamp)


def _extract_format_data(raw_dataset: Dict[str, Any]) -> Dict[int, Any]:
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
        col_id = int(col["id"].split("/d")[1])
        if col["type"] == "DATETIME" and parameters.get_parameter("parse_date"):
            formatted_dataset[col_id] = _to_datetime(col[DATACOL])
        elif col["type"] == "NUMERIC":
            try:
                formatted_dataset[col_id] = list(map(int, col[DATACOL]))
            except ValueError:
                formatted_dataset[col_id] = list(map(float, col[DATACOL]))
        else:
            formatted_dataset[col_id] = col[DATACOL]
    return formatted_dataset


def get_braindata_memory_base_info(
    braincube_path: str, memory_base_bcid: str, braincube_name=""
) -> Dict[str, str]:
    """Get the memory base informations from the braindata.

    Args:
        braincube_path: Path of the memory base's parent braincube.
        memory_base_bcid: memory base's bcid.
        braincube_name: Name of the braincube to use to replace the `{braincube-name}` placeholder

    Returns:
        Json dictionary with the memory base informations.
    """
    long_mb_id = "mb{bcid}".format(bcid=memory_base_bcid)
    braindata_info_path = "braindata/{mb_id}/simple".format(mb_id=long_mb_id)
    data_path = tools.join_path([braincube_path, braindata_info_path.format()])
    return client.request_ws(data_path, braincube_name=braincube_name)


def collect_data(
    variable_ids: List[int],
    memory_base: "MemoryBase",  # type: ignore  # noqa
    filters: List[Dict[str, Any]] = None,
) -> Dict[int, Any]:
    """Get data from the memory bases.

    Args:
        variable_ids: bcIds of variables for which the data are collected.
        memory_base: A memory base on which to collect the data.
        filters: List of filter to apply to the request.

    Returns:
        A dictionary of data list.
    """
    long_mb_id = "mb{bcid}".format(bcid=memory_base.get_bcid())
    long_variable_ids = [_expand_var_id(long_mb_id, vv) for vv in variable_ids]
    data_path = tools.join_path(
        [memory_base.get_braincube_path(), DATA_PATH.format(mb_id=long_mb_id)]
    )
    body_data = {
        "order": memory_base.get_order_variable_long_id(),
        "definitions": long_variable_ids,
        "context": {"dataSource": long_mb_id},
    }
    filters = conditions.combine_filters(filters)  # Merge filters in one filter
    if len(filters) == 1:
        body_data["context"]["filter"] = filters[0]  # type: ignore
    return _extract_format_data(
        client.request_ws(
            data_path,
            body_data=json.dumps(body_data),
            rtype="POST",
            braincube_name=memory_base.get_braincube_name(),
        )
    )
