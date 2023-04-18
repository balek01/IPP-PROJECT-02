import xml.etree.ElementTree as et
import errors as e
import assert_utils as a


def xml_parser(sourceFile, is_file):

    try:
        if is_file:
            xml = et.parse(sourceFile)
            root = xml.getroot()
        else:
            root = et.fromstring(sourceFile)

    except et.ParseError:
        e.exit_and_print(e.XML_FORMAT_ERROR)

    try:
        root[:] = sorted(root, key=lambda child: int(child.get('order', 1)))
    except ValueError:
        e.exit_and_print(e.ASSERT_ORDER_TYPE_ERROR)

    a.assert_tag(root, "program")
    a.assert_attribute(root, "language")
    a.assert_value(root, "language", "IPPcode23")
    order = set()
    for instruction in root:
        instruction[:] = sorted(instruction, key=lambda child: child.tag)
        a.assert_tag(instruction, "instruction")
        a.assert_attribute(instruction, "order")

        ordervalue = int(instruction.attrib.get("order"))

        if ordervalue in order or ordervalue < 1:
            e.exit_and_print(e.ASSERT_ORDER_VALUE_ERROR)

        order.add(ordervalue)
        a.assert_opcode(instruction)
        for arg in instruction:
            a.assert_arg_value_matches_type(arg)
    return root
