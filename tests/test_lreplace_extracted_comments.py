"""Tests for 'lreplace-extracted-comments' hook."""

import contextlib
import io
import os
import uuid

import pytest

from pre_commit_po_hooks.lreplace_extracted_comments import lreplace_extracted_comments


@pytest.mark.parametrize("quiet", (False, True), ids=("quiet=False", "quiet=True"))
@pytest.mark.parametrize(
    "dry_run", (False, True), ids=("dry_run=False", "dry_run=True")
)
@pytest.mark.parametrize(
    (
        "contents",
        "match",
        "replacement",
        "expected_exitcode",
        "expected_line_numbers",
        "expected_in_file_content",
    ),
    (
        (
            [
                (
                    '#\nmsgid ""\nmsgstr ""\n\n#. Translators: Hello\n'
                    '#~ msgid "Obsolete"\n#~ msgstr "Obsoleto"\n'
                )
            ],
            "Translators: ",
            "",
            1,
            [5],
            ["#. Hello"],
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
            "Translators: ",
            "",
            0,
            None,
            ['#~ msgid "Obsolete', 'msgid "Hello"', '#~ msgstr "Hola"'],
        ),
    ),
)
def test_lreplace_extracted_comments(
    quiet,
    dry_run,
    contents,
    match,
    replacement,
    expected_exitcode,
    expected_line_numbers,
    expected_in_file_content,
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
        assert (
            lreplace_extracted_comments(
                filenames,
                match,
                replacement,
                dry_run=dry_run,
                quiet=quiet,
            )
            == expected_exitcode
        )

    if dry_run:
        stderr_lines = stderr.getvalue().splitlines()

        if expected_line_numbers is None:
            expected_line_numbers_length = 0
        else:
            expected_line_numbers_length = len(expected_line_numbers)

        if not quiet:
            assert len(stderr_lines) == expected_line_numbers_length

    for i, filename in enumerate(filenames):

        if not dry_run:
            with open(filename) as f:
                content_lines = f.readlines()

            _in_line = False
            for line in content_lines:
                if expected_in_file_content[i] in line:
                    _in_line = True
                    break
            assert _in_line

        os.remove(filename)
