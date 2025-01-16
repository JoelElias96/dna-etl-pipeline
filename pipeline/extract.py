import os
from pathlib import Path
from typing import Tuple, List


class Extract:
    """
    A class responsible for extracting files and the UUID from a given context path.

    This class takes in a dictionary containing a context path and processes it to:
    - Extract the list of files from the specified directory.
    - Extract the UUID from the context path (which is expected to be part of the directory name).

    Attributes:
        input_data (dict): A dictionary containing the context path and the result path.
            The `context_path` should be a directory path containing files to be extracted.

    Methods:
        extract() -> Tuple[List[str], str]:
            Extracts both the list of files in the context directory and the UUID from the context path.

        _extract_files(context_path: str) -> List[str]:
            Helper method that retrieves a list of files present in the context directory.

        _extract_uuid(context_path: str) -> str:
            Helper method that extracts the UUID (assumed to be the directory name) from the context path.
    """

    def __init__(self, input_data):
        """
        Initialize the Extract class with the input data.

        :param input_data: A dictionary containing the context path and the result path.
        :type input_data: dict
        """
        self.input_data = input_data

    def extract(self) -> Tuple[List, str]:
        """
        Extract the files and the UUID from the context path.

        This method calls `_extract_files` to get a list of files from the context path
        and `_extract_uuid` to get the UUID from the context path (derived from the directory name).

        :return: A tuple containing:
            - A list of filenames found in the context directory.
            - The UUID extracted from the context path.
        :rtype: Tuple[List[str], str]
        """
        context_path = self.input_data.get("context_path")
        return self._extract_files(context_path), self._extract_uuid(context_path)

    def _extract_files(self, context_path: str) -> List:
        """
        Extract the files from the context path.

        This method retrieves the list of files from the directory specified by `context_path`.

        :param context_path: The path of the context directory.
        :type context_path: str

        :return: A list of filenames in the context directory.
        :rtype: List[str]
        """
        files_list = os.listdir(context_path)
        return files_list

    def _extract_uuid(self, context_path: str) -> str:
        """
        Extract the UUID from the context path.

        This method extracts the UUID from the directory name of the `context_path`.

        :param context_path: The path of the context directory.
        :type context_path: str

        :return: The UUID extracted from the context path.
        :rtype: str
        """
        context_uuid_dir = Path(context_path).name
        return context_uuid_dir
