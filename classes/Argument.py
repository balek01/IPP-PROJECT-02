import typing as t


class Argument:
    def __init__(self, type: int, value: t.Any):
        self.type = type
        self.value = value

    def get_value(self):
        return self.value

    def get_type(self):
        return self.type
