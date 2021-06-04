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
      args: ['-m', 'Translators: ', '-r', '']
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
 
 
[pypi-link]: https://pypi.org/project/pre-commit-po-hooks
[pypi-version-badge-link]: https://img.shields.io/pypi/v/pre-commit-po-hooks
[pypi-pyversions-badge-link]: https://img.shields.io/pypi/pyversions/pre-commit-po-hooks
[license-image]: https://img.shields.io/pypi/l/pre-commit-po-hooks?color=light-green
[license-link]: https://github.com/mondeja/pre-commit-po-hooks/blob/master/LICENSE
[tests-image]: https://img.shields.io/github/workflow/status/mondeja/pre-commit-po-hooks/CI?logo=github&label=tests
[tests-link]: https://github.com/mondeja/pre-commit-po-hooks/actions?query=workflow%CI

[django-rosetta-lstrip]: https://github.com/mbi/django-rosetta/pull/245
