import os

class InputValidator:

    valid_extensions = set()  # Changed to a set for adding extensions
    
    @staticmethod
    def add_valid_extension(extensions: list) -> None:
        """
        Add valid file extensions.

        Args:
            extensions (list): List of valid extensions.
        """
        for extension in extensions:
            InputValidator.valid_extensions.add(extension)

    @staticmethod
    def _validate_path(path: str) -> None:
        """
        Validate a given path to ensure it is a directory.

        Args:
            path (str): Path to validate.

        Raises:
            ValueError: If the path is not a valid directory.
        """
        if not os.path.isdir(path):
            raise ValueError(f"Invalid path: {path} is not a directory.")

    @staticmethod
    def validate(input_args: dict) -> None:
        """
        Validate input paths.

        Args:
            input_args (dict): Dictionary of input arguments with paths.

        Raises:
            ValueError: If any path is invalid.
        """
        for key, value in input_args.items():
            InputValidator._validate_path(value)  # Fixed call to static method
