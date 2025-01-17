import pytest
from pipeline.processors.dna_sequence_txt_processor import DNASequenceTxtProcessor


class TestGCContent:

    def test_gc_content_case1(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        assert processor._gc_content("ATCGATCGTAGCTAGCTAGCTGATCGATCGAT") == pytest.approx(46.88, 0.01)

    def test_gc_content_case2(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        assert processor._gc_content("ATCGGTAAATGCCTGAAAGATG") == pytest.approx(40.91, 0.01)

    def test_gc_content_case3(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        assert processor._gc_content("CGTACGTAGCTA") == pytest.approx(50.0, 0.01)

    def test_gc_content_case4(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        assert processor._gc_content("ATATATATATAT") == pytest.approx(0.0, 0.01)

    def test_gc_content_case5(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        assert processor._gc_content("GCGCGCGCGCGC") == pytest.approx(100.0, 0.01)

    def test_gc_content_case6(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        assert processor._gc_content("ATGCATGCATGC") == pytest.approx(50.0, 0.01)

    def test_gc_content_case7(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        assert processor._gc_content("TTTT") == pytest.approx(0.0, 0.01)

    def test_gc_content_case8(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        assert processor._gc_content("GGGG") == pytest.approx(100.0, 0.01)

    def test_gc_content_case9(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        assert processor._gc_content("AAAA") == pytest.approx(0.0, 0.01)

    def test_gc_content_case10(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        assert processor._gc_content("CCCC") == pytest.approx(100.0, 0.01)

    def test_gc_content_long_sequence(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        long_sequence = "A" * 1000000 + "C" * 1000000 + "G" * 1000000 + "T" * 1000000
        assert processor._gc_content(long_sequence) == pytest.approx(50.0, 0.01)

    def test_gc_content_another_long_sequence(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        long_sequence = "A" * 3333 + "TGC\n"
        assert processor._gc_content(long_sequence) == pytest.approx(0.06, 0.01)

    def test_gc_content_empty_sequence(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        with pytest.raises(ValueError, match="The sequence cannot be empty."):
            processor._gc_content("")


class TestCodonFrequency:

    def test_codon_frequency_case1(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        sequence = "ATGCGATACGCTT"
        expected_frequency = {
            "ATG": 1,
            "CGA": 1,
            "TAC": 1,
            "GCT": 1
        }
        assert processor._codon_frequency(sequence) == expected_frequency, f"Failed on {sequence}"

    def test_codon_frequency_case2(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        sequence = "ATCGATCG"
        expected_frequency = {
            "ATC": 1,
            "GAT": 1,
        }
        assert processor._codon_frequency(sequence) == expected_frequency, f"Failed on {sequence}"

    def test_codon_frequency_case3(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        sequence = "CGTACGTAGCTA"
        expected_frequency = {
            "CGT": 1,
            "ACG": 1,
            "TAG": 1,
            "CTA": 1
        }
        assert processor._codon_frequency(sequence) == expected_frequency, f"Failed on {sequence}"

    def test_codon_frequency_case4(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        sequence = "ATATATATATAT"
        expected_frequency = {
            "ATA": 2,
            "TAT": 2
        }
        assert processor._codon_frequency(sequence) == expected_frequency, f"Failed on {sequence}"

    def test_codon_frequency_case5(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        sequence = "GCGCGCGCGCGC"
        expected_frequency = {
            "GCG": 2,
            "CGC": 2
        }
        assert processor._codon_frequency(sequence) == expected_frequency, f"Failed on {sequence}"

    def test_codon_frequency_case6(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        sequence = "ATGCATGCATGC"
        expected_frequency = {
            "ATG": 1,
            "CAT": 1,
            "GCA": 1,
            "TGC": 1
        }
        assert processor._codon_frequency(sequence) == expected_frequency, f"Failed on {sequence}"

    def test_codon_frequency_case7(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        sequence = "TTTT"
        expected_frequency = {
            "TTT": 1
        }
        assert processor._codon_frequency(sequence) == expected_frequency, f"Failed on {sequence}"

    def test_codon_frequency_case8(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        sequence = "GGGG"
        expected_frequency = {
            "GGG": 1
        }
        assert processor._codon_frequency(sequence) == expected_frequency, f"Failed on {sequence}"

    def test_codon_frequency_case9(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        sequence = "AAAA"
        expected_frequency = {
            "AAA": 1
        }
        assert processor._codon_frequency(sequence) == expected_frequency, f"Failed on {sequence}"

    def test_codon_frequency_case10(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        sequence = "CCCC"
        expected_frequency = {
            "CCC": 1
        }
        assert processor._codon_frequency(sequence) == expected_frequency, f"Failed on {sequence}"

    def test_codon_frequency_long_sequence(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        long_sequence = "A" * 333333 + "C" * 333333 + "G" * 333333 + "T" * 333333
        expected_frequency = {
            "AAA": 111111,
            "CCC": 111111,
            "GGG": 111111,
            "TTT": 111111
        }
        assert processor._codon_frequency(long_sequence) == expected_frequency

    def test_codon_frequency_empty_sequence(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        with pytest.raises(ValueError, match="The sequence cannot be empty."):
            processor._codon_frequency("")


class TestMostFrequentCodon:

    def test_simple_case(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        codon_frequencies = [
            {"ATG": 1, "CGA": 2, "TAC": 1},
            {"CGA": 3, "TGC": 1},
            {"CGA": 1, "ATG": 2, "TAC": 2}
        ]
        expected_most_common = ["CGA"]  # Appears 6 times in total
        assert processor._most_frequent_codons(codon_frequencies) == expected_most_common

    def test_single_codon_frequency(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        codon_frequencies = [
                            {"ATG": 5, "CGA": 2, "TAC": 1}
                            ]
        expected_most_common = ["ATG"]  # Most frequent in the single dictionary
        assert processor._most_frequent_codons(codon_frequencies) == expected_most_common

    def test_multiple_codons_same_frequency(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        codon_frequencies = [
                            {"ATG": 3, "CGA": 3, "TAC": 3},
                            {"TAC": 3, "CGA": 3}
                            ]
        expected_most_common = ["CGA", "TAC"]  # Both codons have the highest frequency
        assert processor._most_frequent_codons(codon_frequencies) == expected_most_common

    def test_empty_frequencies(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        codon_frequencies = []
        with pytest.raises(ValueError, match="No codon frequencies provided."):
            processor._most_frequent_codons(codon_frequencies)

    def test_tie_in_frequencies(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        codon_frequencies = [
                            {"ATG": 2, "CGA": 2},
                            {"TAC": 4, "CGA": 2}
                            ]
        expected_most_common = ["CGA", "TAC"]
        assert processor._most_frequent_codons(codon_frequencies) == expected_most_common

    def test_large_number_of_frequencies(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        codon_frequencies = [
                            {"ATG": 1000, "CGA": 2000, "TAC": 1500},
                            {"TGC": 3000, "CGA": 2500}
                            ]
        expected_most_common = ["CGA"]  # Most frequent in the combined dictionaries
        assert processor._most_frequent_codons(codon_frequencies) == expected_most_common


class TestLongestCommonSubsequence:
    def test_simple_case_with_one_continuous_subsequence(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        seq1 = "ATCGATCGTAGCTAGCTAGCTGATCGATCGAT"
        seq2 = "ATCGGTAAATGCCTGAAAGATG"
        expected_lcs = "ATCG"
        assert processor._lcs_between_two(seq1, seq2) == expected_lcs

    def test_no_common_continuous_subsequence(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        seq1 = "AAAA"
        seq2 = "TTTT"
        expected_lcs = ""
        assert processor._lcs_between_two(seq1, seq2) == expected_lcs

    def test_one_sequence_is_empty(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        seq1 = "ATCG"
        seq2 = ""
        expected_lcs = ""
        assert processor._lcs_between_two(seq1, seq2) == expected_lcs

    def test_both_sequences_are_empty(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        seq1 = ""
        seq2 = ""
        expected_lcs = ""
        assert processor._lcs_between_two(seq1, seq2) == expected_lcs

    def test_entire_sequence_is_common(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        seq1 = "ATCG"
        seq2 = "ATCG"
        expected_lcs = "ATCG"
        assert processor._lcs_between_two(seq1, seq2) == expected_lcs

    def test_continuous_subsequence_in_the_middle(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        seq1 = "GATTACAGTACG"
        seq2 = "TAC"
        expected_lcs = "TAC"
        assert processor._lcs_between_two(seq1, seq2) == expected_lcs

    def test_continuous_subsequence_at_the_start(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        seq1 = "ATCGGGG"
        seq2 = "ATC"
        expected_lcs = "ATC"
        assert processor._lcs_between_two(seq1, seq2) == expected_lcs

    def test_continuous_subsequence_at_the_end(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        seq1 = "GGGGATCG"
        seq2 = "ATCG"
        expected_lcs = "ATCG"
        assert processor._lcs_between_two(seq1, seq2) == expected_lcs

    def test_single_character_common_subsequence(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        seq1 = "ATCG"
        seq2 = "G"
        expected_lcs = "G"
        assert processor._lcs_between_two(seq1, seq2) == expected_lcs

    def test_larger_sequences_with_a_small_common_substring(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        seq1 = "A" * 1000000 + "TGC" + "G" * 1000000
        seq2 = "TGC"
        expected_lcs = "TGC"
        assert processor._lcs_between_two(seq1, seq2) == expected_lcs

    def test_overlapping_subsequences_choose_the_longest_continuous_one(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        seq1 = "AGTACGCA"
        seq2 = "TACG"
        expected_lcs = "TACG"
        assert processor._lcs_between_two(seq1, seq2) == expected_lcs

    def test_two_large_sequences(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        seq1 = "A" * 10000 + "C" * 10000 + "G" * 10000 + "T" * 10000
        seq2 = "A" * 10000 + "TGC"
        expected_lcs = "A" * 10000
        assert processor._lcs_between_two(seq1, seq2) == expected_lcs


class TestLongestCommonSubsequenceAmongAll:
    def test_simple_case_with_one_continuous_subsequence(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        processor.dna_sequences = [
            "ATCGATCGTAGCTAGCTAGCTGATCGATCGAT",
            "ATCGGTAAATGCCTGAAAGATG"
        ]
        expected_result = [
            {"value": "ATCG", "sequences": [1, 2], "length": 4}
        ]
        assert processor._longest_common_subsequence_among_all() == expected_result

    def test_no_common_continuous_subsequence(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        processor.dna_sequences = ["AAAA", "TTTT"]
        expected_result = []
        assert processor._longest_common_subsequence_among_all() == expected_result

    def test_single_sequence(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        processor.dna_sequences = ["ATCG"]
        expected_result = []
        assert processor._longest_common_subsequence_among_all() == expected_result

    def test_multiple_identical_sequences(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        processor.dna_sequences = ["ATCG", "ATCG", "ATCG"]
        expected_result = [
            {"value": "ATCG", "sequences": [1, 2, 3], "length": 4}
        ]
        assert processor._longest_common_subsequence_among_all() == expected_result

    def test_several_common_subsequences(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        processor.dna_sequences = [
            "ATCGATCGTAGCTAGCTAGCTGATCGATCGAT",
            "ATCGGTAAATGCCTGAAAGATG",
            "ATCGATCGTAGCTAGCTAGCTGATCGATCG"
        ]
        expected_result = [
            {"value": "ATCGATCGTAGCTAGCTAGCTGATCGATCG", "sequences": [1, 3], "length": 30}
        ]
        assert processor._longest_common_subsequence_among_all() == expected_result

    def test_subsequences_of_equal_length(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        processor.dna_sequences = [
            "ATCG",
            "ATCGTACG",
            "TACG"
        ]
        expected_result = [
            {
                "value": "ATCG",
                "sequences": [1, 2],  # Sequence 1 and Sequence 2
                "length": 4
            },
            {
                "value": "TACG",
                "sequences": [2, 3],  # Sequence 2 and Sequence 3
                "length": 4
            }
        ]
        assert processor._longest_common_subsequence_among_all() == expected_result

    def test_overlapping_subsequences(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        processor.dna_sequences = [
            "AGTACGCA",
            "TACG"
        ]
        expected_result = [
            {"value": "TACG", "sequences": [1, 2], "length": 4}
        ]
        assert processor._longest_common_subsequence_among_all() == expected_result

    def test_sequences_with_no_overlap(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        processor.dna_sequences = [
            "ACGTA",
            "TGCA"
        ]
        expected_result = [
            {
                'length': 1,
                'sequences': [1, 2],
                'value': 'A',
            },
        ]
        assert processor._longest_common_subsequence_among_all() == expected_result

    def test_large_sequences_with_common_subsequence(self):
        processor = DNASequenceTxtProcessor("dummy_path")
        processor.dna_sequences = [
            "A" * 10000 + "C" * 10000 + "G" * 10000 + "T" * 10000,
            "A" * 10000 + "TGC"
        ]
        expected_result = [
            {"value": "A" * 10000, "sequences": [1, 2], "length": 10000}
        ]
        assert processor._longest_common_subsequence_among_all() == expected_result


class TestProcessDNATxtFile:

    def write_and_test(self, tmp_path, file_content: str, expected_output: dict, case_name: str):
        """
        Helper function to write a file and run the test.
        """
        # Create a temporary file in the provided tmp_path
        file_path = tmp_path / "dna_sequences.txt"
        file_path.write_text(file_content)

        # Initialize the TXTProcessor with the file path
        processor = DNASequenceTxtProcessor(file_path)

        # Run the test and compare the result with the expected output
        assert processor.process() == expected_output, f"Failed on {case_name}"

    def test_two_sequences_normal_case(self, tmp_path):
        self.write_and_test(
            tmp_path,
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
                "most_common_codon": ["GAT"],  # Changed to list to match output
                "lcs": [
                    {
                        "value": "ATCG",
                        "sequences": [1, 2],
                        "length": 4,
                    },
                ],
            },
            case_name="Two sequences, normal case",
        )

    def test_single_sequence(self, tmp_path):
        self.write_and_test(
            tmp_path,
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
                "most_common_codon": ["GAT"],  # Changed to list to match output
                "lcs": [],  # No LCS for single sequence
            },
            case_name="Single sequence",
        )

    def test_all_identical_sequences(self, tmp_path):
        self.write_and_test(
            tmp_path,
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
                "most_common_codon": ["ATC", "GAT"],  # Changed to list to handle multiple most common codons
                "lcs": [
                    {
                        "value": "ATCGATCG",
                        "sequences": [1, 2, 3],  # Adjusted to exclude sequence 3
                        "length": 8,
                    },
                ],
            },
            case_name="All identical sequences",
        )

    def test_two_pairs_identical_sequences(self, tmp_path):
        self.write_and_test(
            tmp_path,
            file_content=(
                "ATCGATCG\n"
                "ATCGATCG\n"
                "ATCTATCG\n"
                "ATCTATCG\n"
            ),
            expected_output={
                "sequences": [
                    {"gc_content": 50.0, "codons": {"ATC": 1, "GAT": 1}},
                    {"gc_content": 50.0, "codons": {"ATC": 1, "GAT": 1}},
                    {"gc_content": 37.5, "codons": {"ATC": 1, "TAT": 1}},
                    {"gc_content": 37.5, "codons": {"ATC": 1, "TAT": 1}},
                ],
                "most_common_codon": ["ATC"],  # Two most common codons
                "lcs": [
                    {
                        "value": "ATCGATCG",
                        "sequences": [1, 2],  # Only the first two sequences should be included
                        "length": 8,
                    },
                    {
                        "value": "ATCTATCG",
                        "sequences": [3, 4],  # The second pair of identical sequences
                        "length": 8,
                    },
                ],
            },
            case_name="All identical sequences with variation",
        )

    def test_long_sequences(self, tmp_path):
        self.write_and_test(
            tmp_path,
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
                "most_common_codon": ["AAA"],  # Changed to list to match output
                "lcs": [
                    {
                        "value": "A" * 3333 + "TGC",
                        "sequences": [1, 2],
                        "length": 3336,
                    },
                ],
            },
            case_name="Long sequences",
        )

    def test_another_long_sequence(self, tmp_path):
        self.write_and_test(
            tmp_path,
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
                        "gc_content": 0.06,  # GC is 2 out of 3336
                        "codons": {"AAA": 1111, "TGC": 1},
                    },
                ],
                "most_common_codon": ["AAA"],  # Changed to list to match output
                "lcs": [
                    {
                        "value": "A" * 3333,
                        "sequences": [1, 2],
                        "length": 3333,
                    },
                ],
            },
            case_name="Another long sequence",
        )
