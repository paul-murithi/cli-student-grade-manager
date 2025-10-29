import re

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validate_password(password):
    if not password or password.strip() == "":
        return False
    return len(password) >= 8 and any(char.isdigit() for char in password)


def validate_username(username):
    if not username or username.strip() == "":
        return False
    return username.isalnum() and 3 <= len(username) <= 20
