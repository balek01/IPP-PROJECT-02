from typing import List, Optional
import constants as c
from classes.Instruction import Instruction
from classes.Variable import Variable


class Frame:

    def __init__(self, scope: int):
        self.scope = scope
        self.var_list: List[Variable] = []

    def add_var(self, variable: Variable) -> None:
        self.var_list.append(variable)

    def get_variable_by_name(self, name: str) -> Optional[Variable]:
        for v in self.var_list:
            if v.name == name:
                return v
        return None

    def change_scope_to(self, scope: int) -> None:
        self.scope = scope
        for var in self.var_list:
            var.change_name_scope_to(scope)
