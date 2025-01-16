from pipeline.etl_manager import ETLManager
from tkinter import messagebox


def main() -> None:
    try:
        data = {
                "context_path": "./data/participants/12ba71a0-30f4-464e-ba1b-9a31ea7d35fc",
                "results_path": "./data/participants/12ba71a0-30f4-464e-ba1b-9a31ea7d35fc/out"
                }
        etl_manager = ETLManager(data)
        etl_manager.process()
        print("ETL process completed successfully.")

    except Exception as e:
        messagebox.showerror("ERROR", e)


if __name__ == "__main__":
    main()
