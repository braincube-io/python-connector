from typing import Dict, Any, Optional

from braincube_connector import constants
from braincube_connector.memory_base.nested_resources import mb_child, condition_container


class Study:
    """Study from ModelBuilder"""

    def __init__(self, name, description, memorybase, variable_to_predict, period, condition, events, variables):
        self.name = name
        self.description = description
        self.memorybase = memorybase
        self.variable_to_predict = variable_to_predict
        self.period = period
        self.condition = condition
        self.events = events
        self.variables = variables

