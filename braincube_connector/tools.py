# -*- coding: utf-8 -*-

"""A set of tools to automate tasks for the python client."""

import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Optional

from braincube_connector import constants


def read_config(path: str) -> Dict[str, str]:
    """Reads the configuration file.

    Args:
        path: Path of the configuration token file.

    Returns:
        A configuration diconary.
    """
    config_path = os.path.join(path)

    try:
        with open(config_path, "r") as fconf:
            return json.loads(fconf.readline())
    except FileNotFoundError:
        raise FileNotFoundError("Token file {cpath} not found".format(cpath=config_path))


def generate_header(
    authentication: Dict[str, str],
    content_type: str = "application/json",
    accept: str = "application/json",
) -> Dict[str, str]:
    """Generate a header for the requests.

    Args:
        authentication: The authentication part of the header.
        content_type: file format of the content.
        accept: file format accept

    Returns:
        A ready to use header.
    """
    if len(authentication) > 1:
        raise KeyError("Authentication should use only one method.")
    header = dict(authentication)
    header.update({"Content-Type": content_type, "Accept": accept})
    return header


def strip_path(path: str) -> str:
    """Removes the '/' from the sides of a path.

    Args:
        path: a raw path.

    Returns:
        A path stripped from its side '/'.
    """
    return path.strip("/")


def strip_domain(domain: str) -> str:
    """Removes the 'http(s)://' and '/' from a domain name.

    Args:
        domain: a raw domain name.

    Returns:
        A formatted domain name.
    """
    if "//" in domain:
        domain = domain.split("//")[1]
    return strip_path(domain)


def join_path(path_elmts: List[str]) -> str:
    """Generate a a clean path from a succession of path elements.

    Args:
        path_elmts: A list of path elements to join.

    Returns:
        A clean path.
    """
    clean_elmts = [strip_path(elmts) for elmts in path_elmts]
    return "/".join(clean_elmts)


def generate_url(domain: str, path: str) -> str:
    """Appends a path to the client domain to generate a valid url.

    Args:
        domain: Optional domain, overwrites the default.
        path: Path on the domain.

    Returns:
        A complete url on the configured domain.
    """
    path = strip_path(path)
    return "https://{domain}/{path}".format(domain=domain, path=path)


def check_config(
    config_dict: Optional[Dict[str, str]] = None, config_file: Optional[str] = None
) -> Dict[str, str]:
    """Choose the configuration according the preset rules.

    Args:
        config_file: A path to a configuration file.
        config_dict: A configuration dictionary.

    Returns:
        Path to the first valid configuration file found.
    """
    if config_dict:
        return config_dict

    if config_file is not None and os.path.exists(config_file):
        return read_config(config_file)

    if os.path.exists(constants.DEFAULT_CONFIG):
        return read_config(constants.DEFAULT_CONFIG)

    if os.path.exists(constants.DEFAULT_HOME_CONFIG):
        return read_config(constants.DEFAULT_HOME_CONFIG)

    raise FileNotFoundError(constants.NO_CONFIG_MSG)


def to_datetime_str(timestamp: Optional[float]) -> Optional[str]:
    """Convert a braincube timestamp to a formatted datetime string.

    Args:
        timestamp: timestamp (in ms) to convert.

    Returns:
        A braincube formatted datatime string.
    """
    if not timestamp:
        return None
    return datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc).strftime("%Y%m%d_%H%M%S")
