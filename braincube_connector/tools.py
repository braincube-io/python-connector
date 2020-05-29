# -*- coding: utf-8 -*-

"""A set of tools to automate tasks for the python client."""

import os
import json
from typing import Dict, List, Optional
from datetime import datetime, timezone

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
            config = json.loads(fconf.readline())
    except FileNotFoundError:
        raise FileNotFoundError("Token file {cpath} not found".format(cpath=config_path))
    for key in ("domain", "oauth2_token"):
        if key not in config:
            raise KeyError("The configuration file needs a {key} key.".format(key=key))
    return config


def generate_header(
    sso_token: str, content_type: str = "application/json", accept: str = "application/json",
) -> Dict[str, str]:
    """Generate a header for the requests.

    Args:
        sso_token: a sso token.
        content_type: file format of the content.
        accept: file format accept

    Returns:
        A ready to use header.
    """
    return {"Content-Type": content_type, "Accept": accept, "IPLSSOTOKEN": sso_token}


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


def check_config_file(config_path: str = "") -> str:
    """Choose the configuration according the preset rules.

    Args:
        config_path: Provided path to the configuration.

    Returns:
        Path to the first valid configuration file found.
    """
    if config_path == "":
        if os.path.exists(constants.DEFAULT_CONFIG):
            return constants.DEFAULT_CONFIG
        elif os.path.exists(constants.DEFAULT_HOME_CONFIG):
            return constants.DEFAULT_HOME_CONFIG
    elif os.path.exists(config_path):
        return config_path

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
