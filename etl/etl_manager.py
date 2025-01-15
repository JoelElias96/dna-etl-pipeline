import os
import json
from datetime import datetime
from etl.processor_factory import ProcessorFactory
from etl.input_validation import InputValidator
from typing import Dict, List

class ETLManager:
   
    def __init__(self, input_data: Dict, validate_extensions: List[str] = ["txt", "json"], number_of_file:int = -1) -> None:
        
        self.input_data = input_data
        self.validate_extensions = validate_extensions
        if number_of_file == -1:
            self.validator = InputValidator(input_data, validate_extensions)
        else:
            self.validator = InputValidator(input_data, validate_extensions, number_of_file)
        self.participant_id = None
        self.start_time= None
        self.end_time = None
        self.processed_results = {}
        self.final_results = {}


    def process(self) -> None:
       
        try:
            # Catch the start time before processing

            self.start_time = datetime.utcnow().isoformat()

            # Step 1: Validate input and extract files and participant ID

            files = self.validator.validate()
            self.participant_id = self.validator.get_this_uuid()

            # Step 2: Process each file using the appropriate processor
           
            for file in files:

                # Extract the file extension
                file_extension = file.split('.')[-1].lower() 

                # Instantiate the processor with the file path
                processor = ProcessorFactory.create_processor(os.path.join(self.input_data["context_path"], file), file_extension)

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
        
