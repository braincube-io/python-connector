from typing import List

from braincube_connector import client
from braincube_connector.bases import resource_getter
from braincube_connector.memory_base.nested_resources.condition_container import ConditionContainer
from braincube_connector.memory_base.nested_resources.event import Event
from braincube_connector.memory_base.nested_resources.period import Period
from braincube_connector.memory_base.nested_resources.variable import VariableDescription


class ModelBuilder(resource_getter.ResourceGetter):
    def __init__(self, headers):
        super().__init__()
        self.headers = headers

    def create_study(
            self,
            name: str,
            target: VariableDescription,
            period: Period,
            variables: List[VariableDescription],
            description: str = "",
            conditions: ConditionContainer = None,
            events: List[Event] = None,
    ):
        path = "{braincube_path}/studies".format(braincube_path=self.get_braincube_path())
        body_data = {
            "name": name,
            "description": description,
            "memoryBase": target.get_memory_base().get_metadata(),
            "variableToPredict": target.get_metadata(),
            "period": period.get_metadata(),
            "conditions": [] if conditions is None else conditions.get_metadata(),
            "events": [] if events is None else [event.get_metadata() for event in events],
            "variables": [variable.get_metadata() for variable in variables],
        }
        return client.request_ws(path=path, headers=self.headers, body_data=body_data, rtype="POST")
