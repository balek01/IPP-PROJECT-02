import typing
import Argument


class Instruction:
    def __init__(self, opcode: str, order: int, ):
        self.opcode = opcode
        self.order = order
        self.arglist = []

    def add_argument(self, argument: Argument) -> None:
        self.arglist.append(argument)
