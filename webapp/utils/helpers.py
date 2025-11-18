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
    return 3 <= len(username) <= 20

def fetch_program_id(program_name):
    from webapp.models.models_file import Program
    program = Program.query.filter_by(name=program_name).first()
    return program.id if program else None

def clean_form_data(form_data: dict) -> dict:
    """
    Cleans form data by stripping leading/trailing whitespace from string values.
    Non-string values are left unchanged.
    If the key is 'code' and the value is a string, it is uppercased and stripped.
    """
    if not isinstance(form_data, dict):
        return {}
    cleaned_data = {}
    for key, value in form_data.items():
        if isinstance(value, str):
            if key == 'code':
                cleaned_data[key] = value.upper().strip()
            else:
                cleaned_data[key] = value.strip()
        else:
            cleaned_data[key] = value
    return cleaned_data

def check_errors(cleaned_data: dict) -> list:
    """
    Checks for missing or invalid fields in the cleaned form data.
    Returns a list of field names that are missing or invalid.
    """
    
    from flask import flash
    missing_fields = []
    if not cleaned_data.get('name'):
        missing_fields.append('Name')
    if not cleaned_data.get('code'):
        missing_fields.append('Code')
    if not cleaned_data.get('program'):
        missing_fields.append('Program')
    if not cleaned_data.get('semester'):
        missing_fields.append('Semester')
    return missing_fields
        
def get_letter_grade(score: float) -> str:
    """
    Module to calculate the student's grade based on the score
    Keyword arguments:
    score -- The score as a number
    Return: The letter grade as a string
    """
    if score >= 70:
        return 'A'
    elif score >= 60:
        return 'B'
    elif score >= 50:
        return 'C'
    elif score >= 40:
        return 'D'
    else:
        return 'E'
    