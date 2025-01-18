import tkinter as tk
from tkinter import filedialog, messagebox
from pipeline.etl_manager import ETLManager


class ETLApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ETL Process")
        
        # Instructions label
        self.instructions = tk.Label(self.root, text="Welcome to the ETL Process Application", font=("Arial", 12))
        self.instructions.pack(pady=10)

        # Start button
        self.start_button = tk.Button(self.root, text="Start ETL", command=self.on_start_etl)
        self.start_button.pack(pady=20)

        # Exit button
        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.quit)
        self.exit_button.pack(pady=10)

    def on_start_etl(self):
        """Handler for start ETL process button."""
        json_file = self.select_json_file()
        if json_file:
            self.run_etl_process(json_file)

    def select_json_file(self):
        """Prompt the user to select a JSON file."""
        file_path = filedialog.askopenfilename(
            title="Select a JSON file",
            filetypes=(("JSON Files", "*.json"), ("All Files", "*.*"))
        )
        return file_path

    def create_processing_window(self):
        """
        Creates and displays a processing window with a "Processing..." message.
        """
        # Create a processing window
        processing_window = tk.Toplevel(self.root)
        processing_window.title("Processing")
        processing_window.geometry("200x100")
        processing_window.resizable(False, False)
        
        # Disable interaction with the main window
        processing_window.transient(self.root)
        processing_window.grab_set()

        # Add a label with the text "Processing..."
        label = tk.Label(processing_window, text="Processing...", font=("Arial", 10))
        label.pack(pady=20)

        processing_window.update_idletasks()  # Ensure the window and its contents are fully rendered

        return processing_window

    def run_etl_process(self, file_path):
        """
        Runs the ETL process and closes the processing window upon completion.
        """
        processing_window = self.create_processing_window()
        
        try:
            etl_manager = ETLManager()
            etl_manager.process(file_path)  # Run the ETL process
            processing_window.destroy()
            messagebox.showinfo("Success", f"ETL process completed successfully for {file_path}")
        except Exception as e:
            processing_window.destroy()
            messagebox.showerror("Error", f"ETL process failed: {e}")


def run():
    """Run the ETL application."""
    root = tk.Tk()
    ETLApp(root)
    root.mainloop()
