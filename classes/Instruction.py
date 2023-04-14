from typing import List, Optional
from classes.Argument import Argument


class Instruction:
    def __init__(self, opcode: str, order: int):
        self.opcode: str = opcode
        self.order: int = order
        self.arglist: List[Argument] = []
        self.next_instr: Optional[Instruction] = None

    def add_argument(self, argument: Argument) -> None:
        self.arglist.append(argument)

    def print_args(self) -> None:
        for arg in self.arglist:
            print("Arg.Type: "+str(arg.type)+" Arg.Value: "+str(arg.value))
