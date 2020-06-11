# -*- coding: utf-8 -*-

from typing import Any, Dict, List

from braincube_connector.bases import resource_getter
from braincube_connector.data import conditions
from braincube_connector.memory_base.nested_resources import condition_container, mb_child, rule

BCID = "bcId"
VARIABLE = "variable"
POSITIVE_EVENTS = "positiveEvents"
NEGATIVE_EVENTS = "negativeEvents"


class JobDescription(
    mb_child.MbChild, condition_container.ConditionContainer, resource_getter.ResourceGetter
):
    """JobDescription object that stores the description of a job."""

    entity_path = "jobs/{bcid}"
    request_one_path = "extended"
    request_many_path = "jobs/all/summary"

    def get_data(self, filters: "List[Dict[str, Any]]" = None) -> Dict[str, Any]:
        """Get the filtered data used in the job.

        Warning: As for now the webservice does not have access to the actual job data. This
        function accesses the data from the memory base with the same filters as when the job data
        were created but might return different data if the actual data have been updated in the
        memory base but not in the job.

        Args:
            filters: List of filters to apply to the request.

        Returns:
            A dictionary of filtered data list.
        """
        if not filters:
            filters = []
        filters = filters + self.get_conditions(combine=True, include_events=True)
        variables = self.get_variable_ids()
        return self._memory_base.get_data(variables, filters)

    def get_conditions(self, combine=False, include_events=False) -> "List[Dict[str, Any]]":
        """Get the job conditions.

        Args:
            combine: Combine the conditions under a single condition.
            include_events: If True, it also includes the event conditions.

        Returns:
            A List of conditions.
        """
        filters: List[Dict[str, Any]] = []
        if include_events:
            events = self.get_events()
            for negative_event in events[NEGATIVE_EVENTS]:
                filters = filters + [
                    {"NOT": conditions.combine_filters(negative_event.get_conditions())}
                ]
            for positive_event in events[POSITIVE_EVENTS]:
                filters = filters + positive_event.get_conditions()
        filters = super().get_conditions() + filters
        return conditions.combine_filters(filters) if combine else filters

    def get_variable_ids(self) -> List[str]:
        """Get a list a of the variable bcIds used by the job.

        The list of variable includes the actual job variables and the condition variables.

        Returns:
            A list of variables bcIds.
        """
        variables: List[str] = []
        for entry in self._metadata["modelEntries"]:
            variables = variables + [
                cond[VARIABLE][BCID] for cond in entry["conditions"] if VARIABLE in cond
            ]
        for group in self._metadata["dataGroups"]:
            variables = variables + self._memory_base.get_datagroup(group[BCID]).get_variable_ids()
        return list(set(variables))

    def get_events(self) -> "Dict[str, List[Event]]":  # type: ignore  # noqa
        """Get the events used in the job.

        Returns:
            A list of events.
        """
        events: Dict[str, Any] = {POSITIVE_EVENTS: [], NEGATIVE_EVENTS: []}
        for positive_event in self._metadata["events"][POSITIVE_EVENTS]:
            events[POSITIVE_EVENTS].append(self._memory_base.get_event(positive_event["bcId"]))
        for negative_event in self._metadata["events"][NEGATIVE_EVENTS]:
            events[NEGATIVE_EVENTS].append(self._memory_base.get_event(negative_event["bcId"]))
        return events

    def get_categories(self) -> List[Dict[str, Any]]:
        """Get categories defined for the job (e.g. good or bad).

        Returns:
            A list of category conditions.
        """
        return self._metadata["modelEntries"]

    def get_rule(self, bcid: str) -> rule.RuleDescription:
        """Get a rule description from its bcId.

        Args:
            bcid: Rule bcid.

        Returns:
            A Rule description.
        """
        return self._memory_base.get_rule(bcid)

    def get_rule_list(self, **kwargs) -> rule.RuleDescription:
        """Get a list a of rule descriptions from a list of ids.

        Args:
            **kwargs: Optional page and page_size.

        Returns:
            A list of Rule descriptions.
        """
        return self._get_resource_list(
            rule.RuleDescription, **kwargs, memory_base=self._memory_base
        )
