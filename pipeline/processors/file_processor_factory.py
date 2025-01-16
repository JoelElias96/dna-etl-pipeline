from pipeline.processors.test_metadata_json_processor import TestMetadataJsonProcessor
from pipeline.processors.dna_sequence_txt_processor import DNASequenceTxtProcessor


class FileProcessorFactory:
    @staticmethod
    def create_processor(file_path: str, file_type: str):
        """
        Factory method to create an instance of a file processor based on the file type.

        Args:
            file_path (str): The path to the file to be processed.
            file_type (str): The type of the file.

        Returns:
            An instance of the file processor.

        Raises:
            ValueError: If the file type is not supported.
        """
        if file_type.lower() == 'json':
            return TestMetadataJsonProcessor(file_path)
        elif file_type.lower() == 'txt':
            return DNASequenceTxtProcessor(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
