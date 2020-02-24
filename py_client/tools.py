# -*- coding: utf-8 -*-

"""A set of tools to automate tasks for the python client."""

import os
import json
from typing import Dict


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
