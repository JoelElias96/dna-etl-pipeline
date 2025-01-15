from etl.etl_manager import ETLManager

def main() -> None:
    try:
        data = input("Enter the input: ")       
        etl_manager = ETLManager(data)
        etl_manager.process()
        print("ETL process completed successfully.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
