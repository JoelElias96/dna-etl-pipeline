import pytest
import uuid
from pathlib import Path
from utils.input_validation import InputValidator


class TestValidationStructure:
    
    def test_validate_structure(self):
        input_data = {"context_path": "context", "results_path": "results"}
        validator = InputValidator(input_data, [])
        validator._validate_structure()
    
    def test_validate_structure_missing_context_path(self):
        input_data = {"results_path": "results"}
        validator = InputValidator(input_data, [])
        with pytest.raises(ValueError):
            validator._validate_structure()
    
    def test_validate_structure_missing_results_path(self):
        input_data = {"context_path": "context"}
        validator = InputValidator(input_data, [])
        with pytest.raises(ValueError):
            validator._validate_structure()

    def test_validate_structure_empty_input(self):
        input_data = {}
        validator = InputValidator(input_data, [])
        with pytest.raises(ValueError):
            validator._validate_structure()

    def test_validate_structure_invalid_input(self):
        input_data = {"context": "context", "results": "results"}
        validator = InputValidator(input_data, [])
        with pytest.raises(ValueError):
            validator._validate_structure()
    
    def test_validate_structure_extra_keys(self):
        input_data = {"context_path": "context", "results_path": "results", "extra_key": "value"}
        validator = InputValidator(input_data, [])
        with pytest.raises(ValueError):
            validator._validate_structure()

    def test_no_str_in_value(self):
        input_data = {"context_path": 5, "results_path": ["results"]}
        validator = InputValidator(input_data, [])
        with pytest.raises(ValueError):
            validator._validate_structure()
    
    def test_no_str_in_key(self):
        input_data = {5: "context", "results_path": "results"}
        validator = InputValidator(input_data, [])
        with pytest.raises(ValueError):
            validator._validate_structure()


class TestValidationPaths:
    def test_valid_paths(self, tmp_path):
        uuid_str = str(uuid.uuid4())
        context_path = Path(tmp_path / uuid_str)
        context_path.mkdir(parents=True)
        results_path = Path(tmp_path / uuid_str / "out")
        results_path.mkdir(parents=True)
        input_data = {"context_path": str(context_path), "results_path": str(results_path)}
        validator = InputValidator(input_data, [])
        validator._validate_paths()

    def test_invalid_context_path_not_uuid(self, tmp_path):
        context_path = Path(tmp_path / "not_a_uuid")
        context_path.mkdir(parents=True)
        results_path = Path(tmp_path / "not_a_uuid" / "out")
        results_path.mkdir(parents=True)
        input_data = {"context_path": str(context_path), "results_path": str(results_path)}
        validator = InputValidator(input_data, [])
        with pytest.raises(ValueError, match="Invalid context_path structure"):
            validator._validate_paths()

    def test_invalid_results_path_not_uuid(self, tmp_path):
        uuid_str = str(uuid.uuid4())
        context_path = Path(tmp_path / uuid_str)
        context_path.mkdir(parents=True)
        results_path = Path(tmp_path / "not_a_uuid" / "out")
        results_path.mkdir(parents=True)
        input_data = {"context_path": str(context_path), "results_path": str(results_path)}
        validator = InputValidator(input_data, [])
        with pytest.raises(ValueError, match="Invalid results_path structure"):
            validator._validate_paths()

    def test_no_out_in_results(self, tmp_path):
        uuid_str = str(uuid.uuid4())
        context_path = Path(tmp_path / uuid_str)
        context_path.mkdir(parents=True)
        results_path = Path(tmp_path / uuid_str / "not_out")
        results_path.mkdir(parents=True)
        input_data = {"context_path": str(context_path), "results_path": str(results_path)}
        validator = InputValidator(input_data, [])
        with pytest.raises(ValueError, match="Invalid results_path structure"):
            validator._validate_paths()

    def test_empty_context_path(self, tmp_path):
        uuid_str = str(uuid.uuid4())
        results_path = Path(tmp_path / uuid_str / "out")
        results_path.mkdir(parents=True)
        input_data = {"context_path": "", "results_path": str(results_path)}
        validator = InputValidator(input_data, [])
        with pytest.raises(ValueError, match="context_path is empty."):
            validator._validate_paths()

    def test_empty_results_path(self, tmp_path):
        uuid_str = str(uuid.uuid4())
        context_path = Path(tmp_path / uuid_str)
        context_path.mkdir(parents=True)
        input_data = {"context_path": str(context_path), "results_path": ""}
        validator = InputValidator(input_data, [])
        with pytest.raises(ValueError, match="results_path is empty."):
            validator._validate_paths()

    def test_both_empty_paths(self):
        input_data = {"context_path": "", "results_path": ""}
        validator = InputValidator(input_data, [])
        with pytest.raises(ValueError, match="context_path is empty."):
            validator._validate_paths()


class TestNormalizePath:
    def test_normalize_paths_with_valid_inputs(self):
        validator = InputValidator({}, [])
        context_path = "C:\\Users\\test\\Documents\\context"
        results_path = "C:\\Users\\test\\Documents\\results"
        expected_context_path = str(Path(context_path).resolve())
        expected_results_path = str(Path(results_path).resolve())
        validator.context_path = context_path
        validator.results_path = results_path
        validator._normalize_paths()
        assert validator.context_path == expected_context_path
        assert validator.results_path == expected_results_path

    def test_normalize_paths_with_nonexistent_paths(self):
        validator = InputValidator({}, [])
        context_path = "C:\\Invalid\\Context"
        results_path = "C:\\Invalid\\Results"
        validator.context_path = context_path
        validator.results_path = results_path
        validator._normalize_paths()
        assert validator.context_path == str(Path(context_path).resolve())
        assert validator.results_path == str(Path(results_path).resolve())

    def test_normalize_paths_with_relative_paths(self):
        validator = InputValidator({}, [])
        context_path = "..\\relative\\context"
        results_path = "..\\relative\\results"
        expected_context_path = str(Path(context_path).resolve())
        expected_results_path = str(Path(results_path).resolve())
        validator.context_path = context_path
        validator.results_path = results_path
        validator._normalize_paths()
        assert validator.context_path == expected_context_path
        assert validator.results_path == expected_results_path

    def test_normalize_paths_with_special_characters(self):
        validator = InputValidator({}, [])
        context_path = "C:\\special_@#$\\context"
        results_path = "C:\\special_@#$\\results"
        expected_context_path = str(Path(context_path).resolve())
        expected_results_path = str(Path(results_path).resolve())
        validator.context_path = context_path
        validator.results_path = results_path
        validator._normalize_paths()
        assert validator.context_path == expected_context_path
        assert validator.results_path == expected_results_path

    def test_normalize_paths_with_ios_paths(self):
        validator = InputValidator({}, [])
        context_path = "/Users/test/Documents/context"
        results_path = "/Users/test/Documents/results"
        expected_context_path = str(Path(context_path).resolve())
        expected_results_path = str(Path(results_path).resolve())
        validator.context_path = context_path
        validator.results_path = results_path
        validator._normalize_paths()
        assert validator.context_path == expected_context_path
        assert validator.results_path == expected_results_path

    def test_normalize_paths_with_windows_paths(self):
        validator = InputValidator({}, [])
        context_path = "C:\\Users\\test\\Documents\\context"
        results_path = "C:\\Users\\test\\Documents\\results"
        expected_context_path = str(Path(context_path).resolve())
        expected_results_path = str(Path(results_path).resolve())
        validator.context_path = context_path
        validator.results_path = results_path
        validator._normalize_paths()
        assert validator.context_path == expected_context_path
        assert validator.results_path == expected_results_path


class TestUUIDValidation:
    def test_valid_uuid_in_path(self, tmp_path):
        uuid_str = str(uuid.uuid4())
        context_path = Path(tmp_path / uuid_str)
        results_path = Path(tmp_path / uuid_str / "out")
        context_path.mkdir(parents=True)
        results_path.mkdir(parents=True)
        input_data = {"context_path": str(context_path), "results_path": str(results_path)}
        validator = InputValidator(input_data, [])
        validator._extract_uuid_and_check_validity()
        assert validator.current_uuid == uuid_str
    

    def test_invalid_uuid_in_context_path(self, tmp_path):
        context_path = Path(tmp_path / "not_a_uuid")
        results_path = Path(tmp_path / "not_a_uuid" / "out")
        context_path.mkdir(parents=True)
        results_path.mkdir(parents=True)
        input_data = {"context_path": str(context_path), "results_path": str(results_path)}
        validator = InputValidator(input_data, [])
        with pytest.raises(ValueError):
            validator._extract_uuid_and_check_validity()

    def test_invalid_uuid_in_results_path(self, tmp_path):
        uuid_str = str(uuid.uuid4())
        context_path = Path(tmp_path / uuid_str)
        results_path = Path(tmp_path / "not_a_uuid" / "out")
        context_path.mkdir(parents=True)
        results_path.mkdir(parents=True)
        input_data = {"context_path": str(context_path), "results_path": str(results_path)}
        validator = InputValidator(input_data, [])
        with pytest.raises(ValueError):
            validator._extract_uuid_and_check_validity()

    def test_uuid_mismatch(self, tmp_path):
        uuid1 = str(uuid.uuid4())
        uuid2 = str(uuid.uuid4())
        context_path = Path(tmp_path / uuid1)
        results_path = Path(tmp_path / uuid2 / "out")
        context_path.mkdir(parents=True)
        results_path.mkdir(parents=True)
        input_data = {"context_path": str(context_path), "results_path": str(results_path)}
        validator = InputValidator(input_data, [])
        with pytest.raises(ValueError):
            validator._extract_uuid_and_check_validity()


class TestValidateFiles:

    def test_validate_files_with_valid_context(self, tmp_path):
        context_uuid = str(uuid.uuid4())
        context_path = Path(tmp_path) / "context" / context_uuid
        results_path = Path(tmp_path) / "results" / context_uuid / "out"
        context_path.mkdir(parents=True)
        results_path.mkdir(parents=True)
        file1 = context_path / f"{context_uuid}_dna.txt"
        file2 = context_path / f"{context_uuid}_dna.json"
        file1.touch()
        file2.touch()

        validator = InputValidator({"context_path": str(context_path), "results_path": str(results_path)}, ["txt", "json"])
        validator._extract_uuid_and_check_validity()
        validator._validate_files()

        result = validator.files
        expected_result = [f"{context_uuid}_dna.txt", f"{context_uuid}_dna.json"]

        expected_result.sort()  # Sort only the expected result
        assert result == expected_result

    def test_validate_files_with_invalid_extension(self, tmp_path):
        context_uuid = str(uuid.uuid4())
        context_path = Path(tmp_path) / "context" / context_uuid
        results_path = Path(tmp_path) / "results" / context_uuid / "out"
        context_path.mkdir(parents=True)
        results_path.mkdir(parents=True)
        file1 = context_path / "sample1.invalid"
        file1.touch()

        validator = InputValidator({"context_path": str(context_path), "results_path": str(results_path)}, ["txt"])

        with pytest.raises(ValueError):
            validator._validate_files()

    def test_validate_files_empty_directory(self, tmp_path):
        context_uuid = str(uuid.uuid4())
        context_path = Path(tmp_path) / "context" / context_uuid
        results_path = Path(tmp_path) / "results" / context_uuid / "out"
        context_path.mkdir(parents=True)
        results_path.mkdir(parents=True)

        validator = InputValidator({"context_path": str(context_path), "results_path": str(results_path)}, ["txt"])

        with pytest.raises(ValueError, match="The context_path directory is empty"):
            validator._validate_files()

    def test_validate_files_with_correct_uuid(self, tmp_path):
        context_uuid = str(uuid.uuid4())
        context_path = Path(tmp_path) / "context" / context_uuid
        results_path = Path(tmp_path) / "results" / context_uuid / "out"
        context_path.mkdir(parents=True)
        results_path.mkdir(parents=True)

        file1 = context_path / f"{context_uuid}_dna.txt"
        file1.touch()

        validator = InputValidator({"context_path": str(context_path), "results_path": str(results_path)}, ["txt"])
        validator._extract_uuid_and_check_validity()
        validator._validate_files()

        result = validator.files
        expected_result = [f"{context_uuid}_dna.txt"]

        expected_result.sort()  # Sort only the expected result
        assert result == expected_result

    def test_validate_files_with_mismatched_uuid(self, tmp_path):
        context_uuid = str(uuid.uuid4())
        context_path = Path(tmp_path) / "context" / context_uuid
        results_path = Path(tmp_path) / "results" / context_uuid / "out"
        context_path.mkdir(parents=True)
        results_path.mkdir(parents=True)
        file1 = context_path / "wrong_uuid_file1.txt"
        file1.touch()

        validator = InputValidator({"context_path": str(context_path), "results_path": str(results_path)}, ["txt"])

        with pytest.raises(ValueError, match="does not match the current UUID"):
            validator._validate_files()

    def test_validate_files_with_files_not_matching_uuid(self, tmp_path):
        context_uuid = str(uuid.uuid4())
        context_path = Path(tmp_path) / "context" / context_uuid
        results_path = Path(tmp_path) / "results" / context_uuid / "out"
        context_path.mkdir(parents=True)
        results_path.mkdir(parents=True)
        file1 = context_path / f"{str(uuid.uuid4())}_dna.txt"
        file1.touch()

        validator = InputValidator({"context_path": str(context_path), "results_path": str(results_path)}, ["txt"])

        with pytest.raises(ValueError):
            validator._validate_files()

    def test_validate_files_with_no_files(self, tmp_path):
        context_uuid = str(uuid.uuid4())
        context_path = Path(tmp_path) / "context" / context_uuid
        results_path = Path(tmp_path) / "results" / context_uuid / "out"
        context_path.mkdir(parents=True)
        results_path.mkdir(parents=True)

        validator = InputValidator({"context_path": str(context_path), "results_path": str(results_path)}, ["txt"])

        with pytest.raises(ValueError, match="The context_path directory is empty"):
            validator._validate_files()

    def test_validate_files_multiple_valid_files(self, tmp_path):
        context_uuid = str(uuid.uuid4())
        context_path = Path(tmp_path) / "context" / context_uuid
        results_path = Path(tmp_path) / "results" / context_uuid / "out"
        context_path.mkdir(parents=True)
        results_path.mkdir(parents=True)

        file1 = context_path / f"{context_uuid}_dna.txt"
        file2 = context_path / f"{context_uuid}_dna.csv"
        file3 = context_path / f"{context_uuid}_dna.json"
        file4 = context_path / f"{context_uuid}_dna.xlsx"
        file1.touch()
        file2.touch()
        file3.touch()
        file4.touch()

        validator = InputValidator({"context_path": str(context_path), "results_path": str(results_path)}, ["txt", "json", "csv", "xlsx"])
        validator._extract_uuid_and_check_validity()
        validator._validate_files()

        result = validator.files
        expected_result = [f"{context_uuid}_dna.txt", f"{context_uuid}_dna.json", f"{context_uuid}_dna.csv", f"{context_uuid}_dna.xlsx"]
        
        expected_result.sort()  # Sort only the expected result
        assert result == expected_result

    def test_validate_files_with_multyple_invalid_files(self, tmp_path):
        context_uuid = str(uuid.uuid4())
        context_path = Path(tmp_path) / "context" / context_uuid
        results_path = Path(tmp_path) / "results" / context_uuid / "out"
        context_path.mkdir(parents=True)
        results_path.mkdir(parents=True)

        file1 = context_path / f"{context_uuid}_dna.txt"
        file2 = context_path / f"{context_uuid}_dna.csv"
        file3 = context_path / f"invalid_dna.json"
        file4 = context_path / f"{context_uuid}_dna.xlsx"
        file1.touch()
        file2.touch()
        file3.touch()
        file4.touch()

        validator = InputValidator({"context_path": str(context_path), "results_path": str(results_path)}, ["txt", "json"])

        with pytest.raises(ValueError):
            validator._validate_files()

    def test_validate_with_valid_input(self, tmp_path):
        context_uuid = str(uuid.uuid4())
        context_path = Path(tmp_path) / "context" / context_uuid
        results_path = Path(tmp_path) / "results" / context_uuid / "out"
        context_path.mkdir(parents=True)
        results_path.mkdir(parents=True)

        file1 = context_path / f"{context_uuid}_dna.txt"
        file2 = context_path / f"{context_uuid}_dna.json"
        file1.touch()
        file2.touch()

        input_data = {
            "context_path": str(context_path),
            "results_path": str(results_path)
        }

        validator = InputValidator(input_data, ["txt", "json"])
        validator._extract_uuid_and_check_validity()
        validator._validate_files()

        result = validator.files
        expected_result = [f"{context_uuid}_dna.txt", f"{context_uuid}_dna.json"]

        expected_result.sort()  # Sort only the expected result
        assert result == expected_result


class TestValidateMethod:

    def test_validate_with_valid_input(self, tmp_path):
        context_uuid = str(uuid.uuid4())
        context_path = Path(tmp_path) / "context" / context_uuid
        results_path = Path(tmp_path) / "results" / context_uuid / "out"
        context_path.mkdir(parents=True)
        results_path.mkdir(parents=True)

        file1 = context_path / f"{context_uuid}_dna.txt"
        file2 = context_path / f"{context_uuid}_dna.json"
        file1.touch()
        file2.touch()

        input_data = {
            "context_path": str(context_path),
            "results_path": str(results_path)
        }

        validator = InputValidator(input_data, ["txt", "json"])
        
        # Run validate method
        result = validator.validate()

        expected_result = [f"{context_uuid}_dna.txt", f"{context_uuid}_dna.json"]
        
        expected_result.sort()  # Sort only the expected result
        assert result == (expected_result, context_uuid)
