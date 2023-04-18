import typing as t


class Argument:
    def __init__(self, type: int, value: t.Any):
        self.type = type
        self.value = value
