# -*- coding: utf-8 -*-

from typing import Dict, Any
from py_client import base_entity


class VariableDescription(base_entity.BaseEntity):
    """VariableDescription object that stores the description of a variable."""

    name_key = "standard"

    def __init__(self, bcid: str, name: str, metadata: Dict[str, Any], path: str):
        """Initialize VariableDescription.

        Args:
            bcid: Variable identifier.
            name: Variable name.
            metadata: Informations about the variable.
            path: Path of the variable on the server.
        """
        super().__init__(bcid, name, metadata, path)

    def get_type(self) -> str:
        """Get the type of the variable.

        Returns:
            The type of the variable.
        """
        return self._metadata["type"]


def expand_var_id(long_mb_id: str, var_id: str) -> str:
    """Extend a variable name to include its memory base id.

    Args:
        long_mb_id: Memory base bcId extended with the 'mb' keyword.
        var_id: Varaible bcId.

    Returns:
        An extended variable id '<long_mb_id>/d<var_id>'.
    """
    return "{mb}/d{var}".format(mb=long_mb_id, var=var_id)
