import argparse
import errors as e
import os


def parse_args():
    ap = argparse.ArgumentParser(
        prog='interpret.py',
        description="IPPCODE23 INTERPRET",
        epilog='Atleast one of input files must be sepecified.',
        exit_on_error=False)

    ap.add_argument("--source", required=False, help="source XML file ")
    ap.add_argument("--input", required=False,  help="file containing inputs")

    try:
        args = ap.parse_args()
    except Exception:
        e.exit_and_print(e.ARG_ERROR)

    if not args.input and not args.source:
        e.exit_and_print(e.ARG_ERROR)

    if args.input:
        if not os.path.isfile(args.input) or not os.access(args.input, os.R_OK):
            e.exit_and_print(e.FILE_ERROR)

    if args.source:
        if not os.path.isfile(args.source) or not os.access(args.source, os.R_OK):
            e.exit_and_print(e.FILE_ERROR)

    return args.input, args.source
