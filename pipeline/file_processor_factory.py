from pipeline.metadata_json_processor import MetadataJsonProcessor
from pipeline.dna_txt_file_processor import DNATxtFileProcessor


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
            return MetadataJsonProcessor(file_path)
        elif file_type.lower() == 'txt':
            return DNATxtFileProcessor(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
