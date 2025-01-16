import json
from datetime import datetime
from utils.file_processor import AbstrctFileProcessor
import os


class MetadataJsonProcessor(AbstrctFileProcessor):
    
    """
        JSONProcessor is a class for processing and sanitizing JSON files.
        This class inherits from AbstractFileProcessor and provides methods to:
        - Load and process a JSON file.
        - Validate and sanitize JSON data.
        - Ensure all strings are under 64 characters.
        - Validate date formats and ranges.
        - Ensure participants are at least 40 years old based on their date of birth.
        - Remove sensitive information from the JSON data.
        Methods:
            __init__(file_path: str):
                Initializes the JSONProcessor with the given file path.
            process() -> dict:
                Loads and processes the JSON file, returning the sanitized and validated data.
            _process_json_data(data: dict) -> dict:
                Processes the JSON data by removing sensitive data, validating lengths, dates,
            _remove_sensitive_data(data: dict) -> dict:
                Removes sensitive fields from the JSON data.
            _validate_lengths_of_strs(data: dict) -> None:
                Ensures all string values in the JSON data are under 64 characters.
            _validate_dates_in_file(data: dict) -> None:
                Validates date fields in the JSON data to ensure they are in the correct format
                and within the allowed range.
            _validate_age(i_birth_date: str) -> None:
                Ensures the participant is at least 40 years old based on their date of birth.
    """
    def __init__(self, file_path: str):
        super().__init__(file_path)

    def process(self) -> dict:
        """
        Load and process a JSON file.

        This function validates and sanitizes JSON data, ensuring it meets specific
        requirements and removing sensitive information. It performs the following steps:
        1. Validates that all strings are under 64 characters.
        2. Ensures all dates are in 'YYYY-MM-DD' format and within the range 
           '2014-01-01' to '2024-12-31' (excluding 'date_of_birth').
        3. Checks if the participant's age is at least 40 years based on 'date_of_birth'.
        4. Removes keys that start with an underscore ('_') from the JSON data.

        Returns:
            dict: The sanitized and validated JSON data.

        Raises:
            FileNotFoundError: If the file does not exist.
            json.JSONDecodeError: If the file is not a valid JSON format.
            ValueError: If the JSON data does not pass validation checks.
        """
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                return self._process_json_data(data)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.file_path}")
        except json.JSONDecodeError:
            raise json.JSONDecodeError("Invalid JSON file format.", "", 0)
        except ValueError as e:
            raise ValueError(f"Invalid data in file: {str(e)}")

    def _process_json_data(self, data: dict) -> dict:
        """
        Process the JSON data by removing sensitive data, validating lengths, dates,
        and ensuring the participant's age is at least 40.

        Returns:
            dict: The processed JSON data.

        Raises:
            ValueError: If the JSON data is invalid.
        """
        # Validate the JSON data, raising a ValueError if any validation fails
        try:
            self._validate_lengths_of_strs(data)
            dob = data.get('individual_metadata', {}).get('date_of_birth')
            self._validate_dates_in_file(data)
            if dob:
                self._validate_age(dob)
        except ValueError as e:
            raise ValueError(f"Invalid data: {str(e)}")

        # Remove sensitive data from the JSON data
        return self._remove_sensitive_data(data)

    def _remove_sensitive_data(self, data: dict) -> dict:
        """
        Remove sensitive fields from the data (iterative).
        Iteratively remove sensitive fields from the JSON data.
        Sensitive fields are identified by keys that start with an underscore ('_').

        Args:
            data (dict): The JSON data.

        Returns:
            dict: The sanitized JSON data.
        """
        stack = [data]
        while stack:
            current = stack.pop()

            # Identify keys that start with an underscore
            if isinstance(current, dict):
                keys_to_remove = [key for key in current if key.startswith('_')]
                
                # Remove the identified keys
                for key in keys_to_remove:
                    del current[key]
                # Add the remaining values to the stack for further processing
                stack.extend(current.values())
            elif isinstance(current, list):
                # Add list items to the stack for further processing
                stack.extend(current)
        return data

    def _validate_lengths_of_strs(self, data: dict) -> None:
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
            if len(word) > 64:
                raise ValueError(f"The string '{word}' exceeds 64 characters.")
        # Use a stack to iteratively process the JSON data
        stack = [data]

        # Process the JSON data iteratively
        while stack:
            current = stack.pop()
            # Check if the current item is a dictionary, list, or string
            if isinstance(current, dict):
                for value in current.values():
                    # If the value is a string, validate its length
                    if isinstance(value, str) and not os.path.exists(value):
                        _validate_length_of_str(value)
                    else:
                        stack.append(value)
            # If the current item is a list, add its items to the stack
            elif isinstance(current, list):
                for item in current:
                    if isinstance(item, str):
                        # If the item is a string, validate its length
                        _validate_length_of_str(item)
                    else:
                        stack.append(item)

    def _validate_dates_in_file(self, data: dict) -> None:
        """
        Validate date fields in the JSON data.
        This function recursively checks all date fields in the provided JSON data
        (dictionary or list) to ensure they are in the 'YYYY-MM-DD' format and fall
        within the allowed range of 2014-01-01 to 2024-12-31.
        In case it's the birth date of the individual, it will skip the validation.

        Args:
            data (dict): The JSON data.

        Raises:
            ValueError: If any date is out of the allowed range or in an invalid format.
        """
        # Define the allowed date range as a tuple of datetime objects
        allowed_range = (datetime(2014, 1, 1), datetime(2024, 12, 31))

        def _validate_datetime_format(date_str: str) -> bool:
            """
            Validates if the given date string matches the format '%Y-%m-%d'.
            Args:
                date_str (str): The date string to validate.
            Returns:
                bool: True if the date string matches the format '%Y-%m-%d', False otherwise.
            """

            try:
                datetime.strptime(date_str, '%Y-%m-%d')
                return True
            except ValueError:
                return False

        def _date_in_allowed_range(date_str: str) -> None:
            """
            Check if the given date string is within the allowed range.
            Args:
                date_str (str): The date string in the format '%Y-%m-%d'.
            Raises:
                ValueError: If the date is not within the allowed range.
            """

            date = datetime.strptime(date_str, '%Y-%m-%d')
            if not allowed_range[0] <= date <= allowed_range[1]:
                raise ValueError(f"Date '{date_str}' is out of the allowed range.")

        # Use a stack to iteratively process the JSON data
        stack = [data]
        while stack:
            current = stack.pop()

            # Check if the current item is a dictionary, list, or string
            if isinstance(current, dict):
                for key, value in current.items():
                    # If the key is 'date_of_birth', skip the validation
                    if key != "date_of_birth":
                        stack.append(value)
            elif isinstance(current, list):
                stack.extend(current)
            # If the current item is a string, validate the date format and range
            elif isinstance(current, str) and _validate_datetime_format(current):
                _date_in_allowed_range(current)

    def _validate_age(self, i_birth_date: str) -> None:
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
        # Calculate the age based on the date of birth
        age = (datetime.now() - birth_date).days // 365
        if age < 40:
            raise ValueError("Participant must be at least 40 years old.")

