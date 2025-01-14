import pytest
from etl.file_validation import InputValidator

class TestPathValidation:

    def test_valid_paths(self, tmp_path):
        input_args = {
            "context_path": str(tmp_path),  # Convert tmp_path to string for compatibility
            "results_path": str(tmp_path)
        }
        # Assuming validate_input doesn't return a value for valid inputs
        InputValidator.validate(input_args)

    def test_invalid_paths(self):
        input_args = {
            "context_path": "tests/data/input.json",
            "results_path": "tests/data/input.json"
        }
        with pytest.raises(ValueError):
            InputValidator.validate(input_args)

    def test_one_valid_one_invalid_paths1(self, tmp_path):
        input_args = {
            "context_path": str(tmp_path),
            "results_path": "tests/data/input.json"
        }
        with pytest.raises(ValueError):
            InputValidator.validate(input_args)

    def test_one_valid_one_invalid_paths2(self, tmp_path):
        input_args = {
            "context_path": "tests/data/input.json",
            "results_path": str(tmp_path)
        }
        with pytest.raises(ValueError):
            InputValidator.validate(input_args)
