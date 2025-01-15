import json
import os
import uuid


def create_sample_json(context_path, file_content, user_id):
    """
    Creates a valid JSON file in the context path.
    """

    json_file_path = os.path.join(context_path, f"{user_id}_dna.json")
    with open(json_file_path, "w") as f:
        json.dump(file_content, f, indent=4)
    print(f"Sample JSON file created at: {json_file_path}")


def create_sample_txt(context_path, file_content, user_id):
    """
    Creates a valid TXT file in the context path.
    """

    txt_file_path = os.path.join(context_path, f"{user_id}_dna.txt")
    with open(txt_file_path, "w") as f:
        f.write(file_content)

    print(f"Sample TXT file created at: {txt_file_path}")


def create_dir_for_test_files_1():
    user_id = str(uuid.uuid4())  # Ensure UUID is converted to string
    context_path = f"tests/test_files/{user_id}"
    result_path = f"tests/test_files/{user_id}/out"
    
    # Create the context path directory
    os.makedirs(context_path, exist_ok=True)
    
    # Create the out directory inside the context path
    os.makedirs(result_path, exist_ok=True)

    create_sample_json(context_path, get_sample_json_1(), user_id)
    create_sample_txt(context_path, get_sample_txt_1(), user_id)
    
    return {"context_path": context_path, "results_path": result_path}


def get_sample_json_1() -> dict:
    return {
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
            "collection_date": "2024-12-01"
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
            "individual_id": "IND123456",
            "name": "John Smith",
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


def get_sample_txt_1() -> str:
    return "ATCGATCGTAGCTAGCTAGCTGATCGATCGAT\nATCGGTAAATGCCTGAAAGATG"
