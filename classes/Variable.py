import typing as t
import constants as c


class Variable:
    def __init__(self, name: str, type=None, value=None):
        self.name = name
        self.type = type
        self.value = value

    def change_name_scope_to(self, scope: int) -> None:
        if scope == c.TF:
            self.name = "TF" + self.name[2:]
        if scope == c.LF:
            self.name = "LF" + self.name[2:]
        if scope == c.GF:
            self.name = "GF" + self.name[2:]
