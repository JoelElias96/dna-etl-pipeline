from ui import ask_input_method, run_etl_ui, run_etl_terminal


def main():
    
    input_method = ask_input_method()

    if input_method == "ui":
        run_etl_ui()
    else:
        run_etl_terminal()


if __name__ == "__main__":
    main()
