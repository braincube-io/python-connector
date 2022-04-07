class Variable(object):
    def __init__(
            self, bcid: int, local: str, standard: str, tag: str, unit: str
    ) -> None:
        self.bcid = bcid
        self.local = local
        self.standard = standard
        self.tag = tag
        self.unit = unit


class Condition(object):

    def __init__(
            self, id: int, invert: bool, active: bool, variable: Variable, data_type: str, begin: int or str,
            end: int or str
    ) -> None:
        self.id = id
        self.invert = invert
        self.active = active
        self.variable = variable
        self.data_type = data_type
