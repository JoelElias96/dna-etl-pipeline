import os
import json
from etl.etl_manager import ETLManager

def create_sample_json(context_path):
    """
    Creates a valid JSON file in the context path.
    """
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
            "collection_date": "2024-12-01",
            
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

    json_file_path = os.path.join(context_path, "f3324a99-8a63-4ada-9d1d-562f84c7636d_dna.json")
    with open(json_file_path, "w") as f:
        json.dump(sample_json, f, indent=4)
    print(f"Sample JSON file created at: {json_file_path}")

def create_sample_txt(context_path):
    """
    Creates a valid TXT file in the context path.
    """
    sample_txt = "ATCGATCGTAGCTAGCTAGCTGATCGATCGAT\nATCGGTAAATGCCTGAAAGATG"

    
    txt_file_path = os.path.join(context_path, "f3324a99-8a63-4ada-9d1d-562f84c7636d_dna.txt")
    with open(txt_file_path, "w") as f:
        f.write(sample_txt)

    print(f"Sample TXT file created at: {txt_file_path}")
    
    
def main():
    try:
        context_path = "tests/test_files/f3324a99-8a63-4ada-9d1d-562f84c7636d"
        results_path = "tests/test_files/f3324a99-8a63-4ada-9d1d-562f84c7636d/out"

        # Ensure the output directory exists
        os.makedirs(results_path, exist_ok=True)

        # Create the sample JSON file
        create_sample_json(context_path)

        # Create the sample TXT file
        create_sample_txt(context_path)
        
        # Initialize and run the ETLManager
        data = {
            "context_path": context_path,
            "results_path": results_path
        }
        etl_manager = ETLManager(data)
        etl_manager.process()

        print("ETL process completed successfully.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
