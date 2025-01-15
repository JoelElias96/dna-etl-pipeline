from etl.etl_manager import ETLManager
from tests.test_files_creator import create_dir_for_test_files

def main() -> None:
    try:
        data = create_data()     
        etl_manager = ETLManager(data)
        etl_manager.process()
        print("ETL process completed successfully.")

    except Exception as e:
        print(f"Error: {e}")

def create_data():
    context_path = "tests/test_files"
    user_id = "f3324a99-8a63-4ada-9d1d-562f84c7636c"
    data=create_dir_for_test_files(context_path, user_id)
    return data


if __name__ == "__main__":
    main()
