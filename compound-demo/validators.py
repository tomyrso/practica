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
