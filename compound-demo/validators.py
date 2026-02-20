# validators.py
# Simple validation utilities


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


def validate_phone(value: str) -> tuple[bool, str]:
    if not value:
        return False, "Phone cannot be empty"
    digits = "".join(c for c in value if c.isdigit())
    if len(digits) < 10:
        return False, "Phone must have at least 10 digits"
    if len(digits) > 15:
        return False, "Phone must have at most 15 digits"
    return True, "Valid phone number"
