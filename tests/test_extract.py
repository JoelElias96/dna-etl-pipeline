import pytest
from pathlib import Path
from pipeline.extract import Extractor


class TestExtractFiles:

    def test_extract_files(self, tmp_path):
        # Create a temporary directory
        context_path = tmp_path / "context"
        context_path.mkdir()
        # Create a few files in the temporary directory
        file1 = context_path / "file1.csv"
        file1.write_text("data1")
        file2 = context_path / "file2.csv"
        file2.write_text("data2")
        
        # Ensure backslashes are escaped correctly for JSON
        context_path_str = str(context_path).replace("\\", "/")  # Replace backslashes with forward slashes
        results_path_str = str(tmp_path).replace("\\", "/")  # Assuming results_path is in the temp directory
        
        # Create an input data file with both context_path and results_path
        input_data_file = tmp_path / "input.json"
        input_data_file.write_text(f'{{"context_path": "{context_path_str}", "results_path": "{results_path_str}"}}')
    
        # Initialize the Extract class with the input data file
        extract = Extractor(str(input_data_file))
    
        # Extract the files from the context path
        files_list, uuid, input_data = extract.extract()

        # Check if the files are extracted correctly
        assert files_list == ["file1.csv", "file2.csv"]

    def test_extract_multyple_files(self, tmp_path):
        # Create a temporary directory
        context_path = tmp_path / "context"
        context_path.mkdir()
        
        # Create a few files in the temporary directory
        file1 = context_path / "file1.csv"
        file1.write_text("data1")
        file2 = context_path / "file2.java"
        file2.write_text("data2")
        file3 = context_path / "file3.py"
        file3.write_text("data3")
        file4 = context_path / "file4.json"
        file4.write_text("data4")
        file5 = context_path / "file5.txt"
        file5.write_text("data5")
        file6 = context_path / "file6.pdf"
        file6.write_text("data6")
        file7 = context_path / "file7.xlsx"
        file7.write_text("data7")
        file8 = context_path / "file8.docx"
        file8.write_text("data8")
        
        # Ensure backslashes are escaped correctly for JSON
        context_path_str = str(context_path).replace("\\", "/")  # Replace backslashes with forward slashes
        results_path_str = str(tmp_path).replace("\\", "/")  # Assuming results_path is in the temp directory
        
        # Create an input data file with both context_path and results_path
        input_data_file = tmp_path / "input.json"
        input_data_file.write_text(f'{{"context_path": "{context_path_str}", "results_path": "{results_path_str}"}}')
        
        # Initialize the Extract class with the input data file
        extract = Extractor(str(input_data_file))
        
        # Extract the files from the context path
        files_list, uuid, input_data = extract.extract()

        # Check if the files are extracted correctly
        assert sorted(files_list) == sorted([
            "file1.csv", "file2.java", "file3.py", "file4.json", "file5.txt",
            "file6.pdf", "file7.xlsx", "file8.docx"
        ])


class TestProcessJsonInputFile:

    def test_process_json_input_file(self, tmp_path):
        # Create a temporary JSON file
        input_data_file = tmp_path / "input.json"
        input_data_file.write_text('{"context_path": "context", "results_path": "results"}')
        
        # Initialize the Extract class with the input data file
        extract = Extractor(str(input_data_file))
        
        # Process the JSON input file
        input_data = extract._process_json_input_file_()

        # Check if the input data is processed correctly
        assert input_data == {"context_path": "context", "results_path": "results"}

    def test_process_json_input_file_invalid(self, tmp_path):
        # Create a temporary JSON file with invalid data
        input_data_file = tmp_path / "input.jso"
        input_data_file.write_text('{"invalid_key": "context"}')
        
        # Initialize the Extract class with the input data file
        extract = Extractor(str(input_data_file))
        
        # Process the JSON input file
        with pytest.raises(ValueError):  # Expecting a ValueError, not KeyError
            extract._process_json_input_file_()


class TestExtract:

    def test_extract(self, tmp_path):
        # Create a temporary directory
        context_path = tmp_path / "context"
        context_path.mkdir()
        
        # Create a few files in the temporary directory
        file1 = context_path / "file1.csv"
        file1.write_text("data1")
        file2 = context_path / "file2.csv"
        file2.write_text("data2")
        
        # Ensure backslashes are escaped correctly for JSON
        context_path_str = str(context_path).replace("\\", "/")  # Replace backslashes with forward slashes
        results_path_str = str(tmp_path).replace("\\", "/")  # Assuming results_path is in the temp directory
        
        # Create an input data file with both context_path and results_path
        input_data_file = tmp_path / "input.json"
        input_data_file.write_text(f'{{"context_path": "{context_path_str}", "results_path": "{results_path_str}"}}')
        
        # Initialize the Extract class with the input data file
        extract = Extractor(str(input_data_file))
        
        # Extract the files and the UUID from the context path
        files_list, uuid, input_data = extract.extract()

        # Check if the files and UUID are extracted correctly
        assert files_list == ["file1.csv", "file2.csv"]
        assert uuid == "context"
