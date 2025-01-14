import pytest
import uuid
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
    
class TestValidationPaths:    
    def test_validate_paths(self, tmp_path):
        context_path = tmp_path / "context"
        results_path = tmp_path / "results"
        context_path.mkdir()
        results_path.mkdir()
        input_data = {"context_path": str(context_path), "results_path": str(results_path)}
        validator = InputValidator(input_data, [])
        validator._validate_paths()
    
    def test_validate_paths_invalid_context_path(self, tmp_path):
        context_path = tmp_path / "context"
        results_path = tmp_path / "results"
        results_path.mkdir()
        input_data = {"context_path": str(context_path), "results_path": str(results_path)}
        validator = InputValidator(input_data, [])
        with pytest.raises(ValueError):
            validator._validate_paths()
    
    def test_validate_paths_invalid_results_path(self, tmp_path):
        context_path = tmp_path / "context"
        results_path = tmp_path / "results"
        context_path.mkdir()
        input_data = {"context_path": str(context_path), "results_path": str(results_path)}
        validator = InputValidator(input_data, [])
        with pytest.raises(ValueError):
            validator._validate_paths()
    