from pipeline.processors.file_processor_factory import FileProcessorFactory
import os
from typing import List, Dict, Tuple


class Transform:
    """
    A class responsible for transforming data from a list of files based on their extensions.

    This class takes in a list of file names and input data, processes each file using the appropriate
    processor, and transforms the data based on the file type (e.g., CSV, JSON, etc.).

    Attributes:
        files (List[str]): A list of file names to be processed.
        input_data (dict): A dictionary containing the context path and other necessary data for processing files.

    Methods:
        transform_data() -> Dict:
            Transforms the data from the provided files using the appropriate processor based on file extensions.

        _get_processor(file: str) -> Tuple[FileProcessorFactory, str]:
            Helper method that creates and retrieves the correct file processor
            based on the file's extension.
    """

    def __init__(self, files: List[str], input_data: Dict) -> None:
        """
        Initialize the Transform class with a list of files and input data.

        :param files: A list of file names that need to be processed.
        :type files: List[str]
        :param input_data: A dictionary containing the context path and other configuration data for processing.
        :type input_data: dict
        """
        self.files = files
        self.input_data = input_data
        self.processed_results = {}

    def transformer(self) -> Dict:
        """
        Transforms the data from the provided files using the appropriate processor based on their extensions.

        This method iterates over the list of files, determines the processor based on the file extension,
        processes each file, and stores the result in `processed_results`.

        :return: A Dict containing the transformed data for each file with the file extensions as the key.
        :rtype: Dict
        """
        transformed_data = {}

        for file in self.files:
            # Instantiate the processor with the file path
            processor, file_extension = self._get_processor(file)

            # Process the file and store the result
            self.processed_results[file_extension] = processor.process()

        return transformed_data

    def _get_processor(self, file: str) -> Tuple[FileProcessorFactory, str]:
        """
        Creates and retrieves the correct processor for a given file based on its extension.

        This helper method splits the file name to extract its extension and uses the `FileProcessorFactory`
        to create a processor that is suitable for handling that file type.

        :param file: The file name to determine the processor for.
        :type file: str

        :return: A tuple containing the processor instance and the file extension.
        :rtype: Tuple[FileProcessorFactory, str]
        """
        # Extract the file extension
        file_extension = file.split('.')[-1].lower()

        file_path = os.path.join(self.input_data["context_path"], file)

        return FileProcessorFactory.create_processor(file_path, file_extension), file_extension
