import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


def process_json_file(file_path):
    pass


def select_json_file():
    """Prompt the user to select a JSON file."""
    # Create a file dialog to choose a file
    file_path = filedialog.askopenfilename(
        title="Select a JSON file",
        filetypes=(("JSON Files", "*.json"), ("All Files", "*.*"))
    )
    return file_path


def ask_input_method():
    """Prompt the user to choose between UI or terminal input."""
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window

    answer = messagebox.askquestion(
        "Choose Input Method",
        "Do you want to select the file via the UI?"
    )

    if answer == "yes":
        return "ui"
    else:
        return "terminal"


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
            messagebox.showinfo("No File Selected", "No file was selected. Exiting.")
    else:
        # Terminal input method
        json_file = input("Please enter the full path of the JSON file: ")


if __name__ == "__main__":
    main()
