# -*- coding: utf-8 -*-

from typing import Dict, Any

from py_client import base_entity


class JobDescription(base_entity.BaseEntity):
    """JobDescription object that stores the description of a job."""

    def __init__(self, bcid: str, name: str, metadata: Dict[str, Any], path: str):
        """Initialize JobDescription.

        Args:
            bcid: Variable identifier.
            name: Variable name.
            metadata: Informations about the variable.
            path: Path of the job on the server.
        """
        super().__init__(bcid, name, metadata, path)
