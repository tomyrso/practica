---
title: "Input Validator — (bool, str) Return Pattern"
category: "patterns"
tags: ["validation", "stdlib-only", "tuple-return", "unittest", "python"]
problem_type: "Input Validation"
component: "validators"
symptoms:
  - "Need to validate string input and report why it failed"
  - "Need a consistent validator interface across multiple validators"
  - "Need to test validation logic with unittest"
date: 2026-02-20
---

# Input Validator — (bool, str) Return Pattern

## Pattern

Every validator in this project is a plain function that returns `(bool, str)`:
- `True, "reason"` — input is valid
- `False, "reason"` — input is invalid, reason explains why

```python
def validate_something(value: str) -> tuple[bool, str]:
    ...
    return True, "Valid something"
```

## Solution: validate_email

Reference implementation in `validators.py`:

```python
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

**Key approach:** fail-fast sequential checks — most basic constraints first (empty, spaces), then structural (@), then component validation (local part, domain dot).

## Test Structure

One `unittest.TestCase` per validator. One test per rule:

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

if __name__ == "__main__":
    unittest.main()
```

Run with: `python3 tests.py -v`

## Template for New Validators

```python
def validate_X(value: str) -> tuple[bool, str]:
    if not value:
        return False, "X cannot be empty"
    # high-level format checks
    if some_condition:
        return False, "Specific descriptive reason"
    # component checks
    part1, _, part2 = value.partition(separator)
    if not part1:
        return False, "X must have a [part1]"
    if some_part2_check:
        return False, "X [part2] must ..."
    return True, "Valid X"
```

## Common Mistakes

| Mistake | Fix |
|---|---|
| Returning success before all checks pass | Always put the `return True` at the very end |
| Generic error message (`"Invalid"`) | Be specific: `"Email must contain @"` |
| Testing the message string instead of the bool | `self.assertFalse(valid)`, not `self.assertEqual(msg, "...")` |
| Checking the bool with `if validate_email(x)[0]` | Unpack: `valid, _ = validate_email(x)` |

## Edge Cases to Always Test

- Empty string `""`
- Input with spaces
- Missing required character/symbol
- Missing each component individually
- Valid happy-path case

## Reuse Example: validate_phone

Following the same pattern:

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
