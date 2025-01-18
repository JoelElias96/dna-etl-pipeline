# ETL System for Genetic Data Processing

## Overview

This project implements an ETL (Extract, Transform, Load) system designed to process genetic data, specifically DNA sequences. The system is tailored to handle unstructured data from files and produce a structured, normalized JSON file for analysis. It supports two file types:

- **Txt files: Containing DNA sequences.
- **JSON files: Containing metadata about the DNA test.

The project ensures data accuracy and privacy by validating inputs, removing sensitive information, and performing required transformations.

---

## Features

1. **File Processing**:

   - Computes GC content and codon frequency for DNA sequences.
   - Identifies the most frequent codon across sequences.
   - Determines the Longest Common Subsequence (LCS) among DNA sequences.
   - Sanitizes JSON metadata by removing sensitive fields, validating lengths, and ensuring dates are within the specified range.

2. **ETL Workflow**:

   - **Extract**: Reads `.txt` and `.json` files, validates them, and extracts required data.
   - **Transform**: Processes files based on their type and applies specific transformations.
   - **Load**: Combines processed data into a single JSON file and saves it to the specified output directory.

3. **Flexible Interfaces**:

   - **GUI**: A user-friendly graphical interface built with `tkinter`.
   - **CLI**: A command-line interface for scriptable operations.

---

## Installation

### Prerequisites

- Python 3.8+
- Required packages (install via pip):
  ```bash
  pip install -r requirements.txt
  ```

### Folder Structure

```
project-root/
├── pipeline/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── processors/
│       ├── file_processor.py
│       ├── test_metadata_json_processor.py
│       └── dna_sequence_txt_processor.py
├── utils/
├──── input_validator.py
├── main.py
├── gui/
├──── gui.py
├── cli/
├──── cli.py
├── tests/
│   ├── test_extract.py
│   ├── test_file_validation.py
│   ├── test_json_processor.py
│   ├── test_processor_factory.py
│   └── test_txt_processor
├── data/
│   └── inputs/
│           ├── invalid/
│               ├── 7a2bc928-9ea0-498e-80f1-3113da2b50a6_input.json
│               ├....
│               └── invalid_json_input.json
│           ├── valid/
│               ├── 12ba71a0-30f4-464e-ba1b-9a31ea7d35fc_input.json
│               ├....
│               └── ffa093c9-c178-4631-9f0f-7be686d602b4_input.json
│       participants/
│           ├── 7a2bc928-9ea0-498e-80f1-3113da2b50a6/
│           ├....
│           └── ffa093c9-c178-4631-9f0f-7be686d602b4/
├──requirements.txt
└── README.md
```

---

## How to Use

### 1. Running the Application

#### GUI Mode

To launch the graphical user interface:

```bash
python main.py
```

#### CLI Mode

To use the command-line interface:

```bash
python main.py -i <input_file_or_directory>
```

### 2. Input Format

The input JSON should contain the following structure:

```json
{
  "context_path": "<path_to_input_files>",
  "results_path": "<path_to_output_directory>/out/"
}
```

- `context_path`: Directory containing `.txt` and `.json` files.
- `results_path`: Directory where the output JSON will be saved.

Ensure that the input directory contains both `.txt` and `.json` files with matching UUIDs in their filenames.

### 3. Output

The system generates a structured JSON file in the `results_path`. Example:

```json
{
  "metadata": {
    "start_at": "2025-01-18T12:00:00Z",
    "end_at": "2025-01-18T12:01:00Z",
    "context_path": "<input_directory>",
    "results_path": "<output_directory>/out/"
  },
  "results": [
    {
      "participant": {"_id": "<uuid>"},
      "txt": {"sequences": [...], "most_common_codon": "...", "lcs": {...}},
      "json": {"test_metadata": {...}, "analysis_metadata": {...}, "individual_metadata": {...}}
    }
  ]
}
```

---

## Development

### Key Files

- `pipeline/extract.py`: Handles data extraction and validation.
- `pipeline/transform.py`: Processes and transforms data.
- `pipeline/load.py`: Saves the final output.
- `gui.py`: Provides the graphical user interface.
- `cli.py`: Implements the command-line interface.

### Testing

Unit tests are included for individual components. To run tests:

```bash
pytest tests/
```

---

## Known Limitations

- The GUI does not support batch processing.
- Performance may degrade for very large DNA datasets during LCS computation.

---

## Author

Joel Elias

For questions or feedback, contact me at [Joelel1996@gmail.com](mailto\:Joelel1996@gmail.com)

