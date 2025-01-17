from ui import process_json_file, select_json_file, ask_input_method
import tkinter as tk


def main():
    # Ask the user whether to use the UI or terminal for input
    input_method = ask_input_method()

    if input_method == "ui":
        # Initialize the tkinter root window (it won't be shown)
        root = tk.Tk()
        root.withdraw()  # Hide the main tkinter window

        # Ask the user to select a JSON file
        json_file = select_json_file()

        if json_file:
            process_json_file(json_file)  # Process the selected JSON file

    else:
        # Terminal input method
        json_file = input("Please enter the full path of the JSON file: ")


if __name__ == "__main__":
    main()
