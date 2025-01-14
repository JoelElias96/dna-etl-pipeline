from abc import ABC, abstractmethod

class AbstrctFileProcessor(ABC):
    """
    Abstract Base Class for file processors.
    Defines the interface that all file processors must implement.
    """

    def __init__(self, file_path: str):
        """
        Initialize the file processor with the given file path.
        
        Args:
            file_path (str): The path to the file to be processed.
        """
        self.file_path = file_path

    @abstractmethod
    def process(self) -> dict:
        """
        Abstract method to process the file.
        Subclasses must implement this method.

        Returns:
            dict: The processed data from the file.
        """
        pass
