# -*- coding: utf-8 -*-

from typing import Dict


class Base(object):
    """Base object that sets the standards for all the objects of the package."""

    def __init__(self, name: str):
        """Initialize BaseEntity.

        Args:
            name: Name of the object.
        """
        self._name = name

    def __str__(self) -> str:
        """Produce informal representation of the Base object.

        Returns:
            An informal representation of the Base object.
        """
        return self._get_str(attributes={"name": self._name})

    def __repr__(self) -> str:
        """Produce the a detailed description of the Base object.

        Returns:
            A detailed description of the Base object.
        """
        return "<{self_str} at {addr}>".format(self_str=self, addr=hex(id(self)))

    def _get_str(self, attributes: Dict[str, str]):
        """Generate formated string used to print the object.

        Args:
            attributes: Custom set of attributes to integrate to the string.

        Returns:
            Formatted string available to be used by __str__.
        """
        attrs_str = ", ".join(
            [
                "{aname}={aval}".format(aname=attr_name, aval=attr_value)
                for attr_name, attr_value in attributes.items()
            ]
        )
        return "{class_name}({attrs})".format(class_name=self.__class__.__name__, attrs=attrs_str)
