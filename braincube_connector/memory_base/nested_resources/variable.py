# -*- coding: utf-8 -*-

from braincube_connector.memory_base.nested_resources import mb_child


class VariableDescription(mb_child.MbChild):
    """VariableDescription object that stores the description of a variable."""

    name_key = "standard"
    entity_path = "variables/{bcid}"
    request_one_path = "extended"
    request_many_path = "variables/summary"

    def get_type(self) -> str:
        """Get the type of the variable.

        Returns:
            The type of the variable.
        """
        return self._metadata["type"]

    def get_long_id(self) -> str:
        """Get the extended id of a variable.

        Returns:
            An extended variable id 'long_mb_id/dvar_id'.
        """
        return "mb{mb}/d{var}".format(mb=self._memory_base.get_bcid(), var=self._bcid)
