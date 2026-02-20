---
title: "feat: Add phone validator"
type: feat
status: active
date: 2026-02-20
---

# feat: Add phone validator

## Overview

Add `validate_phone(value)` to `validators.py` following the existing `(bool, str)` pattern.

> **Found in docs/solutions:** `patterns/input-validator-bool-str-pattern.md` — reusing the same pattern and template. No investigation needed.

## Acceptance Criteria

- [ ] `validate_phone(value)` returns `(True, reason)` for valid phone numbers
- [ ] Returns `(False, reason)` for: empty, fewer than 10 digits, more than 15 digits
- [ ] Tests in `tests.py` using `unittest`

## Implementation

Digit-stripping approach: strip formatting characters, count only actual digits (10–15, E.164 standard). No `re` needed.

### validators.py

```python
def validate_phone(value: str) -> tuple[bool, str]:
    if not value:
        return False, "Phone cannot be empty"
    digits = "".join(c for c in value if c.isdigit())
    if len(digits) < 10:
        return False, "Phone must have at least 10 digits"
    if len(digits) > 15:
        return False, "Phone must have at most 15 digits"
    return True, "Valid phone number"
```

### tests.py

```python
class TestValidatePhone(unittest.TestCase):
    def test_valid_phone(self):
        valid, msg = validate_phone("+1 800 555 1234")
        self.assertTrue(valid)

    def test_empty(self):
        valid, _ = validate_phone("")
        self.assertFalse(valid)

    def test_too_short(self):
        valid, _ = validate_phone("123")
        self.assertFalse(valid)

    def test_too_long(self):
        valid, _ = validate_phone("1234567890123456")
        self.assertFalse(valid)

    def test_formatted(self):
        valid, _ = validate_phone("+1 (800) 555-1234")
        self.assertTrue(valid)
```

## References

- Pattern: `docs/solutions/patterns/input-validator-bool-str-pattern.md` ← encontrado por learnings-researcher
- Existing validator: `validators.py` — `validate_email`
