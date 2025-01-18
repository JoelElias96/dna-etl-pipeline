from datetime import datetime
from pipeline.extract import Extractor
from pipeline.transform import Transformer
from pipeline.load import Loader
from typing import Dict


class ETLManager:
    """
    A class that manages the entire ETL (Extract, Transform, Load) process.

    The ETLManager class orchestrates the extraction, transformation, and loading stages for processing
    participant data. It validates input data, extracts the relevant files, transforms the data, and then
    loads the results into the specified output file.

    Attributes:
        extractor (Extractor): An instance of the Extractor class used for extracting files and participant ID.
        transformer (Transformer): An instance of the Transformer class used for transforming the extracted data.
        loader (Loader): An instance of the Loader class used for loading the processed data into an output file.

    Methods:
        process(input_data_file: str) -> None:
            Executes the ETL process: validates input data, extracts files, transforms the data, and loads
            the results.

        _create_result_dictionary(input_data: Dict, processed_results: Dict, start_time: datetime,
        end_time: datetime) -> Dict:
            Creates a dictionary containing metadata and the processed results to be saved to an output file.
    """

    def __init__(self) -> None:
        """
        Initializes the ETLManager class with the provided input data file for the ETL process.

        :param input_data_file: A string containing the path to the input data file (JSON format).
        :type input_data_file: str
        """
        self.extractor = None
        self.transformer = None
        self.loader = None

    def process(self, input_data_file: str) -> None:
        """
        Orchestrates the ETL process: extraction, transformation, and loading.

        This method extracts the necessary files and participant ID, transforms the data, creates a result
        dictionary, and then loads the results into an output file. The start and end times of the process are
        also recorded.

        :param input_data_file: The file containing the input data (JSON format) for the extraction process.
        :type input_data_file: str

        :raises FileNotFoundError: If a required file during extraction or loading cannot be found.
        :raises ValueError: If the input data is invalid or cannot be processed.
        :raises RuntimeError: If an unexpected error occurs during the ETL process.
        """
        try:
            # Capture the start time before processing
            start_time = datetime.now().isoformat()

            # Step 1: Extract files and the participant ID
            self.extractor = Extractor(input_data_file)
            files_list, participant_id, input_data = self.extractor.extract()

            # Step 2: Transform the data
            self.transformer = Transformer(files_list, input_data)
            processed_results = self.transformer.transform()

            # Capture the end time after processing
            end_time = datetime.now().isoformat()

            # Step 3: Create the final result dictionary
            final_output = self._create_result_dictionary(
                input_data, participant_id, processed_results, start_time, end_time
            )

            # Define result file path
            result_file_path = input_data["results_path"] + f"/{participant_id}_result.json"

            # Step 4: Load the results
            self.loader = Loader(input_data["results_path"])
            self.loader.load(final_output, result_file_path)

        except FileNotFoundError as e:
            raise FileNotFoundError(f"ETL process failed: {e}")
        except ValueError as e:
            raise ValueError(f"ETL process failed: {e}")
        except Exception as e:
            raise RuntimeError(f"ETL process failed: {e}")

    def _create_result_dictionary(
        self, input_data: Dict, participant_id: str, processed_results: Dict, start_time: datetime, end_time: datetime
    ) -> Dict:
        """
        Creates a result dictionary containing metadata and the processed results.

        This dictionary includes the start and end times of the ETL process, along with the paths for context
        and results. It also includes the processed results and participant ID for saving to the output file.

        :param input_data: A dictionary containing context and results paths.
        :type input_data: dict
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
                "context_path": input_data["context_path"],
                "results_path": input_data["results_path"],
            },
            "results": [
                {
                    "participant": {"_id": participant_id},
                    "txt": processed_results["txt"],
                    "json": processed_results["json"],
                }
            ],
        }
