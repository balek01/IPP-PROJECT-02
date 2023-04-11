from parseargs import parse_args
import xmlparser as xp

inputfile, sourcefile = parse_args()
xp.xml_parser(sourcefile)

