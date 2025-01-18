import argparse
import os
from pipeline.etl_manager import ETLManager


class ETLAppCli:
    """
    A Command-Line Interface (CLI) application for managing the ETL (Extract, Transform, Load) process.

    This class provides functionality to execute the ETL pipeline for either a single JSON file
    or all JSON files in a directory. Users can provide the input path through command-line arguments.

    Attributes:
        parser (argparse.ArgumentParser): Argument parser for handling CLI arguments.

    Methods:
        run() -> None:
            Parses the CLI arguments and executes the appropriate ETL process based on the input.
        _run_etl(file_path: str) -> None:
            Executes the ETL process for a single JSON file.
        _run_etl_for_directory(directory_path: str) -> None:
            Executes the ETL process for all JSON files in a specified directory.
    """

    def __init__(self) -> None:
        """
        Initializes the ETLAppCli class by setting up the argument parser.
        """
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """
        Creates and configures the argument parser for the CLI application.

        :return: An instance of argparse.ArgumentParser.
        :rtype: argparse.ArgumentParser
        """
        parser = argparse.ArgumentParser(description="ETL CLI for processing JSON files.")
        parser.add_argument(
            "-i", "--input",
            type=str,
            required=True,
            help="Path to the input JSON file or a folder containing multiple JSON files."
        )
        return parser

    def run(self) -> None:
        """
        Parses the CLI arguments and executes the ETL process for either a single file or multiple files.

        :return: None
        """
        args = self.parser.parse_args()
        input_path = args.input

        if os.path.isfile(input_path):
            # Run ETL for a single file
            self._run_etl(input_path)
        elif os.path.isdir(input_path):
            # Run ETL for all JSON files in the directory
            self._run_etl_for_directory(input_path)
        else:
            print(f"Error: {input_path} is neither a valid file nor a directory.")

    def _run_etl_for_directory(self, directory_path: str) -> None:
        """
        Executes the ETL process for all JSON files in the specified directory.

        :param directory_path: The path to the directory containing JSON files.
        :type directory_path: str
        :return: None
        """
        json_files = [f for f in os.listdir(directory_path) if f.endswith(".json")]
        if not json_files:
            print(f"No JSON files found in the folder: {directory_path}")
            return

        for json_file in json_files:
            file_path = os.path.join(directory_path, json_file)
            print(f"Running ETL for file: {file_path}...")
            self._run_etl(file_path)

    def _run_etl(self, file_path: str) -> None:
        """
        Executes the ETL process for the given JSON file.

        :param file_path: The path to the input JSON file.
        :type file_path: str
        :return: None
        """
        try:
            etl_manager = ETLManager()
            # Pass the file path directly to the ETL manager
            etl_manager.process(file_path)
            print(f"ETL process completed successfully for {file_path}\n")
        except Exception as e:
            print(f"Error during ETL process for {file_path}: {e}\n")


def run() -> None:
    """
    Entry point for the CLI application. Initializes and runs the ETLAppCli class.

    :return: None
    """
    ETLAppCli().run()
