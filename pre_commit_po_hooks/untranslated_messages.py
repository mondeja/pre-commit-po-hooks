"""Checks for untranslated messages in PO files.

Returns an error code if a PO file has an untranslated message.
"""

import argparse
import sys


def check_untranslated_messages(filenames, min_=None, quiet=False):
    """Warns about all unstranslated messages found in a set of PO files.

    Parameters
    ----------

    filenames : list
      Set of file names to check.

    quiet : bool, optional
      Enabled, don't print output to stderr when an untranslated message is found.

    Returns
    -------

    int: 0 if no untranslated messages found, 1 otherwise.
    """
    min_string = str(min_ if min_ is not None else 0)

    exitcode = 0
    for filename in filenames:
        with open(filename) as f:
            content_lines = f.readlines()

        if len(content_lines) > 4:  # skip first empty message
            content_lines = content_lines[4:]

        untranslated_messages, total_messages = 0, -1

        for i, line in enumerate(content_lines):
            next_i = i + 1

            if line.startswith('msgid "'):
                total_messages += 1

            if line.startswith('msgstr ""') and (
                next_i == len(content_lines) or (not content_lines[next_i].strip())
            ):
                exitcode = 1
                untranslated_messages += 1
                if not quiet and min_ is None:
                    sys.stderr.write(f"Untranslated message at {filename}:{i + 5}\n")

        if min_ is not None:
            _is_percent = False
            if min_string[-1] == "%":
                min_float = total_messages / 100 * float(min_string[:-1])
                _is_percent = True
            else:
                min_float = float(min)

            translated_messages = total_messages - untranslated_messages
            if min_float > translated_messages:
                exitcode = 1
                if not quiet:
                    if _is_percent:
                        translation_percent = max(
                            100,
                            translated_messages / max(1, total_messages) * 100,
                        )
                        sys.stderr.write(
                            "Lower percent of translation"
                            f" ({round(translation_percent, 3)}) than minimum"
                            f" required ({min_string}) at file {filename}\n"
                        )
                    else:
                        sys.stderr.write(
                            "Lower number of messages translated"
                            f" ({translated_messages}) than required"
                            f" ({min_string}) at file {filename}\n"
                        )

    return exitcode


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filenames", nargs="*", help="Filenames to check for untranslated messages"
    )
    parser.add_argument(
        "-m",
        "--min",
        type=str,
        metavar="N/N%",
        required=False,
        default=None,
        dest="min",
        help=(
            "Minimum messages translated in each PO file to be considered valid."
            " You can pass either a float number optionally ending in a character"
            " % to indicate that is a percentage of the total of translated"
            " entries in each PO file."
        ),
    )
    parser.add_argument("-q", "--quiet", action="store_true", help="Supress output")
    args = parser.parse_args()
    return check_untranslated_messages(
        args.filenames,
        min_=args.min,
        quiet=args.quiet,
    )


if __name__ == "__main__":
    exit(main())
