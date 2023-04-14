from classes.Instruction import Instruction
from classes.Frame import Frame
from classes.Variable import Variable
from classes.Argument import Argument
import errors as e
import constants as c
from typing import Optional, Dict


class Interpret:
    def __init__(self):
        self.instructions: Dict[int, Instruction] = {}
        self.g_frame = Frame(c.GF)
        self.t_frame: Optional[Frame] = None
        self.l_frame: Optional[Frame] = None

    def add_instruction(self, instruction: Instruction) -> None:
        self.instructions[instruction.order] = instruction

    def __arithmetics(self, i: Instruction, operation):

        # check if variable exists and frame too
        arg0 = self._get_variable_from_argument(i.arglist[c.POS_VARIABLE])
        if arg0 is None:
            e.exit_and_print(e.SEMANTIC_VAR_DOES_NOT_EXISTS)

        arg1: Argument = i.arglist[c.POS_ARG1]
        arg2: Argument = i.arglist[c.POS_ARG2]

        if arg1.type == c.VAR:
            arg1: Variable = self._get_variable_from_argument(arg1)
            if arg1 is None:
                e.exit_and_print(e.SEMANTIC_VAR_DOES_NOT_EXISTS)

        if arg2.type == c.VAR:
            arg2: Variable = self._get_variable_from_argument(arg2)
            if arg2 is None:
                e.exit_and_print(e.SEMANTIC_VAR_DOES_NOT_EXISTS)
        # Perform operation
        arg0.type = c.INT
        if operation == c.ADD:
            arg0.value = arg1.value + arg2.value
            print(
                f"Performed addition to variable: {arg0.name} value is : {arg0.value}")

        if operation == c.SUB:
            arg0.value = arg1.value - arg2.value
            print(
                f"Performed substraction to variable: {arg0.name} value is : {arg0.value}")

        if operation == c.IDIV:
            if arg2.value == 0:
                e.exit_and_print(e.SEMANTIC_DIVISION_BY_ZERO)
            arg0.value = arg1.value // arg2.value
            print(
                f"Performed division to variable: {arg0.name} value is : {arg0.value}")

        if operation == c.MUL:
            arg0.value = arg1.value * arg2.value
            print(
                f"Performed multiplication to variable: {arg0.name} value is : {arg0.value}")

    def __defvar(self, i):

        variable: Argument = i.arglist[c.POS_VARIABLE]
        name = variable.value
        frame = self.__get_frame_from__variable_name(name)

        if frame.scope == c.GF:
            if(self.g_frame and self.g_frame.get_variable_by_name(name)):
                e.exit_and_print(e.SEMANTIC_VAR_ALREADY_EXISTS)
            else:
                self.g_frame.add_var(Variable(name, None, None))

        if frame.scope == c.TF or frame.scope == c.LF:
            self.__assert_frame_exists(frame.scope)
            if(self.t_frame.get_variable_by_name(name)):
                e.exit_and_print(e.SEMANTIC_VAR_ALREADY_EXISTS)
            else:
                self.t_frame.add_var(Variable(name, None, None))

    def _get_variable_from_argument(self, arg: Argument) -> Variable:
        arg_name = arg.value
        arg_frame: Frame = self.__get_frame_from__variable_name(arg_name)
        if arg_frame is None:
            e.exit_and_print(e.SEMANTIC_FRAME_DOES_NOT_EXIST)
        return arg_frame.get_variable_by_name(arg_name)

    def __assert_frame_exists(self, frame_type):
        if frame_type == c.LF and self.l_frame is None:
            e.exit_and_print(e.SEMANTIC_FRAME_DOES_NOT_EXIST)

        if frame_type == c.TF and self.t_frame is None:
            e.exit_and_print(e.SEMANTIC_FRAME_DOES_NOT_EXIST)

    def __check_variable_by_name(self, name, expect_type=c.ANY):
        # TODO: FINISH THIS AND USE IT !!!!
        frame = self.__get_frame_from__variable_name(name)
        if frame.scope == c.LF:
            self.__assert_frame_exists(c.LF)
        if frame.scope == c.TF:
            self.__assert_frame_exists(c.TF)
        if expect_type != c.ANY and expect_type != type:
            e.exit_and_print(e.SEMANTIC_WRONG_OPERAND_TYPE)

    def __get_frame_from__variable_name(self, name) -> Frame:
        if (name.startswith("GF")):
            return self.g_frame
        if (name.startswith("LF")):
            return self.l_frame
        if (name.startswith("TF")):
            return self.t_frame

    def run(self):
        i = next(iter(self.instructions.items()))[1]

        while i:
            if not i:
                break
            print(i.opcode)
            i.print_args()
            self.__run_op_code(i)
            i = i.next_instr

    def __run_op_code(self, instruction):
        opcode = instruction.opcode
        match opcode:
            case 'ADD':
                self.__arithmetics(instruction, c.ADD)
            case 'AND':
                pass
            case 'BREAK':
                pass
            case 'CALL':
                pass
            case 'CONCAT':
                pass
            case 'CREATEFRAME':
                pass
            case 'DEFVAR':
                self.__defvar(instruction)
            case 'DPRINT':
                pass
            case 'EQ':
                pass
            case 'EXIT':
                pass
            case 'GETCHAR':
                pass
            case 'GT':
                pass
            case 'IDIV':
                self.__arithmetics(instruction, c.IDIV)
            case 'INT2CHAR':
                pass
            case 'JUMP':
                pass
            case 'JUMPIFEQ':
                pass
            case 'JUMPIFNEQ':
                pass
            case 'LABEL':
                pass
            case 'LT':
                pass
            case 'MUL':
                self.__arithmetics(instruction, c.MUL)
            case 'MOVE':
                pass
            case 'NOT':
                pass
            case 'OR':
                pass
            case 'POPFAME':
                pass
            case 'PUSHFRAME':
                pass
            case 'POPS':
                pass
            case 'PUSHS':
                pass
            case 'READ':
                pass
            case 'RETURN':
                pass
            case 'SETCHAR':
                pass
            case 'STRI2INT':
                pass
            case 'STRLEN':
                pass
            case 'SUB':
                self.__arithmetics(instruction, c.SUB)
            case 'TYPE':
                pass
            case 'WRITE':
                pass
            case _:
                e.exit_and_print(e.INTERNAL_ERROR)
