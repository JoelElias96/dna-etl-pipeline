from etl.etl_manager import ETLManager
from tests.test_files_creator import create_dir_for_test_files_1


def main() -> None:
    try:
        data = create_data()     
        etl_manager = ETLManager(data)
        etl_manager.process()
        print("ETL process completed successfully.")

    except Exception as e:
        print(f"Error: {e}")


def create_data():
    data = create_dir_for_test_files_1()
    return data


if __name__ == "__main__":
    main()
