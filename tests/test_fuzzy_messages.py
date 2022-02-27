"""Obsolete messages hook tests."""

import contextlib
import io
import os
import uuid

import pytest

from pre_commit_po_hooks.fuzzy_messages import check_fuzzy_messages


"""
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
        """


@pytest.mark.parametrize("quiet", (False, True), ids=("quiet=False", "quiet=True"))
@pytest.mark.parametrize(
    ("contents", "n_printed_errors", "expected_exitcode", "expected_line_numbers"),
    (
        pytest.param(
            [
                (
                    '#\nmsgid ""\nmsgstr ""\n\n'
                    '#, fuzzy\n#~ msgid "Obsolete"\n#~ msgstr "Obsoleto"\n'
                )
            ],
            1,
            1,
            [5],
            id="one-fuzzy-message",
        ),
        pytest.param(
            [
                (
                    '#\nmsgid ""\nmsgstr ""\n\n'
                    '#, fuzzy\n#~ msgid "Obsolete"\n#~ msgstr "Obsoleto"\n'
                ),
                (
                    '#\nmsgid ""\nmsgstr ""\n\n'
                    '#, fuzzy\nmsgid "Foo"\nmsgstr "Foo es"\n\n'
                    'msgid "Bar"\nmsgstr "Bar es"\n'
                ),
            ],
            2,
            1,
            [5, 5],
            id="two-fuzzy-messages-in-two-files",
        ),
        pytest.param(
            ['#\nmsgid ""\nmsgstr ""\n\nmsgid "Current"\nmsgstr "Actual"\n'],
            0,
            0,
            None,
            id="no-fuzzy-messages",
        ),
    ),
)
def test_check_fuzzy_messages(
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
        assert check_fuzzy_messages(filenames, quiet=quiet) == expected_exitcode

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
