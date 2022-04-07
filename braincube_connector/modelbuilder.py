from typing import List, Dict

from braincube_connector.bases import base
from braincube_connector.memory_base.nested_resources.period import Period
from braincube_connector.memory_base.nested_resources.variable import VariableDescription


class ModelBuilder(base.Base):

    def create_study(self, name: str, target: VariableDescription, period: Period, variables: List[VariableDescription], description: str = '',  conditions: List[Dict] = [],  ):