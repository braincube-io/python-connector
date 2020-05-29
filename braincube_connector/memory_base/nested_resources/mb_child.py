# -*- coding: utf-8 -*-

from braincube_connector.bases import base_entity


class MbChild(base_entity.BaseEntity):
    """MbChild object provides an interface between a child and its memory bases."""

    def __init__(self, bcid, name, metadata, path, memory_base):
        """Initialize a memory bases child.

        Args:
            bcid: Unique identifier of the entity description in braincube.
            name: Usual name of the entity description.
            metadata: Raw metadata associated to the entity description.
            path: Path of the entity description on the server.
            memory_base: Instance of the parent memory base.
        """
        self.initialize(bcid, name, metadata, path, memory_base)

    def initialize(self, bcid, name, metadata, path, memory_base):
        """Initialize a memory bases child.

        Args:
            bcid: Unique identifier of the entity description in braincube.
            name: Usual name of the entity description.
            metadata: Raw metadata associated to the entity description.
            path: Path of the entity description on the server.
            memory_base: Instance of the parent memory base.
        """
        super().initialize(bcid, name, metadata, path)
        self._memory_base = memory_base

    def get_memory_base(self) -> "MemoryBase":  # type: ignore  # noqa
        """Get the entity's parent memory bases.

        Returns:
            A memory bases entity.
        """
        return self._memory_base
