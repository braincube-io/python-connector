# -*- coding: utf-8 -*-

from py_client.memory_base.nested_resources import mb_child


class VariableDescription(mb_child.MbChild):
    """VariableDescription object that stores the description of a variable."""

    name_key = "standard"
    entity_path = "variables/{bcid}"
    request_one_path = "extended"
    request_many_path = "variables/extended"

    def get_type(self) -> str:
        """Get the type of the variable.

        Returns:
            The type of the variable.
        """
        return self._metadata["type"]


def expand_var_id(long_mb_id: str, var_id: str) -> str:
    """Extend a variable name to include its memory bases id.

    Args:
        long_mb_id: Memory bases bcId extended with the 'mb' keyword.
        var_id: Varaible bcId.

    Returns:
        An extended variable id 'long_mb_id/dvar_id'.
    """
    return "{mb}/d{var}".format(mb=long_mb_id, var=var_id)
