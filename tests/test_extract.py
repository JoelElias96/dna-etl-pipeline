from pipeline.extract import Extract


class TestExtractFiles:

    def test_extract_files(self, tmp_path):
        # Create a temporary directory
        context_path = tmp_path / "context"
        context_path.mkdir()
        # Create a few files in the temporary directory
        file1 = context_path / "file1.csv"
        file1.write_text("data1")
        file2 = context_path / "file2.csv"
        file2.write_text("data2")
        # Initialize the Extract class with the input data
        input_data = {"context_path": str(context_path)}
        extract = Extract(input_data)
        # Extract the files from the context path
        files_list = extract._extract_files(context_path)
        # Check if the files are extracted correctly
        assert files_list == ["file1.csv", "file2.csv"]

    def test_extract_multyple_files(self, tmp_path):
        # Create a temporary directory
        context_path = tmp_path / "context"
        context_path.mkdir()
        # Create a few files in the temporary directory
        file1 = context_path / "file1.csv"
        file1.write_text("data1")
        file2 = context_path / "file2.java"
        file2.write_text("data2")
        file3 = context_path / "file3.py"
        file3.write_text("data3")
        file4 = context_path / "file4.json"
        file4.write_text("data4")
        file5 = context_path / "file5.txt"
        file5.write_text("data5")
        file6 = context_path / "file6.pdf"
        file6.write_text("data6")
        file7 = context_path / "file7.xlsx"
        file7.write_text("data7")
        file8 = context_path / "file8.docx"
        file8.write_text("data8")

        # Initialize the Extract class with the input data
        input_data = {"context_path": str(context_path)}
        extract = Extract(input_data)
        # Extract the files from the context path
        files_list = extract._extract_files(context_path)
        # Check if the files are extracted correctly
        assert files_list == (["file1.csv", "file2.java", "file3.py", "file4.json", "file5.txt",
                               "file6.pdf", "file7.xlsx", "file8.docx"])


class TestExtract:
    def test_extract(self, tmp_path):
        # Create a temporary directory
        context_path = tmp_path / "context"
        context_path.mkdir()
        # Create a few files in the temporary directory
        file1 = context_path / "file1.csv"
        file1.write_text("data1")
        file2 = context_path / "file2.csv"
        file2.write_text("data2")
        # Initialize the Extract class with the input data
        input_data = {"context_path": str(context_path)}
        extract = Extract(input_data)
        # Extract the files and the UUID from the context path
        files_list, uuid = extract.extract()
        # Check if the files and UUID are extracted correctly
        assert files_list == ["file1.csv", "file2.csv"]
        assert uuid == "context"
