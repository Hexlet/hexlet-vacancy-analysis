def is_valid_password(password: str) -> bool:
    if len(password) < 8:
        return False
    elif not any(char.isdigit() for char in password):
        return False
    elif not any(char.isalpha() for char in password):
        return False
    return True
