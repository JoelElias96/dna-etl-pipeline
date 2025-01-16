import os
import json
from datetime import datetime
from pipeline.extract import Extract
from pipeline.transform import Transform
from pipeline.load import Load
from utils.input_validation import InputValidator
from typing import List, Dict


class ETLManager:  

    def __init__(self, input_data: Dict, 
                 validate_extensions: List[str] = ["txt", "json"],
                 number_of_files: int = -1) -> None:
        """
        Initialize the ETLManager with the input data and the file extensions to validate.
        :param input_data: A dictionary containing the context path and results path.
        :param validate_extensions: A list of file extensions to validate.
        :param number_of_file: The number of files to validate. If -1, all files will be validated.
        """  
      
        self.input_data = input_data
        self.validate_extensions = validate_extensions
        # Create an instance of the InputValidator
        if number_of_files == -1:
            self.validator = InputValidator(input_data, validate_extensions)
        else:
            self.validator = InputValidator(input_data, validate_extensions, number_of_files)
        self.participant_id = None
        self.start_time = None
        self.end_time = None
        self.processed_results = {}
        self.final_results = {}

    def process(self) -> None:
        try:
            # Catch the start time before processing
            self.start_time = datetime.utcnow().isoformat()

            # Step 1: Validate input and extract files and participant ID
            files, self.participant_id = self.validator.validate()

            # Step 2: Process each file using the appropriate processor
            for file in files:
                # Extract the file extension
                file_extension = file.split('.')[-1].lower()

                # Instantiate the processor with the file path
                processor = FileProcessorFactory.create_processor(os.path.join(self.input_data["context_path"], file), file_extension)

                # Raise an error if no processor is found for the file extension
                if not processor:
                    raise ValueError(f"No processor found for {file_extension} files.")

                # Process the file and store the result
                self.processed_results[file_extension] = processor.process()

            # Catch the end time after processing
            self.end_time = datetime.utcnow().isoformat()

            # Step 3: Combine results
            self._create_result_dictionary()

            # Step 4: Save the results to a file
            output_file = os.path.join(self.input_data["results_path"], f"{self.participant_id}_result.json")
            with open(output_file, "w") as f:
                json.dump(self.final_results, f, indent=4)
            
            print(f"Results saved to: {output_file}")
        except ValueError as e:
            raise ValueError(f"ETL process failed: {e}")
        except Exception as e:
            raise RuntimeError(f"ETL process failed: {e}")

    def _create_result_dictionary(self) -> None:

        self.final_results = {
            "metadata": {
                "start_at": self.start_time,
                "end_at": self.end_time,
                "context_path": self.input_data["context_path"],
                "results_path": self.input_data["results_path"],
            },
            "results": [
                {
                    "participant": {"_id": self.participant_id},
                    **self.processed_results,
                }
            ],
        }
     
