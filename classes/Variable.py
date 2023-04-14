import typing as t


class Variable:
    def __init__(self, name: str, type=None, value=None):
        self.name = name
        self.type = type
        self.value = value
