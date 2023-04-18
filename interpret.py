import sys
from parseargs import parse_args
import xmlparser as xp
import xml.etree.ElementTree as ET
from classes.Interpret import Interpret
from classes.Instruction import Instruction
from classes.Argument import Argument
from classes.Frame import Frame
import constants as c
import errors as e


def prerun(interpret, xml):
    instruction = xml[0]

    last_instruction = create_instruction(instruction)

    for instruction in xml:
        new_instruction = create_instruction(instruction)

        for arg in instruction:
            newargument = create_argument(arg)
            new_instruction.add_argument(newargument)

        last_instruction.next_instr = new_instruction
        last_instruction = new_instruction
        interpret.add_instruction(new_instruction)


def setup_labels(xml):
    labels = {}
    for instruction in xml:
        set_label(instruction, labels)
    return labels


def set_label(instruction, labels: dict):
    opcode = instruction.attrib.get("opcode").upper()
    if opcode == "LABEL":
        label = instruction.find('*').text
        if label not in labels:
            order = int(instruction.attrib.get("order"))
            labels[label] = order
        else:
            e.exit_and_print(e.SEMANTIC_LABEL_ALREADY_EXISTS)


def create_instruction(instruction):
    order = int(instruction.attrib.get("order"))
    opcode = instruction.attrib.get("opcode").upper()
    return Instruction(opcode, order)


def create_argument(arg):
    type = arg.attrib.get("type")
    type = str_to_type(type)
    value = value_to_type(type, arg.text)
    return Argument(type, value)


def str_to_type(str):
    match str:
        case 'string':
            return c.STRING
        case 'bool':
            return c.BOOL
        case 'int':
            return c.INT
        case 'nil':
            return c.NIL
        case 'label':
            return c.LABEL
        case 'type':
            return c.TYPE
        case "var":
            return c.VAR
        case _:
            e.exit_and_print(e.INTERNAL_ERROR)


def value_to_type(type, value: str):

    match type:
        case c.STRING | c.LABEL | c.VAR:
            return value
        case c.BOOL:
            if value == 'true':
                return True
            else:
                return False
        case c.INT:
            return int(value)
        case c.NIL:
            return None
        case c.TYPE:
            return str_to_type(value)
        case _:
            e.exit_and_print(e.INTERNAL_ERROR)


def main():

    inputfile, source = parse_args()
    if source is None:
        is_file = False
        source = sys.stdin.read()
    else:
        is_file = True

    xml = xp.xml_parser(source, is_file)

    labels = setup_labels(xml)
    interpret = Interpret(labels, inputfile)
    prerun(interpret, xml)
    interpret.run()


if __name__ == '__main__':
    main()
