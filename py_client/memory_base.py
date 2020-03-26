# -*- coding: utf-8 -*-

from typing import Dict, List, Any

from py_client import base_entity
from py_client import constants
from py_client import tools
from py_client import variable
from py_client import job


class MemoryBase(base_entity.BaseEntity):
    """MemoryBase object that handles the feature of a braincube."""

    def __init__(self, bcid: str, name: str, metadata: Dict[str, Any], path: str):
        """Initialize BaseEntity.

        Args:
            bcid: Unique identifier of the object in braincube.
            name: Usual name of the object.
            metadata: Raw metadata associated to the object.
            path: Path of the entity on the server.
        """
        super().__init__(bcid, name, metadata, path)

    def get_variable(self, var_bcid: str) -> variable.VariableDescription:
        """Get a variable description from its bcId.

        Args:
            var_bcid: Variable bcid.

        Returns:
            A variable description.
        """
        var_path = tools.join_path([self._path, "variables/{bcid}".format(bcid=var_bcid)])
        request_path = tools.join_path([var_path, "extended"])
        return variable.VariableDescription.create_one_from_path(request_path, var_path)

    def get_variable_list(
        self, page: int = -1, page_size: int = constants.DEFAULT_PAGE_SIZE
    ) -> List[variable.VariableDescription]:
        """Get a list a of variable descriptions from a list of ids.

        Args:
            page: Index of page to return, all pages are return if page=-1
            page_size: Number of elements on a page.

        Returns:
            A list of Variables description.
        """
        var_path = tools.join_path([self._path, "variables/{bcid}"])
        request_path = tools.join_path([self._path, "variables/summary"])
        return variable.VariableDescription.create_many_from_path(
            request_path, var_path, page, page_size
        )

    def get_job(self, job_bcid: str) -> job.JobDescription:
        """Get a job description from its bcId.

        Args:
            job_bcid: Job bcid.

        Returns:
            A job description.
        """
        job_path = tools.join_path([self._path, "jobs/{bcid}".format(bcid=job_bcid)])
        request_path = tools.join_path([job_path, "extended"])
        return job.JobDescription.create_one_from_path(request_path, job_path)

    def get_job_list(
        self, page: int = -1, page_size: int = constants.DEFAULT_PAGE_SIZE
    ) -> List[job.JobDescription]:
        """Get a list a of job descriptions from a list of ids.

        Args:
            page: Index of page to return, all pages are return if page=-1
            page_size: Number of elements on a page.

        Returns:
            A list of Jobs description.
        """
        job_path = tools.join_path([self._path, "jobs/{bcid}"])
        request_path = tools.join_path([self._path, "jobs/all/summary"])
        return job.JobDescription.create_many_from_path(request_path, job_path, page, page_size)
