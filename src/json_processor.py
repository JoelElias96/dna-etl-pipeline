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
        # Recursively process dictionary items, removing keys that start with '_'
        return {
            key: _remove_sensitive_data(value)
            for key, value in data.items()
            if not key.startswith('_')
        }
    elif isinstance(data, list):
        # Recursively process list items
        return [_remove_sensitive_data(item) for item in data]
    else:
        # Return the data as is if it's neither a dict nor a list
        return data

def _validate_lengths_of_strs(data : dict)-> None:   
    """
    Ensure all string values in the JSON data are under 64 characters.
    This function recursively checks all string values in the provided JSON data 
    (dictionary or list) to ensure they do not exceed 64 characters in length.

    Args:
        data (dict): The JSON data.

    Raises:
        ValueError: If any string value exceeds 64 characters.
    """

    def _validate_length_of_str(word : str) -> None:
        if len(word) > 64:
            raise ValueError(f"The string '{word}' exceeds 64 characters.")
        
    if isinstance(data, dict):
        # Iterate through dictionary items
        
        for key, value in data.items():
            # Check if the value is a string and its length exceeds 64 characters
            if isinstance(value, str):
                _validate_length_of_str(value)
            
            # Recursively validate lengths for nested dictionaries or lists
            _validate_lengths_of_strs(value)

    elif isinstance(data, list):
        # Iterate through list items and recursively validate lengths for list items
        for item in data:

            # Check if the value is a string and its length exceeds 64 characters
            if isinstance(item, str):
                _validate_length_of_str(item)
            
            _validate_lengths_of_strs(item)
    
    else:
        # No action needed for non-dict and non-list items
        pass

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
    _validate_lengths_of_strs(data)
    
    dob = data.get('individual_metadata', {}).get('date_of_birth')
    if dob:
        _validate_age(dob)

    _validate_dates(data)

    return data
