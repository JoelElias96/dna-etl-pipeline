import pytest
import uuid
from pathlib import Path
from etl.input_validation import InputValidator

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
