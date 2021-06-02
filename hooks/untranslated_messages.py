"""Checks for untranslated messages in PO files.

Returns an error code if a pofile has an untranslated message.
"""

import argparse
import sys


def check_untranslated_messages(filenames, quiet=False):
    """Warns about all unstranslated messages found in a set of PO files.

    Parameters
    ----------

    filenames : list
      Set o file names to check.

    quiet : bool, optional
      Enabled, don't print output to stderr when an untranslated message is found.

    Returns
    -------

    int: 0 if no untranslated messages found, 1 otherwise.
    """
    exitcode = 0
    for filename in filenames:
        with open(filename) as f:
            content_lines = f.readlines()

        if len(content_lines) > 4:  # skip first empty message
            content_lines = content_lines[4:]

        for i, line in enumerate(content_lines):
            next_i = i + 1

            if line.startswith('msgstr ""') and (
                next_i == len(content_lines) or (not content_lines[next_i].strip())
            ):
                exitcode = 1
                if not quiet:
                    sys.stderr.write(
                        f"Found untranslated message at {filename}:{i + 5}\n"
                    )

    return exitcode


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filenames", nargs="*", help="Filenames to check for untranslated messages"
    )
    parser.add_argument("-q", "--quiet", action="store_true", help="Supress output")
    args = parser.parse_args()
    return check_untranslated_messages(args.filenames, quiet=args.quiet)


if __name__ == "__main__":
    exit(main())
