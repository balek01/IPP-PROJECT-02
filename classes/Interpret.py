from classes.Instruction import Instruction


class Interpret:
    def __init__(self):
        self.codepointer = 0
        self.instructions = {}

    def get_code_pointer(self):
        return self.codepointer

    def increment_code_pointer(self):
        return self.codepointer

    def set_code_pointer(self, newcp):
        self.codepointer = newcp

    def add_instruction(self, instruction: Instruction) -> None:
        self.instructions[instruction.order] = instruction

    def run(self):
        actual = next(iter(self.instructions.items()))[1]

        while actual.next_instr:

            print(actual.opcode)
            actual.print_args()
            actual = actual.next_instr
