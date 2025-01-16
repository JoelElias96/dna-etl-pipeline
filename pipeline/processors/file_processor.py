from abc import ABC, abstractmethod


class AbstractFileProcessor(ABC):
    """
    Abstract Base Class for file processors.
    Defines the interface that all file processors must implement.
    contains the abstract method process() that must be implemented by subclasses.
    """

    def __init__(self, file_path: str):
        """
        Initialize the file processor with the given file path.
        :param file_path: The path to the file to be processed
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
