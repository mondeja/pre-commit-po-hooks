"""Checks for obsolete messages in PO files.

Returns an error code if a PO file has an obsolete message.
"""

import argparse
import sys


def check_obsolete_messages(filenames, quiet=False):
    """Warns about all obsolete messages found in a set of PO files.

    Parameters
    ----------

    filenames : list
      Set of file names to check.

    quiet : bool, optional
      Enabled, don't print output to stderr when an obsolete message is found.

    Returns
    -------

    int: 0 if no obsolete messages found, 1 otherwise.
    """
    exitcode = 0
    for filename in filenames:
        with open(filename) as f:
            content_lines = f.readlines()

        _inside_obsolete_message = False
        for i, line in enumerate(content_lines):
            if not _inside_obsolete_message and line.startswith("#~ "):
                _inside_obsolete_message = True

                exitcode = 1
                if not quiet:
                    sys.stderr.write(f"Found obsolete message at {filename}:{i + 1}\n")
            elif _inside_obsolete_message and not line.startswith("#~ "):
                _inside_obsolete_message = False

    return exitcode


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filenames", nargs="*", help="Filenames to check for obsolete messages"
    )
    parser.add_argument("-q", "--quiet", action="store_true", help="Supress output")
    args = parser.parse_args()
    return check_obsolete_messages(args.filenames, quiet=args.quiet)


if __name__ == "__main__":
    exit(main())
