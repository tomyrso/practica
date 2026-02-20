---
title: "feat: Add email validator"
type: feat
status: active
date: 2026-02-20
---

# feat: Add email validator

## Overview

Add `validate_email(value)` to `validators.py` following the project's `(bool, str)` convention. No external dependencies — stdlib `re` only.

## Acceptance Criteria

- [ ] `validate_email(value)` returns `(True, reason)` for valid emails
- [ ] Returns `(False, reason)` for: empty string, missing `@`, no domain dot, spaces
- [ ] Tests in `tests.py` using `unittest`, runnable via `python tests.py` or `pytest`

## Implementation

### validators.py

```python
import re

def validate_email(value: str) -> tuple[bool, str]:
    if not value:
        return False, "Email cannot be empty"
    if " " in value:
        return False, "Email cannot contain spaces"
    if "@" not in value:
        return False, "Email must contain @"
    local, _, domain = value.partition("@")
    if not local:
        return False, "Email must have a local part before @"
    if "." not in domain:
        return False, "Email domain must contain a dot"
    return True, "Valid email"
```

### tests.py

```python
import unittest
from validators import validate_email

class TestValidateEmail(unittest.TestCase):
    def test_valid_email(self):
        valid, msg = validate_email("user@example.com")
        self.assertTrue(valid)

    def test_empty(self):
        valid, _ = validate_email("")
        self.assertFalse(valid)

    def test_no_at(self):
        valid, _ = validate_email("userexample.com")
        self.assertFalse(valid)

    def test_no_domain_dot(self):
        valid, _ = validate_email("user@nodot")
        self.assertFalse(valid)

    def test_spaces(self):
        valid, _ = validate_email("user @example.com")
        self.assertFalse(valid)

    def test_no_local_part(self):
        valid, _ = validate_email("@example.com")
        self.assertFalse(valid)

if __name__ == "__main__":
    unittest.main()
```

## References

- CLAUDE.md: validator signature `(bool, str)`, stdlib only, tests in `tests.py`
