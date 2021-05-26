# -*- coding: utf-8 -*-

from typing import Any, Dict, List, Optional

from braincube_connector import client, parameters, constants
from braincube_connector.bases import base

NAME = "name"
BCID = "bcid"


class BaseEntity(base.Base):
    """Basics components of an entity requested by the connector."""

    def __init__(
        self,
        bcid: str,
        name: str,
        metadata: Dict[str, Any],
        path: str = constants.EMPTY_STRING,
        braincube_name: str = constants.EMPTY_STRING,
        parent_entity: Optional["BaseEntity"] = None,
    ):
        """Initialize BaseEntity.

        Args:
            bcid: Unique identifier of the object in braincube.
            name: Usual name of the object.
            metadata: Raw metadata associated to the object.
            path: Path of the entity on the server.
            braincube_name: name of the braincube linked to this entity,
                            useful if you use a placeholder in your config.
            parent_entity: parent of this entity, used to retrieve the braincube name if needed.
        """
        self.initialize(bcid, name, metadata, path, braincube_name, parent_entity)

    def __repr__(self) -> str:
        """Produce the a detailed description of the BaseEntity object.

        Returns:
            A detailed description of the BaseEntity object.
        """
        description = self._get_str(attributes={NAME: self._name, "id": self._bcid})
        return "<{self_str} at {addr}>".format(self_str=description, addr=hex(id(self)))

    @classmethod
    def create_from_json(cls, json_data: Dict[str, str], entity_path: str, caller, **kwargs) -> Any:
        """Create an entity from a raw json.

        Args:
            json_data: Json dictionary obtained from a request to the webservice.
            entity_path: Path of the entity on the webservice.
            caller: class used to call this method, useful to indicate which is the parent entity.
            **kwargs: Additional keyword argument to pass to an object initialization.

        Returns:
            The created entity.
        """
        entity = cls.__new__(cls)

        entity.initialize(
            json_data[cls.get_parameter_key(BCID)],
            json_data[cls.get_parameter_key(NAME)],
            json_data,
            entity_path,
            parent_entity=caller,
            **kwargs,
        )
        return entity

    @classmethod
    def create_singleton_from_path(
        cls,
        request_path: str,
        entity_path: str,
        caller,
        braincube_name: str = constants.EMPTY_STRING,
        **kwargs,
    ) -> Any:
        """Create an entity from a request path.

        Args:
            request_path: Webservice path to request.
            entity_path: Path of the entity on the webservice.
            caller: class used to call this method, useful to indicate which is the parent entity.
            braincube_name: name of the braincube linked to this entity,
                            useful if you use a placeholder in your config.
            **kwargs: Additional keyword argument to pass to an object initialization.

        Returns:
            The created entity.
        """
        json_data = client.request_ws(
            request_path.format(webservice="braincube"), braincube_name=braincube_name
        )
        return cls.create_from_json(json_data, entity_path, caller, **kwargs)

    @classmethod
    def create_collection_from_path(
        cls,
        request_path: str,
        entity_path: str,
        caller,
        page: int = -1,
        page_size: int = -1,
        braincube_name: str = constants.EMPTY_STRING,
        **kwargs,
    ) -> List[Any]:
        """Create many memory_base from a request path.

        Args:
            request_path: Webservice path to request.
            entity_path: Path of the entity on the webservice.
            caller: class used to call this method, useful to indicate which is the parent entity.
            page: Index of page to return, all pages are return if page=-1
            page_size: Number of memory_base per page.
            braincube_name: name of the braincube linked to this entity,
                            useful if you use a placeholder in your config.
            **kwargs: Additional keyword argument to pass to an object initialization.

        Returns:
            The list of created created entity.
        """
        if page_size == -1:
            page_size = parameters.get_parameter("page_size")
        offset = 0 if page < 0 else page * page_size
        entity_list: List[Any] = []

        while True:
            json_data = client.request_ws(
                "{path}?offset={offset}&size={size}".format(
                    path=request_path.format(webservice="braincube"), offset=offset, size=page_size,
                ),
                braincube_name=braincube_name,
            )
            new_entities = [
                cls.create_from_json(elmt, entity_path, caller, **kwargs)
                for elmt in json_data["items"]
            ]
            entity_list += new_entities
            if not new_entities or page > -1:
                break
            else:
                offset += page_size
        return entity_list

    def get_metadata(self) -> Dict[str, Any]:
        """Gets the metadata of the Object.

        Returns:
            A dictionary of metadata.
        """
        return self._metadata

    def get_bcid(self) -> str:
        """Get the entity's bcId.

        Returns:
            The bcId of the object.
        """
        return self._bcid

    def initialize(
        self,
        bcid: str,
        name: str,
        metadata: Dict[str, Any],
        path: str = constants.EMPTY_STRING,
        braincube_name: str = constants.EMPTY_STRING,
        parent_entity: Optional["BaseEntity"] = None,
    ):
        """Initialize BaseEntity.

        Args:
            bcid: Unique identifier of the object in braincube.
            name: Usual name of the object.
            metadata: Raw metadata associated to the object.
            path: Path of the entity on the server.
            braincube_name: name of the braincube linked to this entity,
                            useful if you use a placeholder in your config.
            parent_entity: parent of this entity, used to retrieve the braincube name if needed.
        """
        self._bcid = bcid
        self._name = name
        self._metadata = metadata
        if "{bcid}" in path:
            path = path.replace("{bcid}", str(self._bcid))
        self._path = path
        self._braincube_name = braincube_name
        self._parent_entity = parent_entity

    @classmethod
    def get_parameter_key(cls, key) -> str:
        """Get baseEntity_name_key parameter.and name_bcid parameter.

        Args:
            key: "name" to get the name key or "bcid" to get the bcid key

        Returns:
            The name key of the baseEntity or The bcid key of the baseEntity]
        """
        parameter_key = parameters.get_parameter("{0}_{1}_key".format(cls.__name__, key))

        return (
            parameter_key if parameter_key else cls.__base__.get_parameter_key(key)  # type: ignore
        )

    def get_name(self):
        """Get the entity's name.

        Returns:
            The name of the object.
        """
        return self._metadata[self.get_parameter_key("name")]

    def get_uuid(self):
        """Get the uuid of the entity.

        Returns:
            The uuid of the variable.
        """
        return self._metadata["uuid"].split("_")[1]
