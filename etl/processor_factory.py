from .json_processor import JSONProcessor
from .txt_processor import TXTProcessor

class ProcessorFactory:
    @staticmethod
    def create_processor(file_path: str, file_type: str):
        """
        Factory method to create an instance of JSONProcessor or TXTProcessor.

        Args:
            file_path (str): The path to the file to be processed.
            file_type (str): The type of the file ('json' or 'txt').

        Returns:
            An instance of JSONProcessor or TXTProcessor.

        Raises:
            ValueError: If the file type is not supported.
        """
        if file_type.lower() == 'json':
            return JSONProcessor(file_path)
        elif file_type.lower() == 'txt':
            return TXTProcessor(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
