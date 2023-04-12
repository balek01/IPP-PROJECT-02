import typing
import constants as c
import Instruction


class Frame:

    def __init__(self, scope: int, order: int):
        self.scope = scope
        self.order = order
        self.instList = []

    def add_instr(self, instruction: Instruction) -> None:
        self.instList.append(instruction)

    def pop_frame(self) -> None:
        self.scope = c.TF

    def push_frame(self) -> None:
        self.scope = c.LF
