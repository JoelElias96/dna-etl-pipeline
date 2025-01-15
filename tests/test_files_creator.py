import json
import os


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


def create_dir_for_test_files(context_path, user_id):
    sample_json = {
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
    sample_txt = "ATCGATCGTAGCTAGCTAGCTGATCGATCGAT\nATCGGTAAATGCCTGAAAGATG"

    create_sample_json(context_path, sample_json, user_id)
    create_sample_txt(context_path, sample_txt, user_id)