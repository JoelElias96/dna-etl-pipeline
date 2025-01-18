import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
from pipeline.etl_manager import ETLManager


def process_json_file(file_path: str):
    """
    Processes the selected JSON file through the ETL pipeline.
    """
    etl_manager = ETLManager()
    try:
        # Call ETL manager to process the selected file
        etl_manager.process(file_path)
        messagebox.showinfo("Success", f"ETL process completed successfully for {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"ETL process failed: {e}")


def select_json_file():
    """Prompt the user to select a JSON file."""
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


def run_etl_ui():
    """Function to execute the ETL process with a graphical user interface."""
    root = tk.Tk()
    root.title("ETL Process")

    def on_start_etl():
        """Handler for start ETL process button."""
        json_file = select_json_file()
        if json_file:
            process_json_file(json_file)

    # Instructions label
    instructions = tk.Label(root, text="Click 'Start ETL' and a json file with valid input.")
    instructions.pack(pady=10)

    # Start button
    start_button = tk.Button(root, text="Start ETL", command=on_start_etl)
    start_button.pack(pady=20)

    # Exit button
    exit_button = tk.Button(root, text="Exit", command=root.quit)
    exit_button.pack(pady=10)

    # Run the UI main loop
    root.mainloop()


def run_etl_terminal():
    """Function to execute the ETL process in the terminal."""
    json_file = input("Please enter the full path of the JSON file: ")
    if json_file:
        process_json_file(json_file)

