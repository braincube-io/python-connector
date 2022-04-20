from typing import List, Dict

from braincube_connector import client
from braincube_connector.memory_base.nested_resources.condition_container import ConditionContainer
from braincube_connector.memory_base.nested_resources.event import Event
from braincube_connector.memory_base.nested_resources.period import Period
from braincube_connector.memory_base.nested_resources.variable import VariableDescription


class ModelBuilder(client.Client):

    @staticmethod
    def create_study(self, name: str, target: VariableDescription, period: Period, variables: List[VariableDescription],
                     description: str = '', conditions: ConditionContainer = None, events: List[Event] = None):

        path = "{braincube_path}/studies".format(braincube_path=target.get_memory_base().get_braincube_name())
        header = self._authentication
        body_data = {
            "name": name,
            "description": description,
            "memoryBase": target.get_memory_base().get_metadata(),
            "variableToPredict": target.get_metadata(),
            "period": period.get_metadata(),
            "conditions": [] if conditions is None else conditions.get_metadata(),
            "events": [([] if event is None else event.get_metadata()) for event in events],
            "variables": [var.get_metadata() for var in variables]
        }
        return self.request_ws(path=path, headers=header, body_data=body_data, rtype="POST")
