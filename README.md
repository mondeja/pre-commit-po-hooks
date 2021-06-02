# pre-commit-po-hooks

Hooks for pre-commit useful working with PO files.

## Example configuration

```yaml
- repo: https://github.com/mondeja/pre-commit-po-hooks
  rev: v1.0.0
  hooks:
    - id: obsolete-messages
    - id: untranslated-messages
```

## Hooks

- **`obsolete-messages`**: checks for obsolete messages printing their line
 numbers if found.
- **`untranslated-messages`**: checks for untranslated messages printing their
 line numbers if found.
