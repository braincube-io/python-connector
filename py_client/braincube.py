# -*- coding: utf-8 -*-

from typing import Dict, Any, List

from py_client import tools
from py_client import constants
from py_client import base_entity
from py_client import client
from py_client import memory_base


class Braincube(base_entity.BaseEntity):
    """Braincube object that handles the feature of a braincube."""

    def __init__(self, bcid: str, name: str, metadata: Dict[str, Any]):
        """Initialize Braincube.

        Args:
            bcid: Braincube unique identifier.
            name: Braincube name.
            metadata: Raw metadata associated to the Braincube.
        """
        super().__init__(bcid, name, metadata, "braincube/{bc_name}".format(bc_name=name))

    def get_memory_base(self, mb_bcid: str) -> memory_base.MemoryBase:
        """Get a MemoryBase object from its id.

        Args:
            mb_bcid: Memory base bcid.

        Returns:
            The selected MemoryBase object.
        """
        mb_path = tools.join_path([self._path, "braincube/mb/{bcid}".format(bcid=mb_bcid)])
        request_path = tools.join_path([mb_path, "summary"])
        return memory_base.MemoryBase.create_one_from_path(request_path, mb_path)

    def get_memory_base_list(
        self, page: int = -1, page_size: int = constants.DEFAULT_PAGE_SIZE
    ) -> List[memory_base.MemoryBase]:
        """Get a list of the memory bases available in the braincube.

        Args:
            page: Index of page to return, all pages are return if page=-1
            page_size: Number of elements on a page.

        Returns:
            A list of the MemoryBase objects.
        """
        mb_path = tools.join_path([self._path, "{webservice}/mb/{bcid}"])
        request_path = tools.join_path([self._path, "{webservice}/mb/all/summary"])
        return memory_base.MemoryBase.create_many_from_path(request_path, mb_path, page, page_size)


def get_braincube(name: str) -> Braincube:
    """Get a braincube object from its name.

    Args:
        name: Name of the selected braincube.

    Returns:
        The selected Braincube object.
    """
    cli = client.get_instance()
    available_braincube_infos = cli.get_braincube_infos()
    return Braincube(*available_braincube_infos[name])


def get_braincube_list(names: List[str] = None) -> List[Braincube]:
    """Get a list of available memory bases in the braincube.

    Args:
        names: List of braincube names to return.

    Returns:
        List of the Braincube objects.
    """
    cli = client.get_instance()
    available_braincube_infos = cli.get_braincube_infos()
    if not names:
        names = list(available_braincube_infos.keys())
    return [Braincube(*available_braincube_infos[key]) for key in names]
