# tests.py
# Tests for validators

import unittest
from validators import validate_email


class TestValidateEmail(unittest.TestCase):
    def test_valid_email(self):
        valid, msg = validate_email("user@example.com")
        self.assertTrue(valid)
        self.assertEqual(msg, "Valid email")

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
