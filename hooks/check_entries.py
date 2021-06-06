"""Script that checks entries of PO files."""

import argparse
import os
import sys


def maximum_number_of_messages(filenames, max_messages=10000, quiet=False):
    """Check that the maximum number of messages in each PO file is not
    greater than the number passed in the parameter ``max_messages``.

    Parameters
    ----------

    filenames : list
      Set of file names to check.

    max_messages : int, optional
      Maximum number of messages in each PO file.

    quiet : bool, optional
      Enabled, don't print output to stderr when more messages than allowed
      are found.

    Returns
    -------

    int: 0 if no more than ``max_messages`` messages found for each file,
      1 otherwise.
    """
    exitcode = 0

    for filename in filenames:
        with open(filename) as f:
            content_lines = f.readlines()

        number_of_messages = 0
        for i, line in enumerate(content_lines):
            if line.startswith('msgid "'):
                number_of_messages += 1

        if (number_of_messages - 1) > max_messages:
            exitcode = 1
            if not quiet:
                sys.stderr.write(
                    f"More messages ({number_of_messages}) than allowed"
                    f" ({max_messages}) at file {os.path.abspath(filename)}\n"
                )

    return exitcode


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filenames", nargs="*", help="Filenames to check for obsolete messages"
    )
    parser.add_argument("-q", "--quiet", action="store_true", help="Supress output")
    parser.add_argument(
        "-m",
        "--max-messages",
        type=int,
        metavar="NUMBER",
        required=False,
        default=None,
        help=(
            "Check the maximum number of messages in each PO file "
            "is not greater than the number passed in this parameter."
        ),
    )
    args = parser.parse_args()
    if args.max_messages is not None:
        return maximum_number_of_messages(
            args.filenames, args.max_messages, quiet=args.quiet
        )
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    exit(main())
