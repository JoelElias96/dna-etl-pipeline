import pytest
import os
import json
import uuid
from typing import List
from pipeline.etl_manager import ETLManager


class TestETLManager:

    def setup_files(
        self, 
        tmp_path, 
        uuid_str: str, 
        file_extensions: List[str] = ["txt", "json"], 
        files_content: List[object] = None, 
        wrong_uuid: bool = False
    ):
        """
        Helper method to set up mock files and directories for the tests.
        """
        context_path = tmp_path / uuid_str
        results_path = tmp_path / uuid_str / "out"
        os.makedirs(context_path, exist_ok=True)
        os.makedirs(results_path, exist_ok=True)

        # Default content for files if not provided
        if files_content is None:
            files_content = ["Sample content"] * len(file_extensions)

        if len(file_extensions) != len(files_content):
            raise ValueError("file_extensions and files_content must have the same length.")

        for ext, content in zip(file_extensions, files_content):

            file_uuid = str(uuid.uuid4()) if wrong_uuid else uuid_str
            file_name = f"{file_uuid}_dna.{ext}"

            file_path = context_path / file_name
            if ext == "json":
                with open(file_path, "w") as f:
                    json.dump(content, f)
            else:
                with open(file_path, "w") as f:
                    f.write(content)

        return {"context_path": str(context_path), "results_path": str(results_path)}

    def test_incorrect_metadata(self, tmp_path):
        """
        Tests incorrect metadata in the JSON file.
        """
        uuid = "f3324a99-8a63-4ada-9d1d-562f84c7636d"
        files_content = [
            "ATCGATCGTAGCTAGCTAGCTGATCGATCGAT", 
            {
                "individual_metadata": {
                    "_name": "John Doe",
                    "date_of_birth": "2010-01-01"  # Invalid age
                }
            }
        ]
        input_data = self.setup_files(tmp_path, uuid, files_content=files_content)

        etl_manager = ETLManager(input_data, number_of_files=2)

        with pytest.raises(RuntimeError):
            etl_manager.process()

    def test_long_dna_sequences(self, tmp_path):
        """
        Tests handling of very long DNA sequences.
        """
        uuid = "f3324a99-8a63-4ada-9d1d-562f84c7636d"
        long_sequence = "ATCG" * 100000  # Very long sequence
        files_content = [
            long_sequence,
            {
                "individual_metadata": {
                    "date_of_birth": "1980-01-01"
                }
            }
        ]
        input_data = self.setup_files(tmp_path, uuid, files_content=files_content)

        etl_manager = ETLManager(input_data, number_of_files=2)

        etl_manager.process()

        output_file = os.path.join(input_data["results_path"], f"{uuid}_result.json")
        assert os.path.exists(output_file), "Output file does not exist for long sequences."


    def test_duplicate_data(self, tmp_path):
        """
        Tests handling of duplicate data for the same participant.
        """
        uuid = "f3324a99-8a63-4ada-9d1d-562f84c7636d"
        files_content = [
            "ATCGATCGTAGCTAGCTAGCTGATCGATCGAT",
            {
                "individual_metadata": {
                    "date_of_birth": "1980-01-01"
                }
            }
        ]
        input_data = self.setup_files(tmp_path, uuid, files_content=files_content)

        etl_manager = ETLManager(input_data, number_of_files=2)

        # Process once
        etl_manager.process()

        # Process again to check override
        etl_manager.process()

        output_file = os.path.join(input_data["results_path"], f"{uuid}_result.json")
        assert os.path.exists(output_file), "Output file does not exist after duplicate processing."

    def test_empty_dna_sequence(self, tmp_path):
        """
        Tests processing of an empty DNA sequence file.
        """
        uuid = "f3324a99-8a63-4ada-9d1d-562f84c7636d"
        files_content = [
            "",  # Empty DNA sequence
            {
                "individual_metadata": {
                    "date_of_birth": "1980-01-01"
                }
            }
        ]
        input_data = self.setup_files(tmp_path, uuid, files_content=files_content)

        etl_manager = ETLManager(input_data, number_of_files=2)

        with pytest.raises(RuntimeError):
            etl_manager.process()

