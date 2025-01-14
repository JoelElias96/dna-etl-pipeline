import os

class InputValidator:

    def __init__(self, input_data: dict, validate_extentions : list):
        """
        Initializes the validator with the input data.
        :param input_data: Dictionary containing "context_path" and "results_path".
        :param validate_extentions: List of valid file extensions.
        """
        self.input_data = input_data
        self.context_path = input_data.get("context_path", "")
        self.results_path = input_data.get("results_path", "")
        self.file_mapping = {}
        self.validate_extentions=set(validate_extentions)
        self.files=[]

    def validate(self) -> dict:
        
        self._validate_structure()
        self._validate_paths()
        self._validate_files()
        return self.file_mapping

    def _validate_structure(self):
        """
        Check if input contains the required keys.

        Raises:
            ValueError: If the input does not contain the required keys.
        """
        if "context_path" not in self.input_data or "results_path" not in self.input_data:
            raise ValueError("Input must contain 'context_path' and 'results_path'.")

    def _validate_paths(self):
        """
        Check if paths exist and are valid directories.

        Raises:
            ValueError: If the paths do not exist or are not directories.
        """
        # Check if the context_path exists
        if not os.path.exists(self.context_path):
            raise ValueError(f"Invalid context_path: {self.context_path} does not exist.")
        
        # Check if the context_path is a directory
        if not os.path.isdir(self.context_path):
            raise ValueError(f"Invalid context_path: {self.context_path} is not a directory.")
        
        # Check if the results_path exists
        if not os.path.exists(self.results_path):
            raise ValueError(f"Invalid results_path: {self.results_path} does not exist.")
        
        # Check if the results_path is a directory
        if not os.path.isdir(self.results_path):
            raise ValueError(f"Invalid results_path: {self.results_path} must be a directory.")

    def _validate_files(self):
        
        self._make_files_list()

        # Group files by UUID
        for file in self.files:
            # Check if the file has a valid extension
            if isinstance(file,str) and file.endswith(".txt") or file.endswith(".json"):
               # Extract UUID from the file name
                uuid = file.rsplit("_", 1)[0]  
                # Add the file to the mapping
                if uuid not in self.file_mapping:
                    self.file_mapping[uuid] = []
                self.file_mapping[uuid].append(os.path.join(self.context_path, file))
            else:
                raise ValueError(f"Invalid file extension: {file}. Expected extensions: {self.validate_extentions}")


        self._validate_file_extensions()

    def _make_files_list(self): 
        """
        Validate files in the context_path and organize them by UUID.

        Raises:
            ValueError: If the context_path directory is empty
        """
        self.files = os.listdir(self.context_path)
        if not self.files:
            raise ValueError(f"The context_path directory is empty: {self.context_path}")
        
    def _validate_file_extensions(self):
        """
        Validate the file extensions for each UUID.

        Raises:
            ValueError: If the file extensions are invalid or if there are not exactly one file per required extension.
        """

        for uuid, paths in self.file_mapping.items():
            # Collect the extensions for this UUID
            file_extensions = [os.path.splitext(path)[1] for path in paths]

            # Validate extensions
            invalid_extensions = [ext for ext in file_extensions if ext not in self.validate_extentions]
            if invalid_extensions:
                raise ValueError(
                    f"Invalid file extensions {invalid_extensions} found for UUID '{uuid}'. "
                    f"Expected extensions: {self.validate_extentions}"
                )

            # Validate presence of exactly one file per required extension
            for ext in self.validate_extentions:
                if file_extensions.count(ext) != 1:
                    raise ValueError(
                        f"UUID '{uuid}' must have exactly one file with extension '{ext}', "
                        f"but found {file_extensions.count(ext)}."
                    )
      