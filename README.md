# pre-commit-po-hooks

[![PyPI][pypi-version-badge-link]][pypi-link]
[![Python versions][pypi-pyversions-badge-link]][pypi-link]
[![License][license-image]][license-link]
[![Tests][tests-image]][tests-link]

Hooks for pre-commit useful working with PO files.

## Example configuration

```yaml
- repo: https://github.com/mondeja/pre-commit-po-hooks
  rev: v1.3.3
  hooks:
    - id: obsolete-messages
    - id: untranslated-messages
    - id: remove-django-translators
    - id: standard-metadata
```

## Hooks

### **`obsolete-messages`**

Checks for obsolete messages printing their line numbers if found.

### **`untranslated-messages`**

Checks for untranslated messages printing their line numbers if found.

### **`lreplace-extracted-comments`**

Replaces a matching string at the beginning of extracted comments.

#### Parameters

- `-m/--match "STRING"`: Matching string to be replaced.
- `-r/--replacement "STRING"`: Replacement for the match at the beginning of
 the extracted comment. If you want to remove the matching beginning you can
 pass an empty string `""`.
- `-d/--dry-run`: Don't do the replacements, only writes to stderr the locations
 of the extracted comments to be replaced.
 
### **`remove-django-translators`**

Same as [`lreplace-extracted-comments`][lreplace-extracted-comments-link]
passing `--match "Translators: " --replacement ""`. Useful to remove the string
prepended by Django extracting messages with xgettext (see more about this
problem in [django-rosetta#245][django-rosetta-lstrip]).

### **`check-metadata`**

Check that metadata fields matches a set of regular expressions.

#### Parameters

- `-h/--header HEADER`: Header name to match in metadata. This argument can be
 passed multiple times, but after each `-h/--header` argument must be a
 `-v/--value` that indicates the regular expression for that header.
- `-v/--value REGEX`: Can be passed multiple times. Indicates the regular
 expression that the last header passed in the argument `-h/--header` must
 match in the checked PO files.
- `-n/--no-metadata`: When this option is passed, the hook instead checks that
 there is no metadata in the files, so it will exit with code 1 if some
 metadata is found in a file or 0 if there is no metadata in any files.
- `-r/--remove/--remove-metadata`: When this option is passed the metadata will
 be removed from the files instead of being trated as a lint error.

### **`standard-metadata`**

Check that the metadata of your PO files fits some standard requirements based
on the next regular expressions:

- `Project-Id-Version`: `\d+\.\d+\.\d`
- `Report-Msgid-Bugs-To`: `.+\s<.+@.+\..+>`
- `Last-Translator`: `.+\s<.+@.+\..+>`
- `Language-Team`: `.+\s<.+@.+\..+>`
- `Language`: `\w\w_?\w?\w?(@\w+)?`
- `Content-Type`: `text/plain; charset=[a-zA-Z\-]+`
- `Content-Transfer-Encoding`: `\d+bits?`

If you need to replace some fields with other regular expressions, you can do
it passing the `-h` and `-v` arguments of the
[`check-metadata` hook][check-metadata-link].

For example, if your version
includes the character `v` at the beginning:
`-h "Project-Id-Version" -v "v\d+\.\d+\.\d"`

### **`no-metadata`**

It will check if PO files has metadata. If has metadata, it will fail the check
return 1 exit code.

#### Parameters

- `-r/--remove/--remove-metadata`: When this option is passed the metadata will
 be removed from the files instead of being trated as a lint error.

 
[pypi-link]: https://pypi.org/project/pre-commit-po-hooks
[pypi-version-badge-link]: https://img.shields.io/pypi/v/pre-commit-po-hooks
[pypi-pyversions-badge-link]: https://img.shields.io/pypi/pyversions/pre-commit-po-hooks
[license-image]: https://img.shields.io/pypi/l/pre-commit-po-hooks?color=light-green
[license-link]: https://github.com/mondeja/pre-commit-po-hooks/blob/master/LICENSE
[tests-image]: https://img.shields.io/github/workflow/status/mondeja/pre-commit-po-hooks/CI?logo=github&label=tests
[tests-link]: https://github.com/mondeja/pre-commit-po-hooks/actions?query=workflow%CI

[lreplace-extracted-comments-link]: https://github.com/mondeja/pre-commit-po-hooks#lreplace-extracted-comments
[check-metadata-link]: https://github.com/mondeja/pre-commit-po-hooks#check-metadata
[django-rosetta-lstrip]: https://github.com/mbi/django-rosetta/pull/245
