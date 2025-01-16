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

    txt_file_path = os.path.join(context_path, f"{user_id}abcdefg_dna.txt")
    with open(txt_file_path, "w") as f:
        f.write(file_content)

    print(f"Sample TXT file created at: {txt_file_path}")


def create_dir_for_test_files_1():
    user_id = uuid.uuid4()
    context_path = f"./data/participants/{user_id}"
    result_path = f"./data/participants/{user_id}/out"
    
    # Create the context path directory
    os.makedirs(context_path, exist_ok=True)
    
    # Create the out directory inside the context path
    os.makedirs(result_path, exist_ok=True)

    create_sample_json(context_path, get_sample_json_1(context_path), user_id)
    create_sample_txt(context_path, get_sample_txt_1(), user_id)

    data = {"context_path": context_path, "results_path": result_path}
    json_input_path = f"./data/inputs/invalid/{user_id}_input.json"
    with open(json_input_path, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Sample input file created at: {json_input_path}")
    return data


def get_sample_json_1(context_path):
    return{
    "test_metadata": {
        "test_id": "GEN345",
        "test_type": "Genetic Profiling",
        "date_requested": "2024-03-01",
        "date_completed": "2024-03-05",
        "status": "Completed",
        "laboratory_info": {
            "name": "HealthGene Labs",
            "certification": "CLIA Certified"
        }
    },
    "sample_metadata": {
        "sample_id": "SAMP123",
        "sample_type": "Saliva",
        "collection_date": "2024-03-01",
        "data_file": context_path
    },
    "analysis_metadata": {
        "platform": "Illumina NextSeq",
        "methodology": "Whole Genome Sequencing",
        "coverage": "30x",
        "reference_genome": "GRCh38",
        "variants_detected": {
            "total": 4000,
            "pathogenic": 12,
            "likely_pathogenic": 6,
            "benign": 3982
        }
    },
    "individual_metadata": {
        "_individual_id": "IND456",
        "_name": "David Smith",
        "date_of_birth": "1933-05-10",
        "gender": "Male",
        "ethnicity": "Caucasian"
    },
    "treatment_metadata": {
        "treatment_plan": "Ongoing management of heart disease and blood pressure",
        "start_date": "2024-01-15",
        "current_medications": [
            {
                "name": "Amlodipine",
                "dose": "5 mg daily"
            },
        ],
        "doctor": "Dr. Jane Carter"
    },
    "environmental_factors": {
        "smoking_history": "Non-smoker",
        "exercise": "Daily walking and stretching, 20 minutes",
        "diet": "Low salt, high fiber diet",
        "sleep": "7-8 hours of sleep nightly"
    },
}







def get_sample_txt_1() -> str:
    return ("ACGAGTAGAGGAGTGCTGGCGACACACACACACACTAGGACAGGATCGGAGTACAGGAGGTAGCAGTGAGGAGTCAGTAGGCAGTGTAGCGTGAAGCA\n"
            "GTGACTAGCGTAGAGGACGAGTAGTTCAGGTAGGAGCAGTCAGGAGACGTGCGTGAAGTACGAGTAGGTCAGTGCAGAGTACGC\n"
            "TGCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGAGCGACTAAGAAAAAAAAAAAAAAAGAGTCAGTAGCGTAGGATACGTAGGAGGAGGTGACCTAGAGGACTTAGGAGGTGCGTAGGGAGTGAAGT\n"
            )