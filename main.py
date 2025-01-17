import tkinter as tk
from tkinter import filedialog
import json
from tkinter import messagebox


def process_json_file(json_path):
    """Load and process the JSON file."""
    try:
        with open(json_path, 'r') as file:
            data = json.load(file)  # Load the JSON data
            print("JSON data loaded successfully!")
            # Here you can process the JSON data as needed
            print(data)
    except FileNotFoundError:
        messagebox.showerror("ERROR", f"File not found: {json_path}")
    except json.JSONDecodeError:
        messagebox.showerror("ERROR", "Invalid JSON format.")
    except Exception as e:
        messagebox.showerror("ERROR", f"An error occurred: {e}")


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
        process_json_file(json_file)


if __name__ == "__main__":
    main()
