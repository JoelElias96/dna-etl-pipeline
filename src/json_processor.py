import json
from datetime import datetime

def _remove_sensitive_data(data: dict) -> dict:
    """
    Remove sensitive fields from the data (iterative).
    Iteratively remove sensitive fields from the JSON data.
    Sensitive fields are identified by keys that start with an underscore ('_').

    Args:
        data (dict): The JSON data.

    Returns:
        dict: The sanitized JSON data.
    """
    # Initialize the stack with the input data
    stack = [data]
    
    # Perform iterative depth-first search (DFS) to traverse the data structure
    while stack:
        current = stack.pop()
        
        if isinstance(current, dict):
            # Identify keys that start with an underscore
            keys_to_remove = [key for key in current if key.startswith('_')]
            
            # Remove the identified keys from the dictionary
            for key in keys_to_remove:
                del current[key]
            
            # Add the remaining values to the stack for further traversal
            stack.extend(current.values())
        
        elif isinstance(current, list):
            # Add list items to the stack for further traversal
            stack.extend(current)
    
    # Return the sanitized data
    return data

def _validate_lengths_of_strs(data: dict) -> None:
    """
    Ensure all string values in the JSON data are under 64 characters.
    This function iteratively checks all string values in the provided JSON data 
    (dictionary or list) to ensure they do not exceed 64 characters in length.

    Args:
        data (dict): The JSON data.

    Raises:
        ValueError: If any string value exceeds 64 characters.
    """
    def _validate_length_of_str(word: str) -> None:
        """
        Validate the length of a string.

        Args:
            word (str): The string to validate.

        Raises:
            ValueError: If the string exceeds 64 characters.
        """
        if len(word) > 64:
            raise ValueError(f"The string '{word}' exceeds 64 characters.")

    # Initialize the stack with the input data
    stack = [data]

    # Perform iterative depth-first search (DFS) to traverse the data structure
    while stack:
        current = stack.pop()

        if isinstance(current, dict):
            # If the current element is a dictionary, check its values
            for value in current.values():
                if isinstance(value, str):
                    # Validate the length of string values
                    _validate_length_of_str(value)
                else:
                    # Add non-string values to the stack for further traversal
                    stack.append(value)

        elif isinstance(current, list):
            # If the current element is a list, check its items
            for item in current:
                if isinstance(item, str):
                    # Validate the length of string items
                    _validate_length_of_str(item)
                else:
                    # Add non-string items to the stack for further traversal
                    stack.append(item)

def _validate_dates_in_file(data: dict)-> None:
        """
        Validate date fields in the JSON data.
        This function recursively checks all date fields in the provided JSON data
        (dictionary or list) to ensure they are in the 'YYYY-MM-DD' format and fall
        within the allowed range of 2014-01-01 to 2024-12-31.
        in case its the birth date of the individual, it will skip the validation.

        Args:
            data (dict): The JSON data.

        Raises:
            ValueError: If any date is out of the allowed range or in an invalid format.
        """
        allowed_range = (datetime(2014, 1, 1), datetime(2024, 12, 31))

        def _validate_datetime_format(date_str : str) -> bool:
            """
            Validates if the given date string matches the format '%Y-%m-%d'.
            Args:
                date_str (str): The date string to validate.
            Returns:
                bool: True if the date string matches the format '%Y-%m-%d', False otherwise.
            """
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                return False
            return True
        
        def _date_in_allowed_range(date_str: str) -> None:
            """
            Check if a date falls within the allowed range.

            Args:
                date_str (str): The date string to check.

            Raises:
                ValueError: If the date is out of the allowed range.
            """
            date= datetime.strptime(date_str, '%Y-%m-%d')
            if not allowed_range[0] <= date <= allowed_range[1]:
                raise ValueError(f"Date '{date_str}' is out of the allowed range.")

        
        def _traverse_data_iterative(data: object) -> None:
            """
            Iteratively traverses through a nested data structure using dfs,
            and validates date strings within the allowed range.
            in case its the birth date of the individual, it will skip the validation.

            Args:
                data (object): The data structure to traverse. It can be a dictionary, list, or string.
            Returns:
                None
            Notes:
                - If the data is a dictionary, the function will iteratively traverse its values, skipping any key named "date_of_birth".
                - If the data is a list, the function will iteratively traverse each item in the list.
                 - If the data is a string and represents a date, it will validate the date format and check if the date is within an allowed range.
            """
            stack = [data]

            while stack:
                current = stack.pop()

                if isinstance(current, dict):
                    for key, value in current.items():
                        if key != "date_of_birth":
                            stack.append(value)

                elif isinstance(current, list):
                    stack.extend(current)

                elif isinstance(current, str) and _validate_datetime_format(current):
                    _date_in_allowed_range(current)

        # Start the iterative traversal and validation
        _traverse_data_iterative(data)

def _validate_age(i_birth_date : str) -> None:
    """
    Ensure the participant is at least 40 years old.

    Args:
        dob (str): Date of birth in 'YYYY-MM-DD' format.

    Raises:
        ValueError: If the participant is under 40 years old.
        ValueError: If the date of birth is in an invalid format.
    """
    try:
        birth_date = datetime.strptime(i_birth_date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Invalid date of birth format.")
    
    age = (datetime.now() - birth_date).days // 365
    if age < 40:
        raise ValueError("Participant must be at least 40 years old.")

def _process_json_file(data : dict) -> dict:
    """
    Process the JSON data by removing sensitive data, validating lengths, dates,
    and ensuring the participant's age is at least 40(private).

    Returns:
        dict: The processed JSON data.

    raises:
        ValueError: If the JSON data is invalid.
    """
    
    try:
        # Validate the lengths of all string values in the JSON data
        _validate_lengths_of_strs(data)
        
        # Extract the date of birth from the JSON data
        dob = data.get('individual_metadata', {}).get('date_of_birth')
        
        # Validate the dates in the JSON data
        _validate_dates_in_file(data)
        
        # If date of birth is present, validate the age
        if dob:
            _validate_age(dob)
    except ValueError as e:
        # Raise a ValueError if any validation fails
        raise ValueError(f"Invalid data: {str(e)}")
    
    # Remove sensitive data from the JSON data
    data = _remove_sensitive_data(data)
    
    # Return the processed JSON data
    return data

def process_json_file(file_path : str) -> dict:
    
    """
    Load and process a JSON file.

    This function validates and sanitizes JSON data, ensuring it meets specific
    requirements and removing sensitive information. It performs the following steps:
    1. Validates that all strings are under 64 characters.
    2. Ensures all dates are in 'YYYY-MM-DD' format and within the range 
       '2014-01-01' to '2024-12-31' (excluding 'date_of_birth').
    3. Checks if the participant's age is at least 40 years based on 'date_of_birth'.
    4. Removes keys that start with an underscore ('_') from the JSON data.

    Args:
        file_path (str): The file path to the JSON file.

    Returns:
        dict: The sanitized and validated JSON data.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file is not a valid JSON format.
        ValueError: If the JSON data does not pass validation checks.

    Examples:
        Example of a valid JSON file:
            Input:
                {
                    "individual_metadata": {"date_of_birth": "1980-05-15", "_id": "12345"},
                    "details": {"description": "Valid entry.", "date": "2024-01-01"}
                }

            Output:
                {
                    "individual_metadata": {"date_of_birth": "1980-05-15"},
                    "details": {"description": "Valid entry.", "date": "2024-01-01"}
                }
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return _process_json_file(data)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except json.JSONDecodeError:
        raise json.JSONDecodeError("Invalid JSON file format.", "", 0)
    except ValueError as e:
        raise ValueError(f"Invalid data in file: {str(e)}")
