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


def select_json_file():
    """Prompt the user to select a JSON file."""
    # Create a file dialog to choose a file
    file_path = filedialog.askopenfilename(
        title="Select a JSON file",
        filetypes=(("JSON Files", "*.json"), ("All Files", "*.*"))
    )
    return file_path


def main():
    # Initialize the tkinter root window (it won't be shown)
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window

    # Ask the user to select a JSON file
    json_file = select_json_file()

    if json_file:
        process_json_file(json_file)  # Process the selected JSON file
    else:
        messagebox.showinfo("No File Selected", "No file was selected. Exiting.")


if __name__ == "__main__":
    main()
