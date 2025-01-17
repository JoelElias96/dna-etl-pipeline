import os
from pathlib import Path
from typing import Tuple, List, Dict
import json
from utils.input_validation import InputValidator


class Extractor:
    """
    A class responsible for extracting files and UUID from a given context path provided in the input JSON file.

    The Extractor class processes an input JSON file containing a context path and validates it
      using the InputValidator.
    It then extracts:
    - A list of files from the specified directory.
    - The UUID from the directory name (assumed to be part of the context path).

    Attributes:
        input_data_file (str): The file path of the input JSON file containing the context path and the result path.
        valid_extensions (List[str]): A list of valid file extensions to filter files for extraction.
        Default includes 'txt' and 'json'.

    Methods:
        extract() -> Tuple[List[str], str, Dict]:
            Main method that extracts the list of files from the context path, the UUID from the directory name,
            and returns the full input data for further use.

        _process_json_input_file_() -> Dict:
            Loads and processes the JSON input file, returning it as a dictionary.

        _extract_files(context_path: str) -> List[str]:
            Helper method to retrieve a list of valid files (based on extensions) present in the context directory.

        _extract_uuid(context_path: str) -> str:
            Helper method to extract the UUID, assumed to be the name of the directory in the context path.
    """

    def __init__(self, input_data_file: str, valid_extensions: List[str] = ["txt", "json"]):
        """
        Initialize the Extractor class with the input data file and valid file extensions.

        :param input_data_file: Path to the input JSON file containing the context path and result path.
        :type input_data_file: str
        :param valid_extensions: A list of valid file extensions to be extracted (optional).
        :type valid_extensions: List[str]
        """
        self.input_data_file = input_data_file
        self.valid_extensions = valid_extensions

    def extract(self) -> Tuple[List[str], str, Dict]:
        """
        Extracts both the list of files in the context directory and the UUID from the context path,
        and returns the full input data dictionary.

        This method calls `_extract_files` to get a list of files and `_extract_uuid` to extract the UUID
        from the context path. It also validates the input data using `InputValidator`.

        :return: A tuple containing:
            - A list of filenames found in the context directory.
            - The UUID extracted from the context path.
            - The full input data dictionary from the JSON input file.
        :rtype: Tuple[List[str], str, Dict]
        :raises ValueError: If the input data is invalid according to the validation rules.
        """
        # Load and process the JSON input file
        input_data = self._process_json_input_file_()

        # Validate the input data
        validator = InputValidator(input_data, self.valid_extensions)
        validator.validate()

        # Extract files and UUID from the context path
        context_path = input_data.get("context_path")
        return self._extract_files(context_path), self._extract_uuid(context_path), input_data

    def _process_json_input_file_(self) -> Dict:
        """
        Loads and processes the JSON input file, handling any file reading or JSON decoding errors.

        :return: The data parsed from the JSON file.
        :rtype: Dict
        :raises FileNotFoundError: If the input file does not exist.
        :raises ValueError: If the JSON file is invalid or malformed.
        """
        try:
            with open(self.input_data_file, 'r') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.input_data_file}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON file: {self.input_data_file}")

    def _extract_files(self, context_path: str) -> List:
        """
        Extracts the files from the specified context directory.

        This method retrieves all files from the directory specified by `context_path`,
        filtering by valid file extensions.

        :param context_path: The path of the context directory.
        :type context_path: str

        :return: A list of filenames in the context directory that match the valid extensions.
        :rtype: List[str]
        :raises FileNotFoundError: If the context path does not exist.
        """
        # Validate if the context path exists
        if not os.path.exists(context_path):
            raise FileNotFoundError(f"The context path does not exist: {context_path}")

        files_list = [
            f for f in os.listdir(context_path)
            if os.path.isfile(os.path.join(context_path, f)) and f.split('.')[-1] in self.valid_extensions
        ]
        return files_list

    def _extract_uuid(self, context_path: str) -> str:
        """
        Extracts the UUID from the context path.

        This method assumes that the UUID is part of the directory name in the context path.

        :param context_path: The path of the context directory.
        :type context_path: str

        :return: The UUID extracted from the context path directory name.
        :rtype: str
        :raises ValueError: If the context path is invalid and does not contain a valid UUID.
        """
        context_uuid_dir = Path(context_path).name
        if not context_uuid_dir:
            raise ValueError(f"Invalid context path: {context_path} does not contain a valid UUID.")
        return context_uuid_dir
