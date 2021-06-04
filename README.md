# pre-commit-po-hooks

[![PyPI][pypi-version-badge-link]][pypi-link]
[![Python versions][pypi-pyversions-badge-link]][pypi-link]
[![License][license-image]][license-link]
[![Tests][tests-image]][tests-link]

Hooks for pre-commit useful working with PO files.

## Example configuration

```yaml
- repo: https://github.com/mondeja/pre-commit-po-hooks
  rev: v1.0.0
  hooks:
    - id: obsolete-messages
    - id: untranslated-messages
    - id: lreplace-extracted-comments
      args:
        - -m
        - 'Translators: '
        - -r
        - ''
    - id: check-metadata
      args:
        - -h
        - Project-Id-Version
        - -v
        - v\d+\.\d+\.\d+
```

## Hooks

### **`obsolete-messages`**

Checks for obsolete messages printing their line numbers if found.

### **`untranslated-messages`**

Checks for untranslated messages printing their line numbers if found.

### **`lreplace-extracted-comments`**

Replaces a matching string at the beginning of the extracted comments.
This can be used to remove the string "Translators: " introduced by Django (see
more about this problem in [django-rosetta#245][django-rosetta-lstrip]).

#### Parameters

- `-m/--match "STRING"`: Matching string to be replaced.
- `-r/--replacement "STRING"`: Replacement for the match at the beginning of
 the extracted comment. If you want to remove the matching beginning you can
 pass an empty string `""`.
- `-d/--dry-run`: Don't do the replacements, only writes to stderr the locations
 of the extracted comments to be replaced.
 
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
 
[pypi-link]: https://pypi.org/project/pre-commit-po-hooks
[pypi-version-badge-link]: https://img.shields.io/pypi/v/pre-commit-po-hooks
[pypi-pyversions-badge-link]: https://img.shields.io/pypi/pyversions/pre-commit-po-hooks
[license-image]: https://img.shields.io/pypi/l/pre-commit-po-hooks?color=light-green
[license-link]: https://github.com/mondeja/pre-commit-po-hooks/blob/master/LICENSE
[tests-image]: https://img.shields.io/github/workflow/status/mondeja/pre-commit-po-hooks/CI?logo=github&label=tests
[tests-link]: https://github.com/mondeja/pre-commit-po-hooks/actions?query=workflow%CI

[django-rosetta-lstrip]: https://github.com/mbi/django-rosetta/pull/245
