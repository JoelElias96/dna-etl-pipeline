import pytest
from src.txt_processor import _gc_content, _codon_frequency, _most_frequent_codon, _longest_common_subsequence, process_dna_txt_file
 
class TestGCContent:
    from src.txt_processor import _gc_content

    def test_gc_content_case1(self):
        assert _gc_content("ATCGATCGTAGCTAGCTAGCTGATCGATCGAT") == pytest.approx(46.88, 0.01), "Failed on ATCGATCGTAGCTAGCTAGCTGATCGATCGAT"

    def test_gc_content_case2(self):
        assert _gc_content("ATCGGTAAATGCCTGAAAGATG") == pytest.approx(40.91, 0.01), "Failed on ATCGGTAAATGCCTGAAAGATG"

    def test_gc_content_case3(self):
        assert _gc_content("CGTACGTAGCTA") == pytest.approx(50.0, 0.01), "Failed on CGTACGTAGCTA"

    def test_gc_content_case4(self):
        assert _gc_content("ATATATATATAT") == pytest.approx(0.0, 0.01), "Failed on ATATATATATAT"

    def test_gc_content_case5(self):
        assert _gc_content("GCGCGCGCGCGC") == pytest.approx(100.0, 0.01), "Failed on GCGCGCGCGCGC"

    def test_gc_content_case6(self):
        assert _gc_content("ATGCATGCATGC") == pytest.approx(50.0, 0.01), "Failed on ATGCATGCATGC"

    def test_gc_content_case7(self):
        assert _gc_content("TTTT") == pytest.approx(0.0, 0.01), "Failed on TTTT"

    def test_gc_content_case8(self):
        assert _gc_content("GGGG") == pytest.approx(100.0, 0.01), "Failed on GGGG"

    def test_gc_content_case9(self):
        assert _gc_content("AAAA") == pytest.approx(0.0, 0.01), "Failed on AAAA"

    def test_gc_content_case10(self):
        assert _gc_content("CCCC") == pytest.approx(100.0, 0.01), "Failed on CCCC"

    def test_gc_content_long_sequence(self):
        long_sequence = "A" * 1000000 + "C" * 1000000 + "G" * 1000000 + "T" * 1000000
        assert _gc_content(long_sequence) == pytest.approx(50.0, 0.01), "Failed on long_sequence (1M of each nucleotide)"

    def test_gc_content_another_long_sequence(self):
        long_sequence = "A" * 3333 + "TGC\n"
        assert _gc_content(long_sequence) == pytest.approx(0.06, 0.01), "Failed on long_sequence (1M of each nucleotide)"

    def test_gc_content_empty_sequence(self):
        with pytest.raises(ValueError, match="The sequence cannot be empty."):
            _gc_content("")

class TestCodonFrequency:
    from src.txt_processor import _codon_frequency

    def test_codon_frequency_case1(self):
        sequence = "ATGCGATACGCTT"
        expected_frequency = {
            "ATG": 1,
            "CGA": 1,
            "TAC": 1,
            "GCT": 1
        }
        assert _codon_frequency(sequence) == expected_frequency, f"Failed on {sequence}"

    def test_codon_frequency_case2(self):
        sequence = "ATCGATCG"
        expected_frequency = {
            "ATC": 1,
            "GAT": 1,
        }
        assert _codon_frequency(sequence) == expected_frequency, f"Failed on {sequence}"

    def test_codon_frequency_case3(self):
        sequence = "CGTACGTAGCTA"
        expected_frequency = {
            "CGT": 1,
            "ACG": 1,
            "TAG": 1,
            "CTA": 1
        }
        assert _codon_frequency(sequence) == expected_frequency, f"Failed on {sequence}"

    def test_codon_frequency_case4(self):
        sequence = "ATATATATATAT"
        expected_frequency = {
            "ATA": 2,
            "TAT": 2
        }
        assert _codon_frequency(sequence) == expected_frequency, f"Failed on {sequence}"

    def test_codon_frequency_case5(self):
        sequence = "GCGCGCGCGCGC"
        expected_frequency = {
            "GCG": 2,
            "CGC": 2
        }
        assert _codon_frequency(sequence) == expected_frequency, f"Failed on {sequence}"

    def test_codon_frequency_case6(self):
        sequence = "ATGCATGCATGC"
        expected_frequency = {
            "ATG": 1,
            "CAT": 1,
            "GCA": 1,
            "TGC": 1
        }
        assert _codon_frequency(sequence) == expected_frequency, f"Failed on {sequence}"

    def test_codon_frequency_case7(self):
        sequence = "TTTT"
        expected_frequency = {
            "TTT": 1  
        }
        assert _codon_frequency(sequence) == expected_frequency, f"Failed on {sequence}"

    def test_codon_frequency_case8(self):
        sequence = "GGGG"
        expected_frequency = {
            "GGG": 1 
        }
        assert _codon_frequency(sequence) == expected_frequency, f"Failed on {sequence}"

    def test_codon_frequency_case9(self):
        sequence = "AAAA"
        expected_frequency = {
            "AAA": 1  
        }
        assert _codon_frequency(sequence) == expected_frequency, f"Failed on {sequence}"

    def test_codon_frequency_case10(self):
        sequence = "CCCC"
        expected_frequency = {
            "CCC": 1 
        }
        assert _codon_frequency(sequence) == expected_frequency, f"Failed on {sequence}"

    def test_codon_frequency_long_sequence(self):
        long_sequence = "A" * 333333 + "C" * 333333 + "G" * 333333 + "T" * 333333
        expected_frequency = {
            "AAA": 111111,
            "CCC": 111111,
            "GGG": 111111,
            "TTT": 111111
        }
        assert _codon_frequency(long_sequence) == expected_frequency, "Failed on long_sequence (1M of each nucleotide)"

    def test_codon_frequency_empty_sequence(self):
        with pytest.raises(ValueError, match="The sequence cannot be empty."):
            _codon_frequency("")

class TestMostFrequentCodon:
    from src.txt_processor import _most_frequent_codon

    def test_simple_case(self):
        codon_frequencies = [
            {"ATG": 1, "CGA": 2, "TAC": 1},
            {"CGA": 3, "TGC": 1},
            {"CGA": 1, "ATG": 2, "TAC": 2}
        ]
        expected_most_common = "CGA"  # Appears 6 times in total
        assert _most_frequent_codon(codon_frequencies) == expected_most_common, "Failed on simple case"

    def test_single_codon_frequency(self):
        codon_frequencies = [
            {"ATG": 5, "CGA": 2, "TAC": 1}
        ]
        expected_most_common = "ATG"  # Most frequent in the single dictionary
        assert _most_frequent_codon(codon_frequencies) == expected_most_common, "Failed on single codon frequency"

    def test_multiple_codons_same_frequency(self):
        codon_frequencies = [
            {"ATG": 3, "CGA": 3, "TAC": 2},
            {"TAC": 3, "CGA": 3}
        ]
        expected_most_common = "CGA"  # First codon with the highest frequency
        assert _most_frequent_codon(codon_frequencies) == expected_most_common, "Failed on multiple codons with same frequency"

    def test_empty_frequencies(self):
        codon_frequencies = []
        try:
            _most_frequent_codon(codon_frequencies)
            assert False, "Failed on empty frequencies: Should have raised an error"
        except ValueError as e:
            assert str(e) == "No codon frequencies provided.", "Failed on empty frequencies: Incorrect error message"

    def test_tie_in_frequencies(self):
        codon_frequencies = [
            {"ATG": 2, "CGA": 2},
            {"TAC": 2, "CGA": 2}
        ]
        expected_most_common = "CGA"  # First codon with the highest frequency
        assert _most_frequent_codon(codon_frequencies) == expected_most_common, "Failed on tie in frequencies"

    def test_zero_counts(self):
        codon_frequencies = [
            {"ATG": 0, "CGA": 0, "TAC": 0},
            {"TGC": 0, "CGA": 0}
        ]
        assert _most_frequent_codon(codon_frequencies) == "", "Failed on zero counts"

    def test_large_number_of_frequencies(self):
        codon_frequencies = [
            {"ATG": 1000, "CGA": 2000, "TAC": 1500},
            {"TGC": 3000, "CGA": 2500}
        ]
        expected_most_common = "CGA"  # Most frequent in the combined dictionaries
        assert _most_frequent_codon(codon_frequencies) == expected_most_common, "Failed on large number of frequencies"

class TestLongestCommonSubsequence:
    from src.txt_processor import _longest_common_subsequence

    def test_simple_case_with_one_continuous_subsequence(self):
        seq1 = "ATCGATCGTAGCTAGCTAGCTGATCGATCGAT"
        seq2 = "ATCGGTAAATGCCTGAAAGATG"
        expected_lcs = "ATCG"
        assert _longest_common_subsequence(seq1, seq2) == expected_lcs, "Failed on simple case with one continuous subsequence"

    def test_no_common_continuous_subsequence(self):
        seq1 = "AAAA"
        seq2 = "TTTT"
        expected_lcs = ""
        assert _longest_common_subsequence(seq1, seq2) == expected_lcs, "Failed on no common continuous subsequence"

    def test_one_sequence_is_empty(self):
        seq1 = "ATCG"
        seq2 = ""
        expected_lcs = ""
        assert _longest_common_subsequence(seq1, seq2) == expected_lcs, "Failed on one sequence is empty"

    def test_both_sequences_are_empty(self):
        seq1 = ""
        seq2 = ""
        expected_lcs = ""
        assert _longest_common_subsequence(seq1, seq2) == expected_lcs, "Failed on both sequences are empty"

    def test_entire_sequence_is_common(self):
        seq1 = "ATCG"
        seq2 = "ATCG"
        expected_lcs = "ATCG"
        assert _longest_common_subsequence(seq1, seq2) == expected_lcs, "Failed on entire sequence is common"

    def test_continuous_subsequence_in_the_middle(self):
        seq1 = "GATTACAGTACG"
        seq2 = "TAC"
        expected_lcs = "TAC"
        assert _longest_common_subsequence(seq1, seq2) == expected_lcs, "Failed on continuous subsequence in the middle"

    def test_continuous_subsequence_at_the_start(self):
        seq1 = "ATCGGGG"
        seq2 = "ATC"
        expected_lcs = "ATC"
        assert _longest_common_subsequence(seq1, seq2) == expected_lcs, "Failed on continuous subsequence at the start"

    def test_continuous_subsequence_at_the_end(self):
        seq1 = "GGGGATCG"
        seq2 = "ATCG"
        expected_lcs = "ATCG"
        assert _longest_common_subsequence(seq1, seq2) == expected_lcs, "Failed on continuous subsequence at the end"

    def test_single_character_common_subsequence(self):
        seq1 = "ATCG"
        seq2 = "G"
        expected_lcs = "G"
        assert _longest_common_subsequence(seq1, seq2) == expected_lcs, "Failed on single character common subsequence"

    def test_larger_sequences_with_a_small_common_substring(self):
        seq1 = "A" * 1000000 + "TGC" + "G" * 1000000
        seq2 = "TGC"
        expected_lcs = "TGC"
        assert _longest_common_subsequence(seq1, seq2) == expected_lcs, "Failed on larger sequences with a small common substring"

    def test_overlapping_subsequences_choose_the_longest_continuous_one(self):
        seq1 = "AGTACGCA"
        seq2 = "TACG"
        expected_lcs = "TACG"
        assert _longest_common_subsequence(seq1, seq2) == expected_lcs, "Failed on overlapping subsequences (choose the longest continuous one)"

    def test_two_large_sequences(self):
        seq1 = "A" * 10000 + "C" * 10000 + "G" * 10000 + "T" * 10000
        seq2 = "A" * 10000 + "TGC"
        expected_lcs = "A" * 10000
        assert _longest_common_subsequence(seq1, seq2) == expected_lcs, "Failed on two large sequences"

class TestProcessDNATxtFile:
    from src.txt_processor import process_dna_txt_file

    def write_and_test(self, tmp_path, file_content: str, expected_output: dict, case_name: str):
        """
        Helper function to write a file and run the test.
        """
        # Create a temporary file in the provided tmp_path
        file_path = tmp_path / "dna_sequences.txt"
        file_path.write_text(file_content)

        # Run the test and compare the result with the expected output
        assert process_dna_txt_file(file_path) == expected_output, f"Failed on {case_name}"

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
                "most_common_codon": "GAT",
                "lcs": {
                    "value": "ATCG",
                    "sequences": [1, 2],
                    "length": 4,
                },
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
                "most_common_codon": "GAT",
                "lcs": {
                    "value": "",
                    "sequences": [],
                    "length": 0,
                },
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
                "most_common_codon": "ATC",  # Could also be "CGA" or "TCG"
                "lcs": {
                    "value": "ATCGATCG",
                    "sequences": [1, 2],
                    "length": 8,
                },
            },
            case_name="All identical sequences",
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
                "most_common_codon": "AAA",  # Most frequent codon
                "lcs": {
                    "value": "A" * 3333 + "TGC",
                    "sequences": [1, 2],
                    "length": 3336,
                },
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
                "most_common_codon": "AAA",  # Most frequent codon
                "lcs": {
                    "value": "A" * 3333,
                    "sequences": [1, 2],
                    "length": 3333,
                },
            },
            case_name="Another long sequence",
        )