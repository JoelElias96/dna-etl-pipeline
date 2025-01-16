from datetime import datetime
from pipeline.extract import Extractor
from pipeline.transform import Transform
from pipeline.load import Loader
from utils.input_validation import InputValidator
from typing import List, Dict


class ETLManager:
    """
    A class that manages the entire ETL (Extract, Transform, Load) process.

    The ETLManager class handles the orchestration of the Extract, Transform, and Load stages for processing
    participant data. It validates input data, extracts the relevant files, transforms the data, and then loads
    the results into the specified output file.

    Attributes:
        input_data (dict): A dictionary containing the necessary configuration for the ETL process (e.g., paths).
        validator (InputValidator): An instance of InputValidator used to validate the input data.
        extractor (Extractor): An instance of Extractor used for extracting files and participant ID.
        transformer (Transform): An instance of Transform used for transforming the extracted data.
        loader (Loader): An instance of Loader used for loading the processed data into an output file.
        participant_id (str): The participant ID extracted during the ETL process.

    Methods:
        process():
            Executes the ETL process: validates input data, extracts files, transforms the data, and loads the results.

        _create_result_dictionary(processed_results, start_time, end_time):
            Creates a dictionary that includes metadata and the processed results to be saved to an output file.
    """

    def __init__(self, input_data: Dict, validate_extensions: List[str] = ["txt", "json"],) -> None:
        """
        Initializes the ETLManager class with the provided input data and file validation extensions.

        :param input_data: A dictionary containing the context and results paths,
        as well as any other necessary information.
        :type input_data: dict
        :param validate_extensions: A list of allowed file extensions for validation (default is ["txt", "json"]).
        :type validate_extensions: List[str]
        """
        self.input_data = input_data
        self.validator = InputValidator(input_data, validate_extensions)
        self.extractor = None
        self.transformer = None
        self.loader = None
        self.participant_id = None

    def process(self) -> None:
        """
        Orchestrates the ETL process: validation, extraction, transformation, and loading.

        This method validates the input data, extracts the necessary files and participant ID, transforms the data,
        creates a result dictionary, and then loads the results into an output file.
        The start and end times of the process are also recorded.

        :raises FileNotFoundError: If a file required during extraction or loading cannot be found.
        :raises ValueError: If the input data is invalid or cannot be processed.
        :raises RuntimeError: If an unexpected error occurs during the ETL process.
        """
        try:
            # Catch the start time before processing
            start_time = datetime.utcnow().isoformat()

            # Step 1: Validate the input
            self.validator.validate()

            # Step 2: Extract files and the uuid
            self.extractor = Extractor(self.input_data)
            files_list, self.participant_id = self.extractor.extract()

            # Step 3: Transform the data
            self.transformer = Transform(files_list, self.input_data)
            processed_results = self.transformer.transformer()

            # Catch the end time after processing
            end_time = datetime.utcnow().isoformat()

            # Step 3: Create the final result dictionary
            final_output = self._create_result_dictionary(processed_results, start_time, end_time)

            # Create result file path
            result_file_path = self.input_data["results_path"] + f"/{self.participant_id}_result.json"

            # Step 4: Load the results
            self.loader = Loader(self.input_data["results_path"])
            self.loader.load(final_output, result_file_path)

        except FileNotFoundError as e:
            raise FileNotFoundError(f"ETL process failed: {e}")
        except ValueError as e:
            raise ValueError(f"ETL process failed: {e}")
        except Exception as e:
            raise RuntimeError(f"ETL process failed: {e}")

    def _create_result_dictionary(self, processed_results: Dict, start_time: datetime, end_time: datetime) -> Dict:
        """
        Creates a result dictionary containing metadata and the processed results.

        This dictionary includes the start and end times of the ETL process,
        along with the paths for context and results.
        It also includes the processed results and participant ID for saving to the output file.

        :param processed_results: The transformed data that needs to be included in the result dictionary.
        :type processed_results: dict
        :param start_time: The start time of the ETL process in ISO format.
        :type start_time: datetime
        :param end_time: The end time of the ETL process in ISO format.
        :type end_time: datetime

        :return: A dictionary containing metadata and the processed results.
        :rtype: dict
        """
        return {
            "metadata": {
                "start_at": start_time,
                "end_at": end_time,
                "context_path": self.input_data["context_path"],
                "results_path": self.input_data["results_path"],
            },
            "results": [
                {
                    "participant": {"_id": self.participant_id},
                    **processed_results,
                }
            ],
        }
