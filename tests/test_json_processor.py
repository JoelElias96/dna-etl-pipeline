import pytest
import json
from datetime import datetime
from src.json_processor import _remove_sensitive_data, _validate_lengths_of_strs, _validate_dates_in_file, _validate_age,process_json_file

class TestRemoveSensitiveData:
    

    def test_simple_metadata_with_id_key(self):
        metadata = {"_id": 1, "name": "Alice", "email": "alice@bob.com"}
        expected = {"name": "Alice", "email": "alice@bob.com"}
        assert _remove_sensitive_data(metadata) == expected

    def test_metadata_without_id_key(self):
        metadata = {"name": "Bob", "email": "bob@alice.com"}
        expected = {"name": "Bob", "email": "bob@alice.com"}
        assert _remove_sensitive_data(metadata) == expected

    def test_metadata_with_multiple_sensitive_keys(self):
        metadata = {"_id": 2, "_password": "secret", "name": "Charlie"}
        expected = {"name": "Charlie"}
        assert _remove_sensitive_data(metadata) == expected

    def test_metadata_with_nested_sensitive_data(self):
        metadata = {"_id": 3, "name": "Dave", "details": {"_token": "abc123", "age": 30}}
        expected = {"name": "Dave", "details": {"age": 30}}
        assert _remove_sensitive_data(metadata) == expected

    def test_metadata_with_no_keys(self):
        metadata = {}
        expected = {}
        assert _remove_sensitive_data(metadata) == expected

    def test_metadata_with_only_sensitive_keys(self):
        metadata = {"_id": 4, "_token": "def456"}
        expected = {}
        assert _remove_sensitive_data(metadata) == expected

    def test_metadata_with_sensitive_keys_and_empty_nested_objects(self):
        metadata = {"_id": 5, "info": {"_token": "ghi789"}}
        expected = {"info": {}}
        assert _remove_sensitive_data(metadata) == expected

    def test_metadata_with_list_containing_sensitive_keys(self):
        metadata = {"_id": 6, "users": [{"_id": 1, "name": "Eve"}, {"_id": 2, "name": "Frank"}]}
        expected = {"users": [{"name": "Eve"}, {"name": "Frank"}]}
        assert _remove_sensitive_data(metadata) == expected

    def test_complex_metadata_with_nested_and_mixed_sensitive_and_non_sensitive_data(self):
        metadata = {
            "test_metadata": {
                "test_id": "DNA123456",
                "test_type": "Genetic Analysis",
                "date_requested": "2024-12-01",
                "date_completed": "2024-12-10",
                "status": "Completed",
                "laboratory_info": {
                    "name": "Genomics Lab Inc.",
                    "certification": "CLIA Certified"
                }
            },
            "sample_metadata": {
                "sample_id": "SAMP987654",
                "sample_type": "Saliva",
                "collection_date": "2024-12-01",
                "data_file": "<PATH_TO_TXT_FILE>"
            },
            "analysis_metadata": {
                "platform": "Illumina NovaSeq 6000",
                "methodology": "Whole Genome Sequencing",
                "coverage": "30x",
                "reference_genome": "GRCh38",
                "variants_detected": {
                    "total": 5000,
                    "pathogenic": 15,
                    "likely_pathogenic": 8,
                    "benign": 4977
                }
            },
            "individual_metadata": {
                "_individual_id": "IND123456",
                "_name": "John Smith",
                "date_of_birth": "1985-05-15",
                "gender": "Male",
                "ethnicity": "Caucasian",
                "family_history": {
                    "diseases": [
                        {
                            "name": "Breast Cancer",
                            "relation": "Mother",
                            "age_at_diagnosis": 50
                        },
                        {
                            "name": "Type 2 Diabetes",
                            "relation": "Father",
                            "age_at_diagnosis": 55
                        }
                    ]
                }
            }
        }
        expected = {
            "test_metadata": {
                "test_id": "DNA123456",
                "test_type": "Genetic Analysis",
                "date_requested": "2024-12-01",
                "date_completed": "2024-12-10",
                "status": "Completed",
                "laboratory_info": {
                    "name": "Genomics Lab Inc.",
                    "certification": "CLIA Certified"
                }
            },
            "sample_metadata": {
                "sample_id": "SAMP987654",
                "sample_type": "Saliva",
                "collection_date": "2024-12-01",
                "data_file": "<PATH_TO_TXT_FILE>"
            },
            "analysis_metadata": {
                "platform": "Illumina NovaSeq 6000",
                "methodology": "Whole Genome Sequencing",
                "coverage": "30x",
                "reference_genome": "GRCh38",
                "variants_detected": {
                    "total": 5000,
                    "pathogenic": 15,
                    "likely_pathogenic": 8,
                    "benign": 4977
                }
            },
            "individual_metadata": {
                "date_of_birth": "1985-05-15",
                "gender": "Male",
                "ethnicity": "Caucasian",
                "family_history": {
                    "diseases": [
                        {
                            "name": "Breast Cancer",
                            "relation": "Mother",
                            "age_at_diagnosis": 50
                        },
                        {
                            "name": "Type 2 Diabetes",
                            "relation": "Father",
                            "age_at_diagnosis": 55
                        }
                    ]
                }
            }
        }
        assert _remove_sensitive_data(metadata) == expected

class TestValidateLengths:

    def test_valid_data_no_string_exceeding_64_characters(self):
        data = {
            "name": "Alice",
            "email": "alice@bob.com",
            "details": {
                "address": "123 Main Street",
                "phone": "123-456-7890"
            }
        }
        try:
            _validate_lengths_of_strs(data)
        except ValueError:
            assert False, "Test case 1 failed!"

    def test_string_exceeding_64_characters_flat_dictionary(self):
        data = {
            "name": "A" * 65,
            "email": "alice@bob.com"
        }
        try:
            _validate_lengths_of_strs(data)
            assert False, "Test case 2 failed!"
        except ValueError as e:
            assert str(e) == "The string 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' exceeds 64 characters.", "Test case 2 failed!"

    def test_string_exceeding_64_characters_nested_dictionary(self):
        data = {
            "details": {
                "bio": "B" * 65
            }
        }
        try:
            _validate_lengths_of_strs(data)
            assert False, "Test case 3 failed!"
        except ValueError as e:
            assert str(e) == "The string 'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB' exceeds 64 characters.", "Test case 3 failed!"

    def test_string_exceeding_64_characters_list(self):
        data = ["C" * 65, "Valid string"]
        try:
            _validate_lengths_of_strs(data)
            assert False, "Test case 4 failed!"
        except ValueError as e:
            assert str(e) == "The string 'CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC' exceeds 64 characters.", "Test case 4 failed!"

    def test_mixed_valid_invalid_strings_nested_structure(self):
        data = {
            "users": [
                {"name": "Valid name"},
                {"bio": "D" * 65}
            ]
        }
        try:
            _validate_lengths_of_strs(data)
            assert False, "Test case 5 failed!"
        except ValueError as e:
            assert str(e) == "The string 'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD' exceeds 64 characters.", "Test case 5 failed!"

    def test_empty_dictionary(self):
        data = {}
        try:
            _validate_lengths_of_strs(data)
        except ValueError:
            assert False, "Test case 6 failed!"

    def test_empty_list(self):
        data = []
        try:
            _validate_lengths_of_strs(data)
        except ValueError:
            assert False, "Test case 7 failed!"

    def test_non_string_values(self):
        data = {
            "count": 123,
            "active": True,
            "items": [1, 2, 3]
        }
        try:
            _validate_lengths_of_strs(data)
        except ValueError:
            assert False, "Test case 8 failed!"

class TestValidateDates:
    def test_valid_date_format(self):
        data = {
            "date": "2024-12-31",
            "details": {
                "start": "2014-01-01",
                "end": "2024-12-31"
            }
        }
        try:
            _validate_dates_in_file(data)
        except ValueError:
            assert False, "Test case 1 failed!"

    def test_past_date(self):
        data = {
            "date": "2010-01-01",
            "details": {
                "start": "2014-01-01",
                "end": "2024-12-31"
            }
        }
        with pytest.raises(ValueError, match="Date '2010-01-01' is out of the allowed range."):
            _validate_dates_in_file(data)

    def test_date_out_of_range(self):
        data = {
            "date": "2025-01-01",
            "details": {
                "start_date": "2014-01-01",
                "end_date": "2024-12-31"
            }
        }
        with pytest.raises(ValueError, match="Date '2025-01-01' is out of the allowed range."):
            _validate_dates_in_file(data)

    def test_valid_future_date_within_range(self):
        data = {
            "date": "2024-12-31",
            "details": {
                "start_date": "2014-01-01",
                "end_date": "2022-01-01",
                "milestones": [
                    {"event": "Project Start", "date": "2014-01-01"},
                    {"event": "Midpoint Review", "date": "2019-06-01"},
                    {"event": "Project End", "date": "2026-01-01"}
                ],
                "notes": "This project spans over a decade with multiple key milestones."
            },
            "summary": "A long-term project with significant milestones and a detailed timeline."
        }
        with pytest.raises(ValueError, match="Date '2026-01-01' is out of the allowed range."):
            _validate_dates_in_file(data)

    def test_valid_future_date_within_range_2(self):
        data = {
            "date": "2024-12-31",
            "details": {
                "start_date": "2014-01-01",
                "end_date": "2025-12-31",
                "milestones": [
                    {"event": "Project Start", "date": "2014-01-01"},
                    {"event": "Midpoint Review", "date": "2019-06-01"},
                    {"event": "Project End", "date": "2025-12-31"}
                ],
                "notes": "This project spans over a decade with multiple key milestones."
            },
            "summary": "A long-term project with significant milestones and a detailed timeline."
        }
        with pytest.raises(ValueError, match="Date '2025-12-31' is out of the allowed range."):
            _validate_dates_in_file(data)

    def test_invalid_range_date_in_list(self):
        data = {
            "date": "2024-12-31",
            "details": [
                {"event": "Start", "date": "2014-01-01"},
                {"event": "End", "date": "2025-12-31"}
            ]
        }
        with pytest.raises(ValueError, match="Date '2025-12-31' is out of the allowed range."):
            _validate_dates_in_file(data)

    def test_valid_data_in_complex_nested_structure(self):
        data = {
            "test_metadata": {
                "test_id": "DNA123456",
                "test_type": "Genetic Analysis",
                "date_requested": "2024-12-01",
                "date_completed": "2024-12-10",
                "status": "Completed",
                "laboratory_info": {
                    "name": "Genomics Lab Inc.",
                    "certification": "CLIA Certified"
                }
            },
            "sample_metadata": {
                "sample_id": "SAMP987654",
                "sample_type": "Saliva",
                "collection_date": "2024-12-01",
                "data_file": "<PATH_TO_TXT_FILE>"
            },
            "analysis_metadata": {
                "platform": "Illumina NovaSeq 6000",
                "methodology": "Whole Genome Sequencing",
                "coverage": "30x",
                "reference_genome": "GRCh38",
                "variants_detected": {
                    "total": 5000,
                    "pathogenic": 15,
                    "likely_pathogenic": 8,
                    "benign": 4977
                }
            },
            "individual_metadata": {
                "_individual_id": "IND123456",
                "_name": "John Smith",
                "date_of_birth": "1984-05-15",
                "gender": "Male",
                "ethnicity": "Caucasian",
                "family_history": {
                    "diseases": [
                        {
                            "name": "Breast Cancer",
                            "relation": "Mother",
                            "age_at_diagnosis": 50
                        },
                        {
                            "name": "Type 2 Diabetes",
                            "relation": "Father",
                            "age_at_diagnosis": 55
                        }
                    ]
                }
            }
        }
        try:
            _validate_dates_in_file(data)
        except ValueError:
            assert False, "Test case 7 failed!"

class TestValidateAge:

    def test_valid_age_exactly_40_years_old(self):
        dob = (datetime.now().replace(year=datetime.now().year - 40)).strftime('%Y-%m-%d')
        _validate_age(dob)  # Should not raise any exception

    def test_valid_age_over_40_years_old(self):
        dob = (datetime.now().replace(year=datetime.now().year - 50)).strftime('%Y-%m-%d')
        _validate_age(dob)  # Should not raise any exception

    def test_invalid_age_under_40_years_old(self):
        dob = (datetime.now().replace(year=datetime.now().year - 30)).strftime('%Y-%m-%d')
        with pytest.raises(ValueError, match="Participant must be at least 40 years old."):
            _validate_age(dob)

    def test_invalid_date_format(self):
        dob = "15-05-1985"  # Incorrect format
        with pytest.raises(ValueError, match="Invalid date of birth format."):
            _validate_age(dob)

    def test_future_date(self):
        dob = (datetime.now().replace(year=datetime.now().year + 1)).strftime('%Y-%m-%d')
        with pytest.raises(ValueError, match="Participant must be at least 40 years old."):
            _validate_age(dob)

    def test_empty_date_of_birth(self):
        dob = ""
        with pytest.raises(ValueError, match="Invalid date of birth format."):
            _validate_age(dob)

class TestProcessJsonFile:

    def test_valid_json_with_all_correct_data(self, tmp_path):
        valid_data = {
            "individual_metadata": {
                "date_of_birth": "1980-01-01"
            },
            "other_data": "Valid information"
        }
        test_file = tmp_path / "test.json"
        test_file.write_text(json.dumps(valid_data))
        result = process_json_file(str(test_file))
        assert result == valid_data, "Test case 1 failed!"

    def test_invalid_json_format(self, tmp_path):
        invalid_json_content = "{invalid_json: true}"
        test_file = tmp_path / "test.json"
        test_file.write_text(invalid_json_content)
        with pytest.raises(json.JSONDecodeError, match="Invalid JSON file format."):
            process_json_file(str(test_file))

    def test_file_not_found(self):
        with pytest.raises(FileNotFoundError, match="File not found: test.json"):
            process_json_file("test.json")

    def test_sensitive_data_removed(self, tmp_path):
        data_with_sensitive = {
            "_private_key": "should_be_removed",
            "individual_metadata": {
                "date_of_birth": "1980-01-01"
            }
        }
        expected_data = {
            "individual_metadata": {
                "date_of_birth": "1980-01-01"
            }
        }
        test_file = tmp_path / "test.json"
        test_file.write_text(json.dumps(data_with_sensitive))
        result = process_json_file(str(test_file))
        assert result == expected_data, "Test case 4 failed!"

    def test_string_exceeding_length_limit(self, tmp_path):
        invalid_data = {
            "too_long": "a" * 65,
            "individual_metadata": {
                "date_of_birth": "1980-01-01"
            }
        }
        test_file = tmp_path / "test.json"
        test_file.write_text(json.dumps(invalid_data))
        with pytest.raises(ValueError, match="The string 'a{64,}' exceeds 64 characters."):
            process_json_file(str(test_file))

    def test_participant_under_40_years_old(self, tmp_path):
        data_under_40 = {
            "individual_metadata": {
                "date_of_birth": "2010-01-01"
            }
        }
        test_file = tmp_path / "test.json"
        test_file.write_text(json.dumps(data_under_40))
        with pytest.raises(ValueError, match="Participant must be at least 40 years old."):
            process_json_file(str(test_file))

    def test_complex_metadata_with_nested_sensitive_data(self, tmp_path):
        complex_data = {
            "test_metadata": {
                "test_id": "DNA123456",
                "test_type": "Genetic Analysis",
                "date_requested": "2024-12-01",
                "date_completed": "2024-12-10",
                "status": "Completed",
                "laboratory_info": {
                    "name": "Genomics Lab Inc.",
                    "certification": "CLIA Certified"
                }
            },
            "sample_metadata": {
                "sample_id": "SAMP987654",
                "sample_type": "Saliva",
                "collection_date": "2024-12-01",
                "data_file": "<PATH_TO_TXT_FILE>"
            },
            "analysis_metadata": {
                "platform": "Illumina NovaSeq 6000",
                "methodology": "Whole Genome Sequencing",
                "coverage": "30x",
                "reference_genome": "GRCh38",
                "variants_detected": {
                    "total": 5000,
                    "pathogenic": 15,
                    "likely_pathogenic": 8,
                    "benign": 4977
                }
            },
            "individual_metadata": {
                "_individual_id": "IND123456",
                "_name": "John Smith",
                "date_of_birth": "1984-05-15",
                "gender": "Male",
                "ethnicity": "Caucasian",
                "family_history": {
                    "diseases": [
                        {
                            "name": "Breast Cancer",
                            "relation": "Mother",
                            "age_at_diagnosis": 50
                        },
                        {
                            "name": "Type 2 Diabetes",
                            "relation": "Father",
                            "age_at_diagnosis": 55
                        }
                    ]
                }
            }
        }
        expected_complex_data = {
            "test_metadata": {
                "test_id": "DNA123456",
                "test_type": "Genetic Analysis",
                "date_requested": "2024-12-01",
                "date_completed": "2024-12-10",
                "status": "Completed",
                "laboratory_info": {
                    "name": "Genomics Lab Inc.",
                    "certification": "CLIA Certified"
                }
            },
            "sample_metadata": {
                "sample_id": "SAMP987654",
                "sample_type": "Saliva",
                "collection_date": "2024-12-01",
                "data_file": "<PATH_TO_TXT_FILE>"
            },
            "analysis_metadata": {
                "platform": "Illumina NovaSeq 6000",
                "methodology": "Whole Genome Sequencing",
                "coverage": "30x",
                "reference_genome": "GRCh38",
                "variants_detected": {
                    "total": 5000,
                    "pathogenic": 15,
                    "likely_pathogenic": 8,
                    "benign": 4977
                }
            },
            "individual_metadata": {
                "date_of_birth": "1984-05-15",
                "gender": "Male",
                "ethnicity": "Caucasian",
                "family_history": {
                    "diseases": [
                        {
                            "name": "Breast Cancer",
                            "relation": "Mother",
                            "age_at_diagnosis": 50
                        },
                        {
                            "name": "Type 2 Diabetes",
                            "relation": "Father",
                            "age_at_diagnosis": 55
                        }
                    ]
                }
            }
        }
        test_file = tmp_path / "test.json"
        test_file.write_text(json.dumps(complex_data))
        result = process_json_file(str(test_file))
        assert result == expected_complex_data, "Test case 7 failed!"

    def test_invalid_date_format(self, tmp_path):
        invalid_date_data = {
            "individual_metadata": {
            "date_of_birth": "1980-01-01",
            "gender": "Female",
            "ethnicity": "Asian",
            "family_history": {
                "diseases": [
                {
                    "name": "Hypertension",
                    "relation": "Grandfather",
                    "age_at_diagnosis": 60
                },
                {
                    "name": "Asthma",
                    "relation": "Mother",
                    "age_at_diagnosis": 35
                }
                ]
            }
            },
            "test_metadata": {
            "test_id": "DNA654321",
            "test_type": "Exome Sequencing",
            "date_requested": "2023-11-01",
            "date_completed": "2027-11-10",
            "status": "In Progress",
            "laboratory_info": {
                "name": "Genomics Lab Inc.",
                "certification": "ISO Certified"
            }
            },
            "sample_metadata": {
            "sample_id": "SAMP123456",
            "sample_type": "Blood",
            "collection_date": "2023-11-01",
            "data_file": "<PATH_TO_TXT_FILE>"
            }
        }
        test_file = tmp_path / "test.json"
        test_file.write_text(json.dumps(invalid_date_data))
        with pytest.raises(ValueError, match="Date '2027-11-10' is out of the allowed range."):
            process_json_file(str(test_file))
