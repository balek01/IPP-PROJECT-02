import errors as e
import asserts as a

symbol = ["var", "int", "bool", "string", "float"]


def assert_arithmetic(instruction):
    assert_arg_count(instruction, 3)
    assert_variable(instruction)
    assert_types_offset(instruction, "int")


def assert_compare(instruction):

    allowedTypes = ["int", "bool", "string"]
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
    allowedType = "int"
    assert_arg_count(instruction, 2)
    assert_variable(instruction)
    assert_types_offset(instruction, allowedType)


def assert_s2i_gchar(instruction):
    assert_arg_count(instruction, 2)
    assert_variable(instruction)
    assert_types_offset(instruction, "string", 2, 3)
    assert_types_offset(instruction, "int", 3, 4)


def assert_move(instruction):
    assert_arg_count(instruction, 2)
    assert_variable(instruction)
    assert_types_offset(instruction, symbol, 2)


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
    assert_types_offset(instruction, allowedType)


def assert_read(instruction):
    allowedType = "type"  # this is correct
    assert_arg_count(instruction, 2)
    assert_types_offset(instruction, allowedType)


def assert_concat(instruction):
    pass


def assert_schar(instruction):
    pass


def assert_jumpif(instruction):
    pass


def assert_exit(instruction):
    pass


### utils of utils ###
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
    pass


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
    pass


def assert_same_type(instruction, offset):
    types = set()

    for arg in instruction[offset:]:
        types.add(arg.attrib.get("type"))
    if len(types) > 1:
        e.exit_and_print(e.ASSERT_SAME_TYPE_ERROR)
