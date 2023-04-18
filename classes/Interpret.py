from classes.Instruction import Instruction
from classes.Frame import Frame
from classes.Variable import Variable
from classes.Argument import Argument
import errors as e
import constants as c
from typing import Optional, Dict
import re
import queue


class Interpret:
    def __init__(self, labels, input):
        self.input = input
        self.instructions: Dict[int, Instruction] = {}
        self.g_frame = Frame(c.GF)
        self.t_frame: Optional[Frame] = None
        self.l_frame: Optional[Frame] = None
        self.lables: Dict[str, int] = labels
        self.l_frames = queue.LifoQueue()
        self.call_stack = queue.LifoQueue()

    def add_instruction(self, instruction: Instruction) -> None:
        self.instructions[instruction.order] = instruction

##################################### INSTRUCTIONS #####################################

    def __arithmetics(self, i: Instruction, operation):

        allowed_types = [c.INT]
        arg0 = self.__parse_argument(i, c.POS_VARIABLE)
        arg1 = self.__parse_argument(i, c.POS_ARG1, allowed_types)
        arg2 = self.__parse_argument(i, c.POS_ARG2, allowed_types)

        # Perform operation
        arg0.type = c.INT
        if operation == c.ADD:
            arg0.value = arg1.value + arg2.value

        if operation == c.SUB:
            arg0.value = arg1.value - arg2.value

        if operation == c.IDIV:
            if arg2.value == 0:
                e.exit_and_print(e.SEMANTIC_DIVISION_BY_ZERO)
            arg0.value = arg1.value // arg2.value

        if operation == c.MUL:
            arg0.value = arg1.value * arg2.value

    def __call(self, i: Instruction) -> int:
        order = self.__jump(i)
        self.call_stack.put(i.next_instr)
        return order

    def __compare(self, i: Instruction, operation):

        allowed_types = [c.BOOL, c.STRING, c.INT, c.NIL]
        arg0 = self.__parse_argument(i, c.POS_VARIABLE)
        arg1 = self.__parse_argument(i, c.POS_ARG1, allowed_types)
        arg2 = self.__parse_argument(i, c.POS_ARG2, allowed_types)

        # NIL can be used if any type
        if arg1.type != c.NIL and arg2.type != c.NIL:
            self.__assert_variable_has_same_type(arg1, arg2)

        result = False
        # type check only to prevent nil and string "nil"
        if operation == c.EQ and arg1.value == arg2.value and arg1.type == arg2.type:
            result = True

        # nil is allowed only in EQ expressions
        elif arg1.type == c.NIL or arg2.type == c.NIL:
            e.exit_and_print(e.SEMANTIC_WRONG_OPERAND_TYPE)

         # Perform operation
        if operation == c.GT and arg1.value > arg2.value:
            result = True
        if operation == c.LT and arg1.value < arg2.value:
            result = True

        arg0.type = c.BOOL
        arg0.value = result

    def __concat(self, i: Instruction):

        allowed_types = [c.STRING]
        arg0 = self.__parse_argument(i, c.POS_VARIABLE)
        arg1 = self.__parse_argument(i, c.POS_ARG1, allowed_types)
        arg2 = self.__parse_argument(i, c.POS_ARG2, allowed_types)

        # Perform operation
        arg0.type = c.STRING
        arg0.value = arg1.value + arg2.value

    def __createframe(self, i: Instruction):
        if self.t_frame == None:
            self.t_frame = Frame(c.TF)
        else:
            self.t_frame = Frame(c.TF)

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

    def __exit(self, i: Instruction):
        arg0: Argument = i.arglist[c.POS_VARIABLE]
        if arg0.type == c.VAR:
            arg0: Variable = self.__get_variable_from_argument(arg0)
            self.__check_variable(arg0, c.INT, False)
        if 0 <= arg0.value <= 49:
            exit(arg0.value)
        else:
            e.exit_and_print(e.SEMANTIC_INCORRECT_EXIT_VALUE)

    def __getchar(self, i: Instruction):

        arg0 = self.__parse_argument(i, c.POS_VARIABLE)
        arg1 = self.__parse_argument(i, c.POS_ARG1, c.STRING)
        arg2 = self.__parse_argument(i, c.POS_ARG2, c.INT)
        out = self.__decimal_escape_to_hex(arg1.value)
        if len(out)-1 < arg2.value or -len(out) > arg2.value:
            e.exit_and_print(e.SEMANTIC_INDEX_OUT_OF_STRING)

        arg0.value = out[arg2.value]
        arg0.type = c.STRING

    def __int2char(self, i: Instruction):
        arg0 = self.__parse_argument(i, c.POS_VARIABLE)
        arg1 = self.__parse_argument(i, c.POS_ARG1, c.INT)
        arg0.type = c.STRING
        try:
            arg0.value = chr(arg1.value)
        except ValueError:
            e.exit_and_print(e.SEMANTIC_INT_2_STR_VALUE_ERROR)

    def __stri2int(self, i: Instruction):
        arg0 = self.__parse_argument(i, c.POS_VARIABLE)
        arg1 = self.__parse_argument(i, c.POS_ARG1, c.STRING)
        arg2 = self.__parse_argument(i, c.POS_ARG2, c.INT)
        out = self.__decimal_escape_to_hex(arg1.value)

        if len(out)-1 < arg2.value or -len(out) > arg2.value:
            e.exit_and_print(e.SEMANTIC_INDEX_OUT_OF_STRING)

        arg0.type = c.INT
        try:
            arg0.value = ord(out[arg2.value])
        except ValueError:
            e.exit_and_print(e.SEMANTIC_INT_2_STR_VALUE_ERROR)

    def __strlen(self, i: Instruction):
        arg0 = self.__parse_argument(i, c.POS_VARIABLE)
        arg1 = self.__parse_argument(i, c.POS_ARG1, c.STRING)
        arg0.type = c.INT
        arg0.value = len(arg1.value)

    def __jump(self, i: Instruction) -> int:
        arg0 = i.arglist[c.POS_VARIABLE]

        if arg0.value not in self.lables:
            e.exit_and_print(e.SEMANTIC_LABEL_DOES_NOT_EXISTS)
        else:
            return self.lables[arg0.value]

    def __jumpif(self, i: Instruction, operation) -> int:
        allowed_types = [c.BOOL, c.STRING, c.INT, c.NIL]
        arg0 = i.arglist[c.POS_VARIABLE]
        if arg0.value not in self.lables:
            e.exit_and_print(e.SEMANTIC_LABEL_DOES_NOT_EXISTS)

        arg1 = self.__parse_argument(i, c.POS_ARG1, allowed_types)
        arg2 = self.__parse_argument(i, c.POS_ARG2, allowed_types)
        result = False
        if arg1.type != c.NIL and arg2.type != c.NIL:
            self.__assert_variable_has_same_type(arg1, arg2)

        # type check only to prevent nil and string "nil"
        if operation == c.EQ and arg1.value == arg2.value and arg1.type == arg2.type:
            result = True
        if operation == c.NEQ and arg1.value != arg2.value and arg1.type == arg2.type:
            result = True
        if result:
            return self.lables[arg0.value]
        else:
            return i.next_instr.order

    def __logical(self, i: Instruction, operation):

        allowed_types = [c.BOOL]
        arg0 = self.__parse_argument(i, c.POS_VARIABLE)
        arg1 = self.__parse_argument(i, c.POS_ARG1, allowed_types)

        # NOT has only one source argument
        if operation != c.NOT:
            arg2 = self.__parse_argument(i, c.POS_ARG2, allowed_types)

         # Perform operation
        arg0.type = c.BOOL
        if operation == c.NOT:
            arg0.value = not arg1.value
        if operation == c.AND:
            arg0.value = arg1.value and arg2.value
        if operation == c.OR:
            arg0.value = arg1.value or arg2.value

    def __move(self, i: Instruction):
        arg0 = self.__parse_argument(i, c.POS_VARIABLE)
        arg1 = self.__parse_argument(i, c.POS_ARG1, c.ANY, True)

        # Perform assignment
        arg0.type = arg1.type
        arg0.value = arg1.value

    def __popframe(self):
        if self.l_frame is not None:
            self.t_frame: Frame = self.l_frames.get()
            self.t_frame.change_scope_to(c.TF)
            if self.l_frames.qsize() > 0:
                self.l_frame = self.l_frames.get()
                self.l_frames.put(self.l_frame)
            else:
                self.l_frame = None
        else:
            e.exit_and_print(e.SEMANTIC_FRAME_DOES_NOT_EXIST)

    def __pushframe(self):
        if self.t_frame is not None:
            self.t_frame.change_scope_to(c.LF)
            self.l_frames.put(self.t_frame)
            self.l_frame = self.t_frame
            self.t_frame = None
        else:
            e.exit_and_print(e.SEMANTIC_FRAME_DOES_NOT_EXIST)

    def __read(self, i: Instruction):
        arg0 = self.__parse_argument(i, c.POS_VARIABLE)
        arg1 = self.__parse_argument(i, c.POS_ARG1, c.TYPE)
        if self.input is not None:
            file = open(self.input, "r")
            content: str = file.read()
            file.close()
        else:
            content: str = input()
        type = arg1.value
        match arg1.value:
            case c.BOOL:
                content = content.lower()
                pattern = r"^true$"
                if not re.match(pattern, content):
                    content = "false"
            case c.INT:
                pattern = r"^([-+]?\d+)$"
                if not re.match(pattern, content):
                    content = "nil"
                    type = c.NIL
            case c.NIL:
                content = "nil"

        arg0.value = content
        arg0.type = type

    def __return(self) -> Instruction:
        if self.call_stack.qsize() > 0:
            return self.call_stack.get()
        else:
            e.exit_and_print(e.SEMANTIC_RETURN_STACK_EMPTY)

    def __setchar(self, i: Instruction):
        arg0 = self.__parse_argument(i, c.POS_VARIABLE)
        arg1 = self.__parse_argument(i, c.POS_ARG1, c.INT)
        arg2 = self.__parse_argument(i, c.POS_ARG2, c.STRING)

        arg0_hex = self.__decimal_escape_to_hex(arg0.value)
        arg2_hex = self.__decimal_escape_to_hex(arg2.value)

        if len(arg0_hex)-1 < arg1.value or -len(arg0_hex) > arg1.value:
            e.exit_and_print(e.SEMANTIC_INDEX_OUT_OF_STRING)
        arg0_list = list(arg0_hex)
        arg2_list = list(arg2_hex)
        if len(arg2_list) != 0:
            arg0_list[arg1.value] = arg2_list[0]
        else:
            arg0_list[arg1.value] = ""
        arg0.value = "".join(arg0_list)

    def __out(self, i: Instruction, operation: int):
        arg0: Argument = i.arglist[c.POS_VARIABLE]

        if arg0.type == c.VAR:
            arg0: Variable = self.__get_variable_from_argument(arg0)
            self.__check_variable(arg0, c.ANY, True)
        if arg0.type == c.NIL:
            print('', end='', file=operation)
        elif arg0.type == c.BOOL:
            print(str(arg0.value).lower(), end='', file=operation)
        elif arg0.type == c.STRING:
            out = self.__decimal_escape_to_hex(arg0.value)
            print(out, end='', file=operation)
        else:
            print(arg0.value, end='', file=operation)

    def __type(self, i: Instruction):
        allowed_types = [c.BOOL, c.INT, c.NIL, c.STRING, None]
        arg0 = self.__parse_argument(i, c.POS_VARIABLE)
        arg1 = self.__parse_argument(i, c.POS_ARG1, allowed_types, True)
        match arg1.type:
            case c.BOOL:
                type = "bool"
            case c.INT:
                type = "int"
            case c.NIL:
                type = "nil"
            case c.STRING:
                type = "string"
            case None:
                type = ""
        arg0.type = c.TYPE
        arg0.value = type

        ##################################### UTILITY FUNCTIONS #####################################

    def __decimal_escape_to_hex(self, string):
        return re.sub(
            r"\\(\d\d\d)",
            lambda x: chr(int(x.group(1), 10)),
            string
        )

    def __get_variable_from_argument(self, arg: Argument) -> Variable:
        arg_name = arg.value
        arg_frame: Frame = self.__get_frame_from__variable_name(arg_name)
        self.__assert_frame_exists(arg_frame)
        return arg_frame.get_variable_by_name(arg_name)

    def __assert_frame_exists(self, frame):
        if frame is None:
            e.exit_and_print(e.SEMANTIC_FRAME_DOES_NOT_EXIST)

    def __parse_argument(self, i: Instruction, position: int, allowed_types=c.ANY, can_undefined=False) -> Variable:
        if position == c.POS_VARIABLE:
            arg = self.__get_variable_from_argument(i.arglist[c.POS_VARIABLE])
            self.__check_variable(arg, allowed_types, True)
        else:
            arg: Argument = i.arglist[position]
            if arg.type == c.VAR:
                arg: Variable = self.__get_variable_from_argument(arg)
                self.__check_variable(arg, allowed_types, can_undefined)

        return arg

    def __assert_variable_has_same_type(self, var1, var2):
        if var1.type != var2.type:
            e.exit_and_print(e.SEMANTIC_SAME_TYPE_ERROR)

    def __check_variable(self, variable: Variable, expect_types=c.ANY, can_undefined=False):
        if not isinstance(expect_types, list):
            expect_types = [expect_types]
        if variable is None:
            e.exit_and_print(e.SEMANTIC_VAR_DOES_NOT_EXISTS)
        if not can_undefined and variable.value is None:
            e.exit_and_print(e.SEMANTIC_VAR_VALUE_DOES_NOT_EXISTS)

        if c.ANY not in expect_types and variable.type not in expect_types:
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
            i = self.__run_op_code(i)

    def __run_op_code(self, instruction: Instruction) -> Instruction:
        opcode = instruction.opcode
        i = instruction.next_instr
        match opcode:
            case 'ADD':
                self.__arithmetics(instruction, c.ADD)
            case 'AND':
                self.__logical(instruction, c.AND)
            case 'BREAK':
                pass
            case 'CALL':
                order = self.__call(instruction)
                i = self.instructions[order]
            case 'CONCAT':
                self.__concat(instruction)
            case 'CREATEFRAME':
                self.__createframe(instruction)
            case 'DEFVAR':
                self.__defvar(instruction)
            case 'DPRINT':
                self.__out(instruction, c.DPRINT)
            case 'EQ':
                self.__compare(instruction, c.EQ)
            case 'EXIT':
                self.__exit(instruction)
            case 'GETCHAR':
                self.__getchar(instruction)
            case 'GT':
                self.__compare(instruction, c.GT)
            case 'IDIV':
                self.__arithmetics(instruction, c.IDIV)
            case 'INT2CHAR':
                self.__int2char(instruction)
            case 'JUMP':
                order = self.__jump(instruction)
                i = self.instructions[order]
            case 'JUMPIFEQ':
                order = self.__jumpif(instruction, c.EQ)
                i = self.instructions[order]
            case 'JUMPIFNEQ':
                order = self.__jumpif(instruction, c.NEQ)
                i = self.instructions[order]
            case 'LABEL':
                # DONE
                pass
            case 'LT':
                self.__compare(instruction, c.LT)
            case 'MUL':
                self.__arithmetics(instruction, c.MUL)
            case 'MOVE':
                self.__move(instruction)
            case 'NOT':
                self.__logical(instruction, c.NOT)
            case 'OR':
                self.__logical(instruction, c.OR)
            case 'POPFRAME':
                self.__popframe()
            case 'PUSHFRAME':
                self.__pushframe()
            case 'POPS' | 'PUSHS':
                pass
            case 'READ':
                self.__read(instruction)
            case 'RETURN':
                i = self.__return()
            case 'SETCHAR':
                self.__setchar(instruction)
            case 'STRI2INT':
                self.__stri2int(instruction)
            case 'STRLEN':
                self.__strlen(instruction)
            case 'SUB':
                self.__arithmetics(instruction, c.SUB)
            case 'TYPE':
                self.__type(instruction)
            case 'WRITE':
                self.__out(instruction, c.WRITE)
            case _:
                e.exit_and_print(e.INTERNAL_ERROR)
        return i
