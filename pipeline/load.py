import json


class Load:
    """
    A class responsible for loading results into a JSON file.

    This class provides functionality to save participant data into a specified JSON output file.

    Attributes:
        results_path (str): The path where the results will be stored.

    Methods:
        load_results(participant_data, output_file):
            Saves the provided participant data into the specified JSON output file.
    """

    def __init__(self, results_path):
        """
        Initialize the Load class with the path where the results should be saved.

        :param results_path: The directory path where the results will be stored.
        :type results_path: str
        """
        self.results_path = results_path

    def load_results(self, participant_data, output_file):
        """
        Saves the provided participant data into the specified output file in JSON format.

        This method serializes the `participant_data` into a JSON format and writes it to a file
        specified by `output_file`. The data is written with an indentation of 4 spaces for readability.

        :param participant_data: The data to be saved to the JSON file.
        :type participant_data: dict or any serializable data structure
        :param output_file: The path of the output file where the data will be saved.
        :type output_file: str
        """
        # Save the results to a JSON file
        with open(output_file, "w") as f:
            json.dump(participant_data, f, indent=4)
