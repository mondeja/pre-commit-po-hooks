"""Replaces the beginning of extracted comments which starts with a string
by another value.

Returns an error code if the extracted comments were replaced.
"""

import argparse
import os
import re
import shutil
import sys
import tempfile


TMP_DIR = tempfile.gettempdir()


def lreplace_extracted_comments(
    filenames, match, replacement, dry_run=False, quiet=False
):
    """Replace the beginning of the extracted comments which starts with the
    string passed in the argument ``match``.


    Parameters
    ----------

    filenames : list
      Set o file names to replace.

    match : str
      The start of the extracted comment content to be replaced.

    replacement : str
      The replacement for the beginning of the matching extracted comments.

    dry_run : bool, optional
      Don't do the replacements, just writes to stderr the location of them.
      You can use it with ``quiet=True`` to check if the strings has been
      removed (returns 1 if there is some replacement to do).

    quiet : bool, optional
      Enabled, don't print output to stderr when an obsolete message is found.


    Returns
    -------

    int: 0 if no a extracted comment has been replaced, 1 otherwise.
    """
    regex = re.compile(rf"^#\.\s{re.escape(match)}")

    exitcode = 0
    for filename in filenames:
        with open(filename) as f:
            content_lines = f.readlines()

        tmp_filename = os.path.join(
            TMP_DIR,
            f"pre-commit-po-hooks--{os.path.basename(filename)}",
        )

        with open(tmp_filename, "w") as f:
            for i, line in enumerate(content_lines):
                if line.startswith("#. ") and re.match(regex, line):
                    if dry_run and not quiet:
                        sys.stderr.write(
                            "Translator comment would be replaced"
                            f" at '{filename}:{i+1}'\n"
                        )
                    new_line = f"#. {re.sub(regex, replacement, line)}"
                    if new_line != line:
                        exitcode = 1
                    line = new_line
                f.write(line)

        if not dry_run:
            os.remove(filename)
            shutil.move(tmp_filename, filename)

    return exitcode


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filenames",
        nargs="*",
        help="Filenames to check for obsolete messages",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Supress output",
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        dest="dry_run",
        help="Don't do the replacements, just writes to stderr the location of them.",
    )
    parser.add_argument(
        "-m",
        "--match",
        dest="match",
        required=True,
        metavar="MATCH",
        help="The string to match at the beginning of the extracted comments to"
        " replace it.",
    )
    parser.add_argument(
        "-r",
        "--replacement",
        dest="replacement",
        required=True,
        metavar="REPL",
        help="The substitution to be used to replace the matching string.",
    )
    args = parser.parse_args()

    return lreplace_extracted_comments(
        args.filenames,
        args.match,
        args.replacement,
        dry_run=args.dry_run,
        quiet=args.quiet,
    )


if __name__ == "__main__":
    exit(main())
