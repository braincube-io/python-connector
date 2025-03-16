from braincube_connector.memory_base.nested_resources.study import Study

test_data = {
    "name": "string",
    "description": "string",
    "memoryBase": {
        "uuid": "22992403-1116-4e57-b338-16839f421c7f",
        "id": 20,
        "referenceDateId": 200001
    },
    "variableToPredict": {
        "bcId": 200001,
        "local": "local name",
        "standard": "standard name",
        "tag": "tag name",
        "unit": "°C"
    },
    "period": {
        "begin": 0,
        "end": 0,
        "periodUnitType": "HOUR",
        "quantity": 0,
        "calendarQuantity": 0,
        "offset": 0,
        "offsetQuantity": 0
    },
    "conditions": [
        {
            "dataType": "NUMERICAL",
            "min": 0,
            "max": 10
        },
        {
            "dataType": "DATETIME",
            "beginDate": "2021-07-20T12:20:24.641Z",
            "endDate": "2021-07-21T12:20:24.641Z"
        },
        {
            "dataType": "DISCRETE",
            "modalities": [
                "PRODUCT A"
            ]
        }
    ],
    "events": {
        "id": 1,
        "positiveEvents": [
            {
                "id": 1,
                "uuid": "3d71d567-9bf6-41eb-842c-b45be156b274",
                "name": "event name",
                "conditions": [
                    {
                        "dataType": "NUMERICAL",
                        "min": 0,
                        "max": 10
                    },
                    {
                        "dataType": "DATETIME",
                        "beginDate": "2021-07-20T12:20:24.641Z",
                        "endDate": "2021-07-21T12:20:24.641Z"
                    },
                    {
                        "dataType": "DISCRETE",
                        "modalities": [
                            "PRODUCT A"
                        ]
                    }
                ]
            }
        ],
        "negativeEvents": [
            {
                "id": 1,
                "uuid": "3d71d567-9bf6-41eb-842c-b45be156b274",
                "name": "event name",
                "conditions": [
                    {
                        "dataType": "NUMERICAL",
                        "min": 0,
                        "max": 10
                    },
                    {
                        "dataType": "DATETIME",
                        "beginDate": "2021-07-20T12:20:24.641Z",
                        "endDate": "2021-07-21T12:20:24.641Z"
                    },
                    {
                        "dataType": "DISCRETE",
                        "modalities": [
                            "PRODUCT A"
                        ]
                    }
                ]
            }
        ]
    },
    "variables": [
        {
            "bcId": 200001,
            "local": "local name",
            "standard": "standard name",
            "tag": "tag name",
            "unit": "°C"
        }
    ]
}


class ModelBuilder:
    """Monitoring class to use ModelBuilder functions"""

    @staticmethod
    def create_study(study_data):
        name = study_data["name"]
        description = study_data["description"]
        variable_to_predict = study_data["variableToPredict"]
        period = study_data["period"]
        conditions = study_data["conditions"]
        events = study_data["events"]
        variables = study_data["variables"]

        new_study = Study(name=name, description=description, variable_to_predict=variable_to_predict,
                          variables=variables, period=period, condition=conditions, events=events)


