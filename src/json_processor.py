import json
from datetime import datetime

def _remove_sensitive_data(data: dict) -> dict:
    """
    Remove sensitive fields from the data(private).
    Recursively remove sensitive fields from the JSON data.
    Sensitive fields are identified by keys that start with an underscore ('_').
      
    Args:
        data (dict): The JSON data.

    Returns:
        dict: The sanitized JSON data.
    """
    if isinstance(data, dict):
        return {
            key: _remove_sensitive_data(value)
            for key, value in data.items()
            if not key.startswith('_')
        }
    elif isinstance(data, list):
        return [_remove_sensitive_data(item) for item in data]
    else:
        return data

def _validate_lengths(data):
    """
    Ensure all string values in the JSON data are under 64 characters.

    Args:
        data (dict): The JSON data.

    Raises:
        ValueError: If any string value exceeds 64 characters.
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, str) and len(value) > 64:
                raise ValueError(f"Value for '{key}' exceeds 64 characters.")
            _validate_lengths(value)
    elif isinstance(data, list):
        for item in data:
            _validate_lengths(item)

def _validate_dates(data):
    """
    Validate date fields in the JSON data.

    Args:
        data (dict): The JSON data.

    Returns:
        dict: The JSON data with validated dates.

    Raises:
        ValueError: If any date is out of the allowed range.
    """
    allowed_range = (datetime(2014, 1, 1), datetime(2024, 12, 31))

    def validate_date(date_str):
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            if not (allowed_range[0] <= date <= allowed_range[1]):
                raise ValueError(f"Date '{date_str}' is out of range.")
            return date_str
        except ValueError:
            raise ValueError(f"Invalid date format: {date_str}")

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, str) and key.startswith('date_'):
                data[key] = validate_date(value)
            _validate_dates(value)
    elif isinstance(data, list):
        for item in data:
            _validate_dates(item)

def _validate_age(dob):
    """
    Ensure the participant is at least 40 years old.

    Args:
        dob (str): Date of birth in 'YYYY-MM-DD' format.

    Raises:
        ValueError: If the participant is under 40 years old.
    """
    try:
        birth_date = datetime.strptime(dob, '%Y-%m-%d')
        age = (datetime.now() - birth_date).days // 365
        if age < 40:
            raise ValueError("Participant must be at least 40 years old.")
    except ValueError:
        raise ValueError("Invalid date of birth format.")

def process(data):
    """
    Process the JSON data by removing sensitive data, validating lengths, dates,
    and ensuring the participant's age is at least 40.

    Returns:
        dict: The processed JSON data.
    """
    data = _remove_sensitive_data(data)
    _validate_lengths(data)
    
    dob = data.get('individual_metadata', {}).get('date_of_birth')
    if dob:
        _validate_age(dob)

    _validate_dates(data)

    return data
