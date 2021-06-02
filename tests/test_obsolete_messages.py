"""Obsolete messages hook tests."""

import contextlib
import io
import os
import uuid

import pytest

from hooks.obsolete_messages import check_obsolete_messages


@pytest.mark.parametrize("quiet", (False, True))
@pytest.mark.parametrize(
    ("contents", "n_printed_errors", "expected_exitcode", "expected_line_numbers"),
    (
        (
            ['#\nmsgid ""\nmsgstr ""\n\n#~ msgid "Obsolete"\n#~ msgstr "Obsoleto"\n'],
            1,
            1,
            [5],
        ),
        (
            [
                (
                    '#\nmsgid ""\nmsgstr ""\n\n#~ msgid "Obsolete "\n#~ "message"'
                    '\n#~ msgstr "Mensaje obsoleto"\n'
                ),
                '#\nmsgid ""\nmsgstr ""\n\nmsgid "Hello"\nmsgstr "Hola"\n',
                (
                    '#\nmsgid ""\nmsgstr ""\n\n#~ msgid "Hello"\n#~ msgstr "Hola"\n'
                    '\nmsgid "Foo"\nmsgstr "Bar"\n'
                ),
            ],
            2,
            1,
            [5, 5],
        ),
        (
            ['#\nmsgid ""\nmsgstr ""\n\nmsgid "Current"\nmsgstr "Actual"\n'],
            0,
            0,
            None,
        ),
    ),
)
def test_check_obsolete_messages(
    quiet,
    contents,
    n_printed_errors,
    expected_exitcode,
    expected_line_numbers,
    tmp_path,
):
    filenames = []
    for content in contents:
        filename = tmp_path / f"{uuid.uuid4().hex[:16]}.po"

        with open(filename, "w") as f:
            f.write(content)

        filenames.append(filename)

    stderr = io.StringIO()
    with contextlib.redirect_stderr(stderr):
        assert check_obsolete_messages(filenames, quiet=quiet) == expected_exitcode

    stderr_lines = stderr.getvalue().splitlines()
    if quiet:
        n_printed_errors = 0
    assert len(stderr_lines) == n_printed_errors

    if n_printed_errors:
        assert len(stderr_lines) == len(expected_line_numbers)

        for i, line in enumerate(stderr_lines):
            line_number = int(line.split(":")[-1])
            assert line_number == expected_line_numbers[i]

    for filename in filenames:
        os.remove(filename)
