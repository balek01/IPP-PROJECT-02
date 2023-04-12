import typing
from classes.Argument import Argument


class Instruction:
    def __init__(self, opcode: str, order: int, ):
        self.opcode = opcode
        self.order = order
        self.arglist = []
        self.next_instr = None

    def add_argument(self, argument: Argument) -> None:
        self.arglist.append(argument)

    def print_args(self) -> None:
        for arg in self.arglist:
            print("Arg.Type: "+str(arg.type)+" Arg.Value: "+str(arg.value))
