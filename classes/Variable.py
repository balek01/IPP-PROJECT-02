import typing as t


class Variable:
    def __init__(self, name: str, type: type, value: t.Any):
        self.name = name
        self.type = type
        self.value = value

    def get_name(self) -> str:
        return self.name

    def get_value(self) -> t.Any:
        return self.value

    def get_type(self) -> type:
        return self.type
