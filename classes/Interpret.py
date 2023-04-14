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

##################################### INSTRUCTIONS #####################################

    def __arithmetics(self, i: Instruction, operation):

        arg0 = self._get_variable_from_argument(i.arglist[c.POS_VARIABLE])
        self.__check_variable(arg0, c.ANY, True)

        arg1: Argument = i.arglist[c.POS_ARG1]
        arg2: Argument = i.arglist[c.POS_ARG2]

        if arg1.type == c.VAR:
            arg1: Variable = self._get_variable_from_argument(arg1)
            self.__check_variable(arg1, c.INT)
        if arg2.type == c.VAR:
            arg2: Variable = self._get_variable_from_argument(arg2)
            self.__check_variable(arg2, c.INT)

        # Perform operation
        arg0.type = c.INT
        if operation == c.ADD:
            arg0.value = arg1.value + arg2.value
         #   print(
         #       f"Performed addition to variable: {arg0.name} value is : {arg0.value}")

        if operation == c.SUB:
            arg0.value = arg1.value - arg2.value
        #    print(
        #        f"Performed substraction to variable: {arg0.name} value is : {arg0.value}")

        if operation == c.IDIV:
            if arg2.value == 0:
                e.exit_and_print(e.SEMANTIC_DIVISION_BY_ZERO)
            arg0.value = arg1.value // arg2.value
        #    print(
        #        f"Performed division to variable: {arg0.name} value is : {arg0.value}")

        if operation == c.MUL:
            arg0.value = arg1.value * arg2.value
        #    print(
        #        f"Performed multiplication to variable: {arg0.name} value is : {arg0.value}")

    def __defvar(self, i: Instruction):

        variable: Argument = i.arglist[c.POS_VARIABLE]
        name = variable.value
        frame = self.__get_frame_from__variable_name(name)
        self.__assert_frame_exists(frame)
        if frame.scope == c.GF:
            if(self.g_frame and self.g_frame.get_variable_by_name(name)):
                e.exit_and_print(e.SEMANTIC_VAR_ALREADY_EXISTS)
            else:
                self.g_frame.add_var(Variable(name, None, None))

        # TODO: CORRECT ASSERTION
        if frame.scope == c.TF or frame.scope == c.LF:
            if(self.t_frame.get_variable_by_name(name)):
                e.exit_and_print(e.SEMANTIC_VAR_ALREADY_EXISTS)
            else:
                self.t_frame.add_var(Variable(name, None, None))

    def __move(self, i: Instruction):
        arg0 = self._get_variable_from_argument(i.arglist[c.POS_VARIABLE])
        arg1: Argument = i.arglist[c.POS_ARG1]

        # check existence of variable
        self.__check_variable(arg0, c.ANY, True)
        if arg1.type == c.VAR:
            arg1: Variable = self._get_variable_from_argument(arg1)
            self.__check_variable(arg1, c.ANY, True)
        # perform assignment
        arg0.type = arg1.type
        arg0.value = arg1.value

    def __write(self, i: Instruction):
        arg0: Argument = i.arglist[c.POS_VARIABLE]
        if arg0.type == c.VAR:
            arg0: Variable = self._get_variable_from_argument(arg0)
            self.__check_variable(arg0, c.ANY, True)
        # TODO correct behavior for boolean and nil
        print(arg0.value, end='')

##################################### UTILITY FUNCTIONS #####################################

    def _get_variable_from_argument(self, arg: Argument) -> Variable:
        arg_name = arg.value
        arg_frame: Frame = self.__get_frame_from__variable_name(arg_name)
        if arg_frame is None:
            e.exit_and_print(e.SEMANTIC_FRAME_DOES_NOT_EXIST)
        return arg_frame.get_variable_by_name(arg_name)

    def __assert_frame_exists(self, frame):
        if frame is None:
            e.exit_and_print(e.SEMANTIC_FRAME_DOES_NOT_EXIST)

    def __check_variable(self, variable: Variable, expect_type=c.ANY, nullable=False):
        if variable is None:
            e.exit_and_print(e.SEMANTIC_VAR_DOES_NOT_EXISTS)
        if not nullable and variable.value is None:
            e.exit_and_print(e.SEMANTIC_VAR_VALUE_DOES_NOT_EXISTS)

        if expect_type != c.ANY and expect_type != variable.type:
            e.exit_and_print(e.SEMANTIC_WRONG_OPERAND_TYPE)

    def __get_frame_from__variable_name(self, name) -> Optional[Frame]:
        if (name.startswith("GF")):
            return self.g_frame
        if (name.startswith("LF")):
            return self.l_frame
        if (name.startswith("TF")):
            return self.t_frame
        e.exit_and_print(e.INTERNAL_ERROR)

    def run(self):
        i = next(iter(self.instructions.items()))[1]

        while i:
            if not i:
                break
           # print(i.opcode)
           # i.print_args()
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
                self.__move(instruction)
            case 'NOT':
                pass
            case 'OR':
                pass
            case 'POPFRAME':
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
                self.__write(instruction)
            case _:
                e.exit_and_print(e.INTERNAL_ERROR)
