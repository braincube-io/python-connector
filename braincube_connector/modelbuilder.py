from typing import List, Dict

import requests

from braincube_connector import client
from braincube_connector.bases import base
from braincube_connector.client import request_ws
from braincube_connector.memory_base.nested_resources.period import Period
from braincube_connector.memory_base.nested_resources.variable import VariableDescription


class ModelBuilder(client.Client):

    @staticmethod
    def create_study(self, name: str, memorybase: MemoryBase, target: VariableDescription, period: Period, variables: List[VariableDescription],
                     description: str = '', conditions: List[Dict] = [], ):
        path = "?"
        header = "?"
        body_data = {
            "name": name,
            "description": description,
            "memoryBase": memorybase
        }
        study = self.request_ws(path=path, headers=header, body_data=body_data)
