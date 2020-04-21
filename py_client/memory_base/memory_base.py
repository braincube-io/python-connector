# -*- coding: utf-8 -*-

from typing import Dict, List, Tuple, Any

from py_client.bases import base_entity
from py_client.data import data
from py_client import tools
from py_client.memory_base.nested_resources import variable, event, datagroup, job

EXTENDED = "extended"


class MemoryBase(base_entity.BaseEntity):
    """MemoryBase object that handles the feature of a braincube."""

    def get_variable(self, bcid: str) -> variable.VariableDescription:
        """Get a variable description from its bcId.

        Args:
            bcid: Variable bcid.

        Returns:
            A variable description.
        """
        return self._get_ressource(variable.VariableDescription, bcid)

    def get_variable_list(self, **kwargs) -> List[variable.VariableDescription]:
        """Get a list a of variable descriptions from a list of ids.

        Args:
            **kwargs: Optional page and page_size.

        Returns:
            A list of Variables description.
        """
        return self._get_ressource_list(variable.VariableDescription, **kwargs)

    def get_job(self, bcid: str) -> job.JobDescription:
        """Get a job description from its bcId.

        Args:
            bcid: Job bcid.

        Returns:
            A job description.
        """
        return self._get_ressource(job.JobDescription, bcid)

    def get_job_list(self, **kwargs) -> List[job.JobDescription]:
        """Get a list a of job descriptions from a list of ids.

        Args:
            **kwargs: Optional page and page_size.

        Returns:
            A list of Jobs description.
        """
        return self._get_ressource_list(job.JobDescription, **kwargs)

    def get_datagroup(self, bcid: str) -> datagroup.DataGroup:
        """Get a DataGroup from its bcId.

        Args:
            bcid: Data group bcid.

        Returns:
            A data group description.
        """
        return self._get_ressource(datagroup.DataGroup, bcid)

    def get_datagroup_list(self, **kwargs) -> List[datagroup.DataGroup]:
        """Get a list a of data groups from a list of ids.

        Args:
            **kwargs: Optional page and page_size.

        Returns:
            A list of data groups.
        """
        return self._get_ressource_list(datagroup.DataGroup, **kwargs)

    def get_event(self, bcid: str) -> event.Event:
        """Get a Event from its bcId.

        Args:
            bcid: Event bcid.

        Returns:
            A event description.
        """
        return self._get_ressource(event.Event, bcid)

    def get_event_list(self, **kwargs) -> List[event.Event]:
        """Get a list a of events from a list of ids.

        Args:
            **kwargs: Optional page and page_size.

        Returns:
            A list of events.
        """
        return self._get_ressource_list(event.Event, **kwargs)

    def get_data(
        self, var_ids: "List[str]", filters: "List[Dict[str, Any]]" = None
    ) -> Dict[str, Any]:
        """Get data from the memory bases.

        Args:
            var_ids: bcIds of variables for which the data are collected.
            filters: List of filters to apply to the request.

        Returns:
            A dictionary of data list.
        """
        bc_path = (self._path.split("{webservice}"))[0]
        return data.collect_data(var_ids, bc_path, self._metadata, filters)

    def _get_ressource(self, ressource_class: Any, bcid: str):
        """Get a ressource from its bcId.

        Args:
            ressource_class: Class of the ressource to get.
            bcid: Event bcid.

        Returns:
            A ressource description.
        """
        return ressource_class.create_one_from_path(
            *generate_path(
                self._path,
                ressource_class.entity_path.format(bcid=bcid),
                ressource_class.request_one_path,
            ),
            memory_base=self
        )

    def _get_ressource_list(self, ressource_class: Any, **kwargs):
        """Get a list a of ressources from a list of ids.

        Args:
            ressource_class: Class of the ressources to get.
            **kwargs: Optional page and page_size.

        Returns:
            A list of ressources.
        """
        return ressource_class.create_many_from_path(
            *generate_path(
                self._path,
                ressource_class.entity_path,
                ressource_class.request_many_path,
                request_list=True,
            ),
            memory_base=self,
            **kwargs
        )


def generate_path(
    mb_path: str, entity_path: str, request_path: str, request_list: bool = False
) -> Tuple[str, str]:
    """Factorize the generation of path required by create_*_from_path.

    Args:
        mb_path: Path of the memory bases.
        entity_path: Path complement to go to the entity.
        request_path: Path complement to request.
        request_list: Is the request for a list or one element?

    Returns:
        The complete path to request and to bind to the created entity.
    """
    entity_path = tools.join_path([mb_path, entity_path])
    pre_request_path = mb_path if request_list else entity_path
    request_path = tools.join_path([pre_request_path, request_path])
    return (request_path, entity_path)
