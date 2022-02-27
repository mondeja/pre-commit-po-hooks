"""Checks for fuzzy messages in PO files.

Returns an error code if a PO file has a fuzzy message.
"""

import argparse
import sys


def check_fuzzy_messages(filenames, quiet=False):
    """Warns about all fuzzy messages found in a set of PO files.

    Parameters
    ----------

    filenames : list
      Set of file names to check.

    quiet : bool, optional
      Enabled, don't print output to stderr when an fuzzy message is found.

    Returns
    -------

    int: 0 if no fuzzy messages found, 1 otherwise.
    """
    exitcode = 0
    for filename in filenames:
        with open(filename) as f:
            content_lines = f.readlines()

        for i, line in enumerate(content_lines):
            if line.startswith("#,") and "fuzzy" in line:
                exitcode = 1
                if not quiet:
                    sys.stderr.write(f"Found fuzzy message at {filename}:{i + 1}\n")

    return exitcode


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filenames", nargs="*", help="Filenames to check for fuzzy messages"
    )
    parser.add_argument("-q", "--quiet", action="store_true", help="Supress output")
    args = parser.parse_args()
    return check_fuzzy_messages(args.filenames, quiet=args.quiet)


if __name__ == "__main__":
    exit(main())
