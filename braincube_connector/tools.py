# -*- coding: utf-8 -*-

"""A set of tools to automate tasks for the python client."""

import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Optional
from urllib.parse import urlsplit, urlunsplit

from braincube_connector import constants


def read_config(path: str) -> Dict[str, str]:
    """Reads the configuration file.

    Args:
        path: Path of the configuration token file.

    Returns:
        A configuration dictionary.
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


def build_url(
    base_url: str = constants.EMPTY_STRING,
    path: str = constants.EMPTY_STRING,
    braincube_name: str = constants.EMPTY_STRING,
) -> str:
    """Appends a path to the given base_url to generate a valid url.

    Args:
        base_url: Base URL to complete with given path.
        path: Path to a specific resource.
        braincube_name: name of the braincube to use to replace the placeholder.

    Returns:
        A complete url.
    """
    parts = urlsplit(base_url)
    full_path = join_path([parts.path, path])

    url_with_placeholder = urlunsplit(
        (
            parts.scheme,
            parts.netloc,
            strip_path(full_path),
            constants.EMPTY_STRING,
            constants.EMPTY_STRING,
        )
    )

    return url_with_placeholder.replace(constants.BRAINCUBE_NAME_PLACEHOLDER, braincube_name)


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


def get_sso_base_url(config: Dict[str, str]) -> str:
    """Returns the Braincube SSO API base URL, built using the given configuration dictionary.

    Args:
        config: A configuration dictionary

    Returns:
        An URL to the Braincube SSO API
    """
    default_base_url = "{protocol}://{domain}".format(
        protocol=constants.DEFAULT_PROTOCOL, domain=config.get(constants.DOMAIN_KEY),
    )

    base_url = config.get(constants.SSO_BASE_URL_KEY, default_base_url)
    return strip_path(base_url)


def get_braincube_base_url(config: Dict[str, str]) -> str:
    """Returns the Braincube API base URL, built using the given configuration dictionary.

    Args:
        config: A configuration dictionary

    Returns:
        An URL to the Braincube API
    """
    default_base_url = "{protocol}://{api_subdomain}.{domain}".format(
        protocol=constants.DEFAULT_PROTOCOL,
        api_subdomain=constants.DEFAULT_API_SUBDOMAIN,
        domain=config.get(constants.DOMAIN_KEY),
    )

    base_url = config.get(constants.BRAINCUBE_BASE_URL_KEY, default_base_url)
    return strip_path(base_url)
