import pytest

 
def test_gc_content():
    from src.txt_processor import _gc_content
    assert _gc_content("ATCGATCGTAGCTAGCTAGCTGATCGATCGAT") == pytest.approx(46.88, 0.01), "Failed on ATCGATCGTAGCTAGCTAGCTGATCGATCGAT"
    assert _gc_content("ATCGGTAAATGCCTGAAAGATG") == pytest.approx(40.91, 0.01), "Failed on ATCGGTAAATGCCTGAAAGATG"
    assert _gc_content("CGTACGTAGCTA") == pytest.approx(50.0, 0.01), "Failed on CGTACGTAGCTA"
    assert _gc_content("ATATATATATAT") == pytest.approx(0.0, 0.01), "Failed on ATATATATATAT"
    assert _gc_content("GCGCGCGCGCGC") == pytest.approx(100.0, 0.01), "Failed on GCGCGCGCGCGC"
    assert _gc_content("ATGCATGCATGC") == pytest.approx(50.0, 0.01), "Failed on ATGCATGCATGC"
    assert _gc_content("TTTT") == pytest.approx(0.0, 0.01), "Failed on TTTT"
    assert _gc_content("GGGG") == pytest.approx(100.0, 0.01), "Failed on GGGG"
    assert _gc_content("AAAA") == pytest.approx(0.0, 0.01), "Failed on AAAA"
    assert _gc_content("CCCC") == pytest.approx(100.0, 0.01), "Failed on CCCC" 
    long_sequence = "A" * 1000000 + "C" * 1000000 + "G" * 1000000 + "T" * 1000000
    assert _gc_content(long_sequence) == pytest.approx(50.0, 0.01), "Failed on long_sequence (1M of each nucleotide)"
    long_sequence = "A" * 3333 + "TGC\n"
    assert _gc_content(long_sequence) == pytest.approx(0.06, 0.01), "Failed on long_sequence (1M of each nucleotide)"
    with pytest.raises(ValueError, match="The sequence cannot be empty."):
        _gc_content("")

def test_codon_frequency():

    from src.txt_processor import _codon_frequency

    sequence = "ATGCGATACGCTT"
    expected_frequency = {
        "ATG": 1,
        "CGA": 1,
        "TAC": 1,
        "GCT": 1
    }
    assert _codon_frequency(sequence) == expected_frequency, f"Failed on {sequence}"


    sequence = "ATCGATCG"
    expected_frequency = {
        "ATC": 1,
        "GAT": 1,
    }
    assert _codon_frequency(sequence) == expected_frequency, f"Failed on {sequence}"

    sequence = "CGTACGTAGCTA"
    expected_frequency = {
        "CGT": 1,
        "ACG": 1,
        "TAG": 1,
        "CTA": 1
    }
    assert _codon_frequency(sequence) == expected_frequency, f"Failed on {sequence}"

    sequence = "ATATATATATAT"
    expected_frequency = {
        "ATA": 2,
        "TAT": 2
    }
    assert _codon_frequency(sequence) == expected_frequency, f"Failed on {sequence}"

    sequence = "GCGCGCGCGCGC"
    expected_frequency = {
        "GCG": 2,
        "CGC": 2
    }
    assert _codon_frequency(sequence) == expected_frequency, f"Failed on {sequence}"

    sequence = "ATGCATGCATGC"
    expected_frequency = {
        "ATG": 1,
        "CAT": 1,
        "GCA": 1,
        "TGC": 1
    }
    assert _codon_frequency(sequence) == expected_frequency, f"Failed on {sequence}"

    sequence = "TTTT"
    expected_frequency = {
        "TTT": 1  
    }
    assert _codon_frequency(sequence) == expected_frequency, f"Failed on {sequence}"

    sequence = "GGGG"
    expected_frequency = {
        "GGG": 1 
    }
    assert _codon_frequency(sequence) == expected_frequency, f"Failed on {sequence}"

    sequence = "AAAA"
    expected_frequency = {
        "AAA": 1  
    }
    assert _codon_frequency(sequence) == expected_frequency, f"Failed on {sequence}"

    sequence = "CCCC"
    expected_frequency = {
        "CCC": 1 
    }
    assert _codon_frequency(sequence) == expected_frequency, f"Failed on {sequence}"

    long_sequence = "A" * 333333 + "C" * 333333 + "G" * 333333 + "T" * 333333
    expected_frequency = {
        "AAA": 111111,
        "CCC": 111111,
        "GGG": 111111,
        "TTT": 111111
       
    }
    assert _codon_frequency(long_sequence) == expected_frequency, "Failed on long_sequence (1M of each nucleotide)"

    with pytest.raises(ValueError, match="The sequence cannot be empty."):
        _codon_frequency("")

def test_most_frequent_codon():
    from src.txt_processor import _most_frequent_codon

    # Test 1: Simple case
    codon_frequencies = [
        {"ATG": 1, "CGA": 2, "TAC": 1},
        {"CGA": 3, "TGC": 1},
        {"CGA": 1, "ATG": 2, "TAC": 2}
    ]
    expected_most_common = "CGA"  # Appears 6 times in total
    assert _most_frequent_codon(codon_frequencies) == expected_most_common, "Failed on Test 1"

    # Test 2: Single codon frequency dictionary
    codon_frequencies = [
        {"ATG": 5, "CGA": 2, "TAC": 1}
    ]
    expected_most_common = "ATG"  # Most frequent in the single dictionary
    assert _most_frequent_codon(codon_frequencies) == expected_most_common, "Failed on Test 2"

    # Test 3: Multiple codons with the same frequency
    codon_frequencies = [
        {"ATG": 3, "CGA": 3, "TAC": 2},
        {"TAC": 3, "CGA": 3}
    ]
    expected_most_common = "CGA"  # First codon with the highest frequency
    assert _most_frequent_codon(codon_frequencies) == expected_most_common, "Failed on Test 3"

    # Test 4: Empty list of frequencies
    codon_frequencies = []
    try:
        _most_frequent_codon(codon_frequencies)
        assert False, "Failed on Test 4: Should have raised an error"
    except ValueError as e:
        assert str(e) == "No codon frequencies provided.", "Failed on Test 4: Incorrect error message"

    # Test 5: Tie in frequencies
    codon_frequencies = [
        {"ATG": 2, "CGA": 2},
        {"TAC": 2, "CGA": 2}
    ]
    expected_most_common = "CGA"  # First codon with the highest frequency
    assert _most_frequent_codon(codon_frequencies) == expected_most_common, "Failed on Test 5"
    
    # Test 6: Codon frequencies with zero counts
    codon_frequencies = [
        {"ATG": 0, "CGA": 0, "TAC": 0},
        {"TGC": 0, "CGA": 0}
    ]
    assert _most_frequent_codon(codon_frequencies) == "", "Failed on Test 6"

    # Test 7: Large number of codon frequencies
    codon_frequencies = [
        {"ATG": 1000, "CGA": 2000, "TAC": 1500},
        {"TGC": 3000, "CGA": 2500}
    ]
    expected_most_common = "CGA"  # Most frequent in the combined dictionaries
    assert _most_frequent_codon(codon_frequencies) == expected_most_common, "Failed on Test 7"

def test_longest_common_subsequence():
    from src.txt_processor import _longest_common_subsequence

    # Test 1: Simple case with one continuous subsequence
    seq1 = "ATCGATCGTAGCTAGCTAGCTGATCGATCGAT"
    seq2 = "ATCGGTAAATGCCTGAAAGATG"
    expected_lcs = "ATCG"
    assert _longest_common_subsequence(seq1, seq2) == expected_lcs, "Failed on Test 1"

    # Test 2: No common continuous subsequence
    seq1 = "AAAA"
    seq2 = "TTTT"
    expected_lcs = ""
    assert _longest_common_subsequence(seq1, seq2) == expected_lcs, "Failed on Test 2"

    # Test 3: One sequence is empty
    seq1 = "ATCG"
    seq2 = ""
    expected_lcs = ""
    assert _longest_common_subsequence(seq1, seq2) == expected_lcs, "Failed on Test 3"

    # Test 4: Both sequences are empty
    seq1 = ""
    seq2 = ""
    expected_lcs = ""
    assert _longest_common_subsequence(seq1, seq2) == expected_lcs, "Failed on Test 4"

    # Test 5: Entire sequence is common
    seq1 = "ATCG"
    seq2 = "ATCG"
    expected_lcs = "ATCG"
    assert _longest_common_subsequence(seq1, seq2) == expected_lcs, "Failed on Test 5"

    # Test 6: Continuous subsequence in the middle
    seq1 = "GATTACAGTACG"
    seq2 = "TAC"
    expected_lcs = "TAC"
    assert _longest_common_subsequence(seq1, seq2) == expected_lcs, "Failed on Test 6"

    # Test 7: Continuous subsequence at the start
    seq1 = "ATCGGGG"
    seq2 = "ATC"
    expected_lcs = "ATC"
    assert _longest_common_subsequence(seq1, seq2) == expected_lcs, "Failed on Test 7"

    # Test 8: Continuous subsequence at the end
    seq1 = "GGGGATCG"
    seq2 = "ATCG"
    expected_lcs = "ATCG"
    assert _longest_common_subsequence(seq1, seq2) == expected_lcs, "Failed on Test 8"

    # Test 9: Single character common subsequence
    seq1 = "ATCG"
    seq2 = "G"
    expected_lcs = "G"
    assert _longest_common_subsequence(seq1, seq2) == expected_lcs, "Failed on Test 9"

    # Test 10: Larger sequences with a small common substring
    seq1 = "A" * 1000000 + "TGC" + "G" * 1000000
    seq2 = "TGC"
    expected_lcs = "TGC"
    assert _longest_common_subsequence(seq1, seq2) == expected_lcs, "Failed on Test 10"

    # Test 11: Overlapping subsequences (choose the longest continuous one)
    seq1 = "AGTACGCA"
    seq2 = "TACG"
    expected_lcs = "TACG"
    assert _longest_common_subsequence(seq1, seq2) == expected_lcs, "Failed on Test 11"

    # Test 12: two large sequences
    seq1 = "A" * 10000 + "C" * 10000 + "G" * 10000 + "T" * 10000
    seq2 = "A" * 10000 + "TGC"
    expected_lcs = "A" * 10000
    assert _longest_common_subsequence(seq1, seq2) == expected_lcs, "Failed on Test 12"

def test_process_dna_txt_file(tmp_path):
    from src.txt_processor import process_dna_txt_file

    def write_and_test(file_content : str , expected_output : dict, case_name :str):
        """
        Helper function to write a file and run the test.
        """
        # Create a temporary file in the provided tmp_path
        file_path = tmp_path / "dna_sequences.txt"
        file_path.write_text(file_content)

        # Run the test and compare the result with the expected output
        assert process_dna_txt_file(file_path) == expected_output, f"Failed on {case_name}"

    # Test 1: Two sequences, normal case
    write_and_test(
        file_content=(
            "ATCGATCGTAGCTAGCTAGCTGATCGATCGAT\n"
            "ATCGGTAAATGCCTGAAAGATG\n"
        ),
        expected_output={
            "sequences": [
                {
                    "gc_content": 46.88,
                    "codons": {
                        "ATC": 1,
                        "GAT": 2,
                        "CGT": 1,
                        "AGC": 1,
                        "TAG": 1,
                        "CTA": 1,
                        "GCT": 1,
                        "CGA": 1,
                        "TCG": 1,
                    },
                },
                {
                    "gc_content": 40.91,
                    "codons": {
                        "ATC": 1,
                        "GGT": 1,
                        "AAA": 2,
                        "TGC": 1,
                        "CTG": 1,
                        "GAT": 1,
                    },
                },
            ],
            "most_common_codon": "GAT",
            "lcs": {
                "value": "ATCG",
                "sequences": [1, 2],
                "length": 4,
            },
        },
        case_name="Two sequences, normal case",
    )

    # Test 2: Single sequence
    write_and_test(
        file_content="ATCGATCGTAGCTAGCTAGCTGATCGATCGAT\n",
        expected_output={
            "sequences": [
                {
                    "gc_content": 46.88,
                    "codons": {
                        "ATC": 1,
                        "GAT": 2,
                        "CGT": 1,
                        "AGC": 1,
                        "TAG": 1,
                        "CTA": 1,
                        "GCT": 1,
                        "CGA": 1,
                        "TCG": 1,
                    },
                },
            ],
            "most_common_codon": "GAT",
            "lcs": {
                "value": "",
                "sequences": [],
                "length": 0,
            },
        },
        case_name="Single sequence",
    )


    # Test 4: All identical sequences
    write_and_test(
        file_content=(
            "ATCGATCG\n"
            "ATCGATCG\n"
            "ATCGATCG\n"
        ),
        expected_output={
            "sequences": [
                {"gc_content": 50.0, "codons": {"ATC": 1, "GAT": 1}},
                {"gc_content": 50.0, "codons": {"ATC": 1, "GAT": 1}},
                {"gc_content": 50.0, "codons": {"ATC": 1, "GAT": 1}},
            ],
            "most_common_codon": "ATC",  # Could also be "CGA" or "TCG"
            "lcs": {
                "value": "ATCGATCG",
                "sequences": [1, 2],
                "length": 8,
            },
        },
        case_name="All identical sequences",
    )

    # Test 5: Long sequences
    write_and_test(
        file_content=(
            "A" * 3333 + "TGC\n" +
            "A" * 3333 + "TGC\n"
        ),
        expected_output={
            "sequences": [
                {
                    "gc_content": 0.06,  # GC is 3 out of 1,000,003
                    "codons": {"AAA": 1111, "TGC": 1},
                },
                {
                    "gc_content": 0.06,
                    "codons": {"AAA": 1111, "TGC": 1},
                },
            ],
            "most_common_codon": "AAA",  # Most frequent codon
            "lcs": {
                "value": "A" * 3333 + "TGC",
                "sequences": [1, 2],
                "length": 3336,
            },
        },
        case_name="Long sequences",
    )

    # Test 6: another long sequence
    write_and_test(
        file_content=(
            "A" * 3333 + "C" * 3333 + "G" * 3333 + "T" * 3333 + "\n" +
            "A" * 3333 + "TGC\n"
        ),
        expected_output={
            "sequences": [
                {
                    "gc_content": 50.00,  # GC is 6,666 out of 13,332
                    "codons": {"AAA": 1111, "CCC": 1111, "GGG": 1111, "TTT": 1111},
                },
                {
                    "gc_content": 0.06 ,# GC is 2 out of 3336
                    "codons": {"AAA": 1111, "TGC": 1},
                },
            ],
            "most_common_codon": "AAA",  # Most frequent codon
            "lcs": {
                "value": "A" * 3333,
                "sequences": [1, 2],
                "length": 3333,
            },
        },
        case_name="Long sequences",
    )