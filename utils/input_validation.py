import os
import uuid
import re
from typing import List, Dict
from pathlib import Path


class InputValidator:
    """
    A utility class for validating input data, directory structures, and file extensions.

    This class ensures that the provided paths are valid directories,
    contain files with specified extensions, and organizes these files by their UUIDs.
    the class retrieves the UUID from the context_path and results_path,
    and returns a list of the files in the context_path directory and the current UUID.

    Attributes:
        input_data (dict): Dictionary containing 'context_path' and 'results_path' as keys.
        validate_extentions (list): List of valid file extensions to check against.
        context_path (str): Path to the directory containing the context files.
        results_path (str): Path to the directory where results are stored.
        file_mapping (dict): A mapping of UUIDs to their associated file paths.
        files (list): List of files in the 'context_path' directory.

    Methods:
        validate() -> dict:
            Validates the input data, paths, and files, and returns a UUID-to-file mapping.
    """

    def __init__(self, input_data: Dict, validate_extentions: List[str], num_of_files: int = 0) -> None:
        """
        Initialize the validator with the input data.

        :param input_data: A dictionary containing "context_path" and "results_path".
        :type input_data: dict
        :param validate_extentions: A list of valid file extensions.
        :type validate_extentions: list[str]
        :param num_of_files: The maximum number of files to validate for each UUID. (optional)
        :type num_of_files: int
        """

        self.input_data = input_data
        self.context_path = input_data.get("context_path", "")
        self.results_path = input_data.get("results_path", "")
        self.current_uuid = ""
        self.valid_extentions = set(validate_extentions)
        self.files = []
        self.num_of_files = len(self.valid_extentions) if num_of_files == 0 else num_of_files

    def validate(self) -> None:
        """
        Validates the input data and organizes files by their UUIDs.

        This function performs the following checks:
        1. Ensures the input dictionary contains required keys: 'context_path' and 'results_path'.
        2. Verifies that the specified paths exist and are valid directories.
        3. Confirms that the 'context_path' contains files with valid extensions.
        4. Groups files by their UUIDs and checks that each UUID has exactly one file for every required extension.

        Returns:
            dict: A mapping of UUIDs to their associated file paths.

        Raises:
            ValueError: If the input structure, paths, or files are invalid.
        """
        try:
            self._validate_structure()
            self._validate_paths()
            self._extract_uuid_and_check_validity()
            self._validate_files()
            self.files.sort()
            return self.files, self.current_uuid
        except ValueError as error:
            raise ValueError(error)

    def _normalize_paths(self) -> None:
        """
        Normalize and validate a given path to ensure it works across platforms.

        Raises:
            ValueError: If the input path is not a valid string or does not exist.
        """
        try:
            # Create a Path object and resolve the absolute path
            self.context_path = str(Path(self.context_path).resolve(strict=False))
        except Exception as e:
            raise ValueError(f"Error resolving path {self.context_path}: {e}")

        try:
            # Create a Path object and resolve the absolute path
            self.results_path = str(Path(self.results_path).resolve(strict=False))
        except Exception as e:
            raise ValueError(f"Error resolving path {self.results_path}: {e}")

    def _extract_uuid_and_check_validity(self) -> None:
        """
        Extract and validate UUIDs from the given paths.
        Ensure that the UUID in the context_path matches the UUID in the results_path.

        Raises:
            ValueError: If the UUIDs are missing, invalid, or do not match.
        """
        # Regular expression pattern for UUIDs
        uuid_pattern = r"[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}"

        # Extract UUID from context_path (should be the directory name)
        context_uuid_dir = Path(self.context_path).name

        # Extract UUID from results_path (should be the grandparent directory name of "out")
        results_uuid_dir = Path(self.results_path).parent.name

        # Validate the extracted UUIDs
        if not re.fullmatch(uuid_pattern, context_uuid_dir):
            raise ValueError(f"Invalid or missing UUID directory in context_path: {self.context_path}")

        # Check if the UUIDs match
        if context_uuid_dir != results_uuid_dir:
            raise ValueError(
                        f"UUID mismatch between context_path"
                        f"and results_path: {context_uuid_dir} != {results_uuid_dir}")

        # Set the current UUID
        self.current_uuid = context_uuid_dir

    def _is_uuid_valid(self, uuid_string: str) -> bool:
        """
        Check if the given string is a valid UUID.

        Args:
            uuid_string (str): A string to validate.

        Returns:
            bool: True if the string is a valid UUID, False otherwise.
        """
        try:
            # Attempt to create a UUID object
            uuid.UUID(uuid_string)
            # Return True since no exception was raised
            return True
        except (ValueError, AttributeError, TypeError):
            # Invalid UUID string
            return False

    def _validate_structure(self):
        """
        Check if input contains the required keys and values.

        Raises:
            ValueError: If the input does not contain the required keys.
        """
        if ("context_path" not in self.input_data or
                "results_path" not in self.input_data or
                len(self.input_data) != 2):
            raise ValueError("Input must contain 'context_path' and 'results_path'.")
        if not all(isinstance(value, str) for value in self.input_data.values()):
            raise ValueError("Values in the input dictionary must be strings.")
        if not all(isinstance(key, str) for key in self.input_data.keys()):
            raise ValueError("Keys in the input dictionary must be strings.")

    def _validate_paths(self):
        """
        Check if paths exist and have valid structures.

        Raises:
            ValueError: If the paths do not exist or do not match the expected structure.
        """
        # Check if context_path is empty
        if not self.context_path:
            raise ValueError("context_path is empty.")

        # Check if results_path is empty
        if not self.results_path:
            raise ValueError("results_path is empty.")

        # Check if context_path exists
        if not os.path.exists(self.context_path):
            raise ValueError(f"Invalid context_path: {self.context_path} does not exist.")

        # Check if context_path is a directory
        if not os.path.isdir(self.context_path):
            raise ValueError(f"Invalid context_path: {self.context_path} must be a directory.")

        # Check if results_path exists
        if not os.path.exists(self.results_path):
            raise ValueError(f"Invalid results_path: {self.results_path} does not exist.")

        # Check if results_path is a directory
        if not os.path.isdir(self.results_path):
            raise ValueError(f"Invalid results_path: {self.results_path} must be a directory.")

        # Validate the structure of context_path
        context_path_parts = Path(self.context_path).parts
        if len(context_path_parts) < 1 or not self._is_uuid_valid(context_path_parts[-1]):
            raise ValueError(
                            f"Invalid context_path structure: {self.context_path}. "
                            f"It must have a UUID as the directory name.")

        # Validate the structure of results_path
        results_path_parts = Path(self.results_path).parts
        if (len(results_path_parts) < 2 or results_path_parts[-1] != "out"
                or not self._is_uuid_valid(results_path_parts[-2])):
            raise ValueError(
                            f"Invalid results_path structure: {self.results_path}. "
                            f"It must have a UUID as the grandparent directory and 'out' as the parent directory.")

    def _validate_files(self):
        """
        Validate files in the context_path and organize them by UUID.

        Raises:
            ValueError: If the context_path directory is empty, if the file extensions are invalid,
              or if there are not exactly one file per required extension.
        """
        self._make_files_list()

        # Group files by UUID
        for file in self.files:
            # Extract UUID from the file name
            uuid = file.split("_", 1)[0]
            # Add the file to the mapping
            if uuid != self.current_uuid:
                raise ValueError(
                                f"UUID {uuid} does not match the current UUID {self.current_uuid},"
                                f"there is a file with a different UUID in the context_path directory.")

    def _make_files_list(self):
        """
        Validate files in the context_path and organize them by to a list.

        Raises:
            ValueError: If the context_path directory is empty
        """
        # List all files in the context_path directory that have valid extensions
        self.files = [
            f for f in os.listdir(self.context_path)
            if os.path.isfile(os.path.join(self.context_path, f))
        ]
        # Raise an error if there are no files in the context_path directory
        if not self.files:
            raise ValueError(f"The context_path directory is empty: {self.context_path}")
        self._validate_file_extensions()

    def _validate_file_extensions(self):
        """
        Validate the file extensions for each UUID according to the required extensions.

        Raises:
            ValueError: If the file extensions are invalid or if there are not exactly one file per required extension.
        """

        for file in self.files:
            # Extract the file extension
            file_extension = file.split(".")[-1]
            # Check if the file extension is valid
            if file_extension not in self.valid_extentions:
                raise ValueError(f"Invalid file extension: {file_extension} for file {file}.")
