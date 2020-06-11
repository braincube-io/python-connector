# -*- coding: utf-8 -*-

"""The modules contains the singleton instances of the package in a dictionary."""

from typing import Any, Dict

instances: Dict[str, Any] = {"parameter_set": {}}


def add_instance(key: str, instance: Any):
    """Add an instance to the dictionary of instances.

    Args:
        key: Key of the instance.
        instance: Object to store as un instance.
    """
    instances[key] = instance


def get_instance(key: str) -> Any:
    """Get an instance from a key.

    Args:
        key: Key of the instance.

    Returns:
        The requested instance.
    """
    return instances.get(key)
