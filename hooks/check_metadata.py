"""Script that checks metadata sanity of PO files.

For each metadata header, you can specify that the value should match with
a regex.
"""

import argparse
import re
import sys


def check_metadata(
    filenames, headers_spec, no_metadata=False, remove_metadata=False, quiet=False
):
    """Check that metadata headers and values match a set of requirements.

    Parameters
    ----------

    filenames : list
      Set of file names to check.

    headers_spec : dict
      Name of headers as keys and regular expressions as values to match
      in the metadata of each file.

    no_metadata : bool, optional
      When this option is set to ``True``, the hook instead checks that there
      is no metadata in the files, so it will return 1 if metadata is found
      and 0 exitcode otherwise.

    remove_metadata : bool, optional
      Removes the metadata of the PO file.

    quiet : bool, optional
      Enabled, don't print output to stderr when a wrong metadata is found.

    Returns
    -------

    int: 0 if no wrong metadata fields found, 1 otherwise.
    """
    headers_spec_regex = {
        header: re.compile(rf"{value}") for header, value in headers_spec.items()
    }

    exitcode = 0
    for filename in filenames:
        headers_matched = []

        with open(filename) as f:
            content_lines = f.readlines()

        _first_metadata_line = None
        for i, line in enumerate(content_lines):
            if line.startswith('msgid ""') and content_lines[i + 1].startswith(
                'msgstr ""'
            ):
                if (len(content_lines) > i + 2) and content_lines[i + 2].startswith(
                    '"'
                ):
                    _first_metadata_line = i + 2

                    if no_metadata and not remove_metadata:
                        exitcode = 1
                        if not quiet:
                            sys.stderr.write(
                                f"Found unexpected metadata at {filename}:{i + 3}\n"
                            )
                else:
                    if not no_metadata:
                        exitcode = 1
                        if not quiet:
                            sys.stderr.write(
                                f"No metadata found in the file {filename}\n"
                            )

                break

        if (no_metadata and exitcode) or _first_metadata_line is None:
            continue

        if remove_metadata:
            with open(filename, "w") as f:
                f.write("".join(content_lines[:_first_metadata_line]))

                index = 0
                for i, line in enumerate(content_lines[_first_metadata_line:]):
                    if not line.strip():
                        index = i
                        break

                f.write("".join(content_lines[_first_metadata_line + index :]))
                exitcode = 1
        else:
            for i, line in enumerate(content_lines[_first_metadata_line:]):
                if not line.strip():
                    break

                header, value = line.split(": ", maxsplit=1)
                header = header.lstrip('"')

                if header in headers_spec_regex:
                    headers_matched.append(header)
                    value = re.sub(r"(\n|\\n|\"$)+", "", value)
                    regex = headers_spec_regex[header]
                    if re.match(regex, value) is None:
                        exitcode = 1
                        if not quiet:
                            sys.stderr.write(
                                f"Wrong metadata value at {filename}"
                                f":{_first_metadata_line + i + 1} (regex"
                                f" '{regex.pattern}' not matching for value"
                                f" '{value}' in header '{header}')\n"
                            )

            for header in headers_spec.keys():
                if header not in headers_matched:
                    sys.stderr.write(
                        f"Metadata header '{header}' expected at file"
                        f" {filename}:{_first_metadata_line}, but not found\n"
                    )
                    exitcode = 1

    return exitcode


def main():
    parser = argparse.ArgumentParser()

    to_remove = ["-h", "--header", "-v", "--value"]
    argv, headers_spec, _current_header = (sys.argv, dict(), None)
    argv_length = len(argv)
    for i, arg in enumerate(argv):
        if i < (argv_length - 1):
            if arg in ["-h", "--header"]:
                _current_header = argv[i + 1]
            elif arg in ["-v", "--value"] and _current_header is not None:
                value = argv[i + 1]
                headers_spec[_current_header] = value
                to_remove.extend([value, _current_header])
                _current_header = None
    for value in to_remove:
        if value in argv:
            argv.remove(value)

    parser.add_argument(
        "filenames", nargs="*", help="Filenames to check for obsolete messages"
    )
    parser.add_argument(
        "-n",
        "--no-metadata",
        action="store_true",
        dest="no_metadata",
        help=(
            "The files shouldn't have metadata. If a file has metadata"
            " information, exits with code 1."
        ),
    )
    parser.add_argument(
        "-r",
        "--remove",
        "--remove-metadata",
        action="store_true",
        dest="remove_metadata",
        help=(
            "Remove metadata from files that have it. You must pass it along"
            " with '--no-metadata'."
        ),
    )
    parser.add_argument(
        "-s",
        "--standard-headers",
        action="store_true",
        dest="standard_headers",
        help=(
            "A common standard set of headers will be defined as specification."
            " Each value can be overwritten using '-h' and '-v' arguments."
            "\n\n- 'Project-Id-Version': \\d+\\.\\d+\\.\\d\n"
            "- 'Report-Msgid-Bugs-To': .+\\s<.+@.+\\..+>\n"
            "- 'Last-Translator': .+\\s<.+@.+\\..+>\n"
            "- 'Language-Team': .+\\s<.+@.+\\..+>\n"
            "- 'Language': \\w\\w_?\\w?\\w?(@\\w+)?\n"
            "- 'Content-Type': text/plain; charset=[A-Z\\-]+\n"
            r"- 'Content-Transfer-Encoding': \d+bits?"
        ),
    )
    parser.add_argument("-q", "--quiet", action="store_true", help="Supress output")
    args = parser.parse_args()

    if args.remove_metadata:
        args.no_metadata = True

    if args.no_metadata and len(headers_spec.keys()):
        raise ValueError(
            "You must pass either '--no-metadata' or headers regexes specification,"
            " but both can't be non false."
        )

    if args.no_metadata and args.standard_headers:
        raise ValueError(
            "You must pass either '--no-metadata' or standard headers regexes"
            " specification."
        )

    if args.standard_headers:
        new_headers_spec = {
            "Project-Id-Version": r"\d+\.\d+\.\d",
            "Report-Msgid-Bugs-To": r".+\s<.+@.+\..+>",
            "Last-Translator": r".+\s<.+@.+\..+>",
            "Language-Team": r".+\s<.+@.+\..+>",
            "Language": r"\w\w_?\w?\w?(@\w+)?",
            "Content-Type": r"text/plain; charset=[0-9a-zA-Z\-]+",
            "Content-Transfer-Encoding": r"\d+bits?",
        }
        if headers_spec:
            new_headers_spec.update(headers_spec)

        headers_spec = new_headers_spec

    return check_metadata(
        args.filenames,
        headers_spec,
        no_metadata=args.no_metadata,
        remove_metadata=args.remove_metadata,
        quiet=args.quiet,
    )


if __name__ == "__main__":
    exit(main())
