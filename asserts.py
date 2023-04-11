import errors as e
import re
import assert_utils as au


def assert_opcode_value(instruction):
    opcode = instruction.attrib.get("opcode").upper()

    match opcode:
        case 'ADD' | 'SUB' | 'MUL' | 'IDIV':
            au.assert_arithmetic(instruction)
        case 'LT' | 'GT' | 'EQ':
            au.assert_compare(instruction)
        case 'AND' | 'OR':
            au.assert_logical(instruction)
        case 'NOT':
            au.assert_not(instruction)
        case 'INT2CHAR':
            au.assert_i2ch(instruction)
        case 'TYPE' | 'STRLEN':
            # TODO:
            pass
        case 'STRI2INT' | 'GETCHAR':
            au.assert_s2i_gchar(instruction)
        case 'MOVE':
            au.assert_move(instruction)
        case 'POPS' | 'DEFVAR':
            au.assert_only_var(instruction)
        case 'CREATEFRAME' | 'PUSHFRAME' | 'POPFRAME' | 'RETURN' | 'BREAK':
            au.assert_no_args(instruction)
        case 'WRITE' | 'DPRINT' | 'PUSHS':
            au.assert_only_sym(instruction)
        case 'JUMP' | 'CALL' | 'LABEL':
            au.assert_only_label(instruction)
        case 'READ':
            au.assert_read(instruction)
        case 'CONCAT':
            au.assert_concat(instruction)
        case 'SETCHAR':
            au.assert_schar(instruction)
        case 'JUMPIFEQ' | 'JUMPIFNEQ':
            au.assert_jumpif(instruction)
        case 'EXIT':
            au.assert_exit(instruction)
        case _:
            e.exit_and_print(e.ASSERT_OPCODE_VALUE_ERROR)
