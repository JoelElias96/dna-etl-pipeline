from pipeline.etl_manager import ETLManager
from tests.test_files_creator import create_dir_for_test_files_1
from tkinter import messagebox


def main() -> None:
    try:
        data = create_dir_for_test_files_1()
        etl_manager = ETLManager(data)
        etl_manager.process()
        print("ETL process completed successfully.")

    except Exception as e:
        messagebox.showerror("ERROR", e)


if __name__ == "__main__":
    main()
