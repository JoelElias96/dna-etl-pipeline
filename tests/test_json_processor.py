
def test_remove_sensitive_data():
    from src.json_processor import _remove_sensitive_data

    # Test case 1: Simple metadata with _id key
    metadata = {"_id": 1, "name": "Alice", "email": "alice@bob.com"}
    expected = {"name": "Alice", "email": "alice@bob.com"}
    assert _remove_sensitive_data(metadata) == expected

    # Test case 2: Metadata without _id key
    metadata = {"name": "Bob", "email": "bob@alice.com"}
    expected = {"name": "Bob", "email": "bob@alice.com"}
    assert _remove_sensitive_data(metadata) == expected

    # Test case 3: Metadata with multiple sensitive keys
    metadata = {"_id": 2, "_password": "secret", "name": "Charlie"}
    expected = {"name": "Charlie"}
    assert _remove_sensitive_data(metadata) == expected

    # Test case 4: Metadata with nested sensitive data
    metadata = {"_id": 3, "name": "Dave", "details": {"_token": "abc123", "age": 30}}
    expected = {"name": "Dave", "details": {"age": 30}}
    assert _remove_sensitive_data(metadata) == expected

    # Test case 5: Metadata with no keys at all
    metadata = {}
    expected = {}
    assert _remove_sensitive_data(metadata) == expected

    # Test case 6: Metadata with only sensitive keys
    metadata = {"_id": 4, "_token": "def456"}
    expected = {}
    assert _remove_sensitive_data(metadata) == expected

    # Test case 7: Metadata with sensitive keys and empty nested objects
    metadata = {"_id": 5, "info": {"_token": "ghi789"}}
    expected = {"info": {}}
    assert _remove_sensitive_data(metadata) == expected

    # Test case 8: Metadata with list containing sensitive keys
    metadata = {"_id": 6, "users": [{"_id": 1, "name": "Eve"}, {"_id": 2, "name": "Frank"}]}
    expected = {"users": [{"name": "Eve"}, {"name": "Frank"}]}
    assert _remove_sensitive_data(metadata) == expected

     # Test case 9: Complex metadata with nested and mixed sensitive and non-sensitive data
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

def test_validate_lengths():
    from src.json_processor import _validate_lengths_of_strs

    # Test case 1: Valid data with no string exceeding 64 characters
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

    # Test case 2: String exceeding 64 characters in a flat dictionary
    data = {
        "name": "A" * 65,
        "email": "alice@bob.com"
    }
    try:
        _validate_lengths_of_strs(data)
        assert False, "Test case 2 failed!"
    except ValueError as e:
        assert str(e) == "The string 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' exceeds 64 characters.", "Test case 2 failed!"

    # Test case 3: String exceeding 64 characters in a nested dictionary
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

    # Test case 4: String exceeding 64 characters in a list
    data = ["C" * 65, "Valid string"]
    try:
        _validate_lengths_of_strs(data)
        assert False, "Test case 4 failed!"
    except ValueError as e:
        assert str(e) == "The string 'CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC' exceeds 64 characters.", "Test case 4 failed!"

    # Test case 5: Mixed valid and invalid strings in a nested structure
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

    # Test case 6: Empty dictionary
    data = {}
    try:
        _validate_lengths_of_strs(data)
    except ValueError:
        assert False, "Test case 6 failed!"

    # Test case 7: Empty list
    data = []
    try:
        _validate_lengths_of_strs(data)
    except ValueError:
        assert False, "Test case 7 failed!"

    # Test case 8: Non-string values
    data = {
        "count": 123,
        "active": True,
        "items": [1, 2, 3]
    }
    try:
        _validate_lengths_of_strs(data)
    except ValueError:
        assert False, "Test case 8 failed!"


