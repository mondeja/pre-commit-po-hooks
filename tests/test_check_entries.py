"""Tests for 'max_lines' and 'max_messages' hooks."""

import contextlib
import io
import tempfile

import pytest

from hooks.check_entries import maximum_number_of_lines, maximum_number_of_messages


@pytest.mark.parametrize("quiet", (False, True), ids=("quiet=False", "quiet=True"))
@pytest.mark.parametrize(
    (
        "n_messages",
        "max_n_messages",
        "expected_exitcode",
    ),
    ((5, 6, 0), (5, 5, 0), (5, 4, 1), (0, -1, 1)),
)
def test_expected_number_of_messages(
    quiet,
    n_messages,
    max_n_messages,
    expected_exitcode,
):
    content = """#

msgid ""
msgstr ""

""" + "\n\n".join(
        [f'msgid "{i}"\nmsgstr ""' for i in range(1, n_messages + 1)]
    )

    with tempfile.NamedTemporaryFile(mode="w") as f:
        f.write(content)
        f.seek(0)

        if quiet or not n_messages > max_n_messages:
            expected_stderr = ""
        else:
            expected_stderr = (
                f"More messages ({n_messages}) than allowed"
                f" ({max_n_messages}) at file {f.name}\n"
            )

        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            assert (
                maximum_number_of_messages(
                    [f.name],
                    max_messages=max_n_messages,
                    quiet=quiet,
                )
                == expected_exitcode
            )
        assert stderr.getvalue() == expected_stderr


@pytest.mark.parametrize("quiet", (False, True), ids=("quiet=False", "quiet=True"))
@pytest.mark.parametrize(
    (
        "n_lines",
        "max_n_lines",
        "expected_exitcode",
    ),
    ((5, 6, 0), (5, 5, 0), (5, 4, 1), (0, -1, 1)),
)
def test_expected_number_of_lines(
    quiet,
    n_lines,
    max_n_lines,
    expected_exitcode,
):
    content = "\n".join([str(i) for i in range(n_lines)])

    with tempfile.NamedTemporaryFile(mode="w") as f:
        f.write(content)
        f.seek(0)

        if quiet or not n_lines > max_n_lines:
            expected_stderr = ""
        else:
            expected_stderr = (
                f"More lines ({n_lines}) than allowed"
                f" ({max_n_lines}) at file {f.name}\n"
            )

        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            assert (
                maximum_number_of_lines(
                    [f.name],
                    max_lines=max_n_lines,
                    quiet=quiet,
                )
                == expected_exitcode
            )
        assert stderr.getvalue() == expected_stderr
