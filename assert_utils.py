import errors as e
import asserts as a
import re

symbol = ["var", "int", "bool", "string", "float", "nil"]


def assert_arithmetic(instruction):
    assert_arg_count(instruction, 3)
    assert_variable(instruction)
    assert_types_offset(instruction, ["int", "var"])


def assert_compare(instruction):

    allowedTypes = ["int", "bool", "string", "var"]
    assert_arg_count(instruction, 3)
    assert_variable(instruction)
    assert_types_offset(instruction, allowedTypes)
    assert_same_type(instruction, 1)


def assert_logical(instruction):
    allowedType = ["bool", 'var']
    assert_arg_count(instruction, 3)
    assert_variable(instruction)
    assert_types_offset(instruction, allowedType)


def assert_not(instruction):
    allowedType = ["bool", "var"]
    assert_arg_count(instruction, 2)
    assert_variable(instruction)
    assert_types_offset(instruction, allowedType)


def assert_i2ch(instruction):
    allowedType = ["int", "var"]
    assert_arg_count(instruction, 2)
    assert_variable(instruction)
    assert_types_offset(instruction, allowedType)


def assert_s2i_gchar(instruction):
    assert_arg_count(instruction, 3)
    assert_variable(instruction)
    assert_types_offset(instruction, ["string", "var"], 2, 3)
    assert_types_offset(instruction, ["int", "var"], 3, 4)


def assert_move(instruction):
    assert_arg_count(instruction, 2)
    assert_variable(instruction)
    assert_types_offset(instruction, symbol, 1)


def assert_only_var(instruction):
    assert_arg_count(instruction, 1)
    assert_variable(instruction)


def assert_no_args(instruction):
    assert_arg_count(instruction, 0)


def assert_only_sym(instruction):
    assert_arg_count(instruction, 1)
    assert_types_offset(instruction, symbol)


def assert_only_label(instruction):
    allowedType = "label"
    assert_arg_count(instruction, 1)
    assert_types_offset(instruction, allowedType, 0)


def assert_read(instruction):
    allowedType = "type"  # this is correct
    assert_arg_count(instruction, 2)
    assert_types_offset(instruction, allowedType)


def assert_concat(instruction):
    allowedTypes = ["string", "var"]
    assert_arg_count(instruction, 3)
    assert_variable(instruction)
    assert_types_offset(instruction, allowedTypes)


def assert_schar(instruction):
    assert_arg_count(instruction, 3)
    assert_variable(instruction)
    assert_types_offset(instruction, ["int", "var"], 1, 2)
    assert_types_offset(instruction, ["string", "var"], 2, 3)


def assert_jumpif(instruction):
    assert_arg_count(instruction, 3)
    assert_types_offset(instruction, "label", 0, 1)
    assert_same_type(instruction, 1)


def assert_exit(instruction):
    assert_arg_count(instruction, 1)
    assert_types_offset(instruction, ["int", "var"], 0)


def assert_arg_value_matches_type(argument):
    type = argument.attrib.get("type")
    regex = get_regex(type)
    #print(type, regex, argument.text)
    if argument.text is None:
        argument.text = ""
    if not re.search(regex, argument.text):
        e.exit_and_print(e.ASSERT_TYPE_DOESNT_MATCH_VALUE_ERROR)

############################### utils of utils ###############################


def get_regex(type):

    var = r'^((LF|GF|TF)@(([_\-;$&%*!?]|[A-Z]|[a-z]|[áčďéěíňóřšťůúýžÁČĎÉĚÍŇÓŘŠŤŮÚÝŽ]))+([_\-$&%*!?]|[A-Z]|[a-z]|[0-9]|[áčďéěíňóřšťůúýžÁČĎÉĚÍŇÓŘŠŤŮÚÝŽ])*)$'
    int = r"^([-+]?\d+)$"
    bool = r'(^(false|true)$)'
    label = r'^([_\-$&%*!?]|[A-Z]|[a-z]|[0-9])+$'
    str = r'^(?:[^\\#\s]|\\(?:0[0-9]{2}|1[0-9]{2}|2[0-9][0-9]|3[0-2]|[35]5|92))*$'
    nil = r'^nil$'
    typeregex = r'^(int|string|bool|nil|label)$'

    match type:
        case 'int':
            return int
        case 'bool':
            return bool
        case 'label':
            return label
        case 'string':
            return str
        case 'var':
            return var
        case 'nil':
            return nil
        case 'type':
            return typeregex
        case _:
            e.exit_and_print(e.INTERNAL_ERROR)


def assert_opcode(instruction):
    assert_attribute(instruction, "opcode")
    a.assert_opcode_value(instruction)


def assert_tag(element, expected):
    if element.tag != expected:
        e.exit_and_print(e.ASSERT_TAG_ERROR)


def assert_attribute(element, expected):
    if not expected in element.attrib:
        e.exit_and_print(e.ASSERT_ATTR_ERROR)


def assert_value(element, attribute, value):
    if element.attrib.get(attribute) != value:
        e.exit_and_print(e.ASSERT_VALUE_ERROR)


def assert_arg_count(instruction, count):

    i = 1
    for arg in instruction:
        assert_tag(arg, "arg" + str(i))
        i += 1

    if count != i-1:
        e.exit_and_print(e.ASSERT_ARG_COUNT_ERROR)


def assert_types_offset(instruction, types, fromoffset=1, toffset=None):
    if toffset is None:
        toffset = len(instruction)

    for arg in instruction[fromoffset:toffset]:
        assert_types(arg, types)


def assert_types(arg, types):
    assert_attribute(arg, "type")
    if isinstance(types, str):
        types = [types]
    error = True
    for type in types:
        if arg.attrib.get("type") == type:
            error = False
    if error:
        e.exit_and_print(e.ASSERT_TYPE_ERROR)


def assert_variable(instruction):
    assert_types(instruction[0], "var")


def assert_same_type(instruction, offset, nil=False):
    types = set()
    var = False
    for arg in instruction[offset:]:
        val = arg.attrib.get("type")
        if val == "var":
            var = True
        if nil and val == "nil":
            var = True
        types.add(arg.attrib.get("type"))
    if not var and len(types) > 1:
        e.exit_and_print(e.ASSERT_SAME_TYPE_ERROR)
