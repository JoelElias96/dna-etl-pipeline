import tkinter as tk
from tkinter import filedialog, messagebox
from pipeline.etl_manager import ETLManager


class ETLApp:
    """
    A GUI application for managing the ETL (Extract, Transform, Load) process.

    This class provides a graphical interface for users to select input JSON files
    and execute the ETL process. The application includes a main window with options
    to start the ETL process and exit the application.

    Attributes:
        root (tk.Tk): The main Tkinter window for the application.
        instructions (tk.Label): A label displaying instructions to the user.
        start_button (tk.Button): A button to start the ETL process.
        exit_button (tk.Button): A button to exit the application.

    Methods:
        run() -> None:
            Runs the ETL application.
    """

    def __init__(self, root: tk.Tk) -> None:
        """
        Initializes the ETLApp class and sets up the main application window.

        :param root: The main Tkinter window for the application.
        :type root: tk.Tk
        """
        self.root = root
        self.root.title("ETL Process")

        # Instructions label
        self.instructions = tk.Label(
            self.root, text="Welcome to the ETL Process Application", font=("Arial", 12)
        )
        self.instructions.pack(pady=10)

        # Start button
        self.start_button = tk.Button(self.root, text="Start ETL", command=self._on_start_etl)
        self.start_button.pack(pady=20)

        # Exit button
        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.quit)
        self.exit_button.pack(pady=10)

    def _on_start_etl(self) -> None:
        """
        Handler for the "Start ETL" button. Prompts the user to select a JSON file
        and starts the ETL process if a file is selected.

        :return: None
        """
        json_file = self._select_json_file()
        if json_file:
            self._run_etl_process(json_file)

    def _select_json_file(self) -> str:
        """
        Opens a file dialog to allow the user to select a JSON file.

        :return: The path to the selected JSON file.
        :rtype: str
        """
        file_path = filedialog.askopenfilename(
            title="Select a JSON file",
            filetypes=(("JSON Files", "*.json"), ("All Files", "*.*"))
        )
        return file_path

    def _create_processing_window(self) -> tk.Toplevel:
        """
        Creates and displays a "Processing..." window while the ETL process is running.

        The processing window prevents interaction with the main application window
        and shows a simple "Processing..." message.

        :return: The processing window instance.
        :rtype: tk.Toplevel
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

    def _run_etl_process(self, file_path: str) -> None:
        """
        Executes the ETL process using the provided JSON file and closes the
        processing window upon completion.

        :param file_path: The path to the input JSON file for the ETL process.
        :type file_path: str

        :raises Exception: If an error occurs during the ETL process.
        :return: None
        """
        processing_window = self._create_processing_window()

        try:
            etl_manager = ETLManager()
            etl_manager.process(file_path)  # Run the ETL process
            processing_window.destroy()
            messagebox.showinfo("Success", f"ETL process completed successfully for {file_path}")
        except Exception as e:
            processing_window.destroy()
            messagebox.showerror("Error", f"ETL process failed: {e}")


def run() -> None:
    """
    Runs the ETL application by creating the main Tkinter window
    and initializing the ETLApp class.

    :return: None
    """
    root = tk.Tk()
    ETLApp(root)
    root.mainloop()
