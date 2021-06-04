"""Tests for 'check_metadata' hook."""

import contextlib
import io
import os
import uuid

import pytest

from hooks.check_metadata import check_metadata


@pytest.mark.parametrize("quiet", (False, True), ids=("quiet=False", "quiet=True"))
@pytest.mark.parametrize(
    (
        "contents",
        "headers_spec",
        "n_printed_errors",
        "expected_exitcode",
        "expected_line_numbers",
    ),
    (
        (
            [
                (
                    '#\nmsgid ""\nmsgstr ""\n"Project-Id-Version: v0.240.1\\n"\n'
                    '"Report-Msgid-Bugs-To: Álvaro Mondéjar'
                    ' <mondejar1994@gmail.com>\\n"\n'
                ),
            ],
            {
                "Project-Id-Version": r"v\d+\.\d+\.\d+",
                "Report-Msgid-Bugs-To": "foobar",
            },
            1,
            1,
            [5],
        ),
    ),
)
def test_check_obsolete_messages(
    quiet,
    contents,
    headers_spec,
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
        assert check_metadata(filenames, headers_spec, quiet=quiet) == expected_exitcode

    stderr_lines = stderr.getvalue().splitlines()
    if quiet:
        n_printed_errors = 0
    assert len(stderr_lines) == n_printed_errors

    if n_printed_errors:
        assert len(stderr_lines) == len(expected_line_numbers)

        for i, line in enumerate(stderr_lines):
            line_number = int(line.split(":")[1].split(" ")[0])
            assert line_number == expected_line_numbers[i]

    for filename in filenames:
        os.remove(filename)
