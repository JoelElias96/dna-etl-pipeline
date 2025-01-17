from itertools import combinations
from collections import defaultdict
from pipeline.processors.file_processor import AbstractFileProcessor
from typing import List, Dict
import logging


class DNASequenceTxtProcessor (AbstractFileProcessor):
    """
    TXTProcessor is a class for processing DNA sequences from a text file to compute various metrics and statistics.
    This class inherits from AbstrctFileProcessor and provides methods to:
    1. Load DNA sequences from a file.
    2. Compute the GC content and codon frequency for each sequence.
    3. Determine the most common codons across all sequences.
    4. Compute the longest common subsequence (LCS) among all sequences.
    Attributes:
        file_path (str): The path to the file containing DNA sequences.
    Methods:
        process() -> dict:
            Returns a dictionary containing the processed data.
        _load_sequences() -> list:
            Loads DNA sequences from a file and returns a list of non-empty sequences.
        _gc_content(sequence: str) -> float:
            Calculates the GC content of a DNA sequence.
        _codon_frequency(sequence: str) -> dict:
            Calculates the frequency of each codon in a given DNA sequence.
        _most_frequent_codons(codon_freqs: list) -> list:
            Finds the most frequent codons among a list of codon frequency dictionaries.
        _longest_common_subsequence_among_all(sequences: list) -> tuple:
        _lcs_between_two(word1: str, word2: str) -> str:
            Finds the longest continuous common subsequence (substring) between two strings.
    """

    def __init__(self, file_path: str):
        """
        Initialize the DNASequenceTxtProcessor with the given file path.
        Args:
            file_path (str): The path to the file containing DNA sequences.
        """
        super().__init__(file_path)
        self.dna_sequences = []

    def process(self) -> Dict:
        """
        Processes DNA sequences to compute various metrics and statistics.
        This method performs the following operations:
        1. Loads DNA sequences.
        2. Computes the GC content and codon frequency for each sequence.
        3. Determines the most common codons across all sequences.
        4. Computes the longest common subsequence (LCS) among all sequences.
        Returns:
            dict: A dictionary containing the following keys:
                - "sequences" (list): A list of dictionaries, each containing:
                - "gc_content" (float): The GC content of the sequence.
                - "codons" (dict): A dictionary with codon frequencies.
            - "most_common_codon" (list): The most frequently occurring codon across all sequences.
            - "lcs" (dict): A dictionary containing:
                - "value" (str): The longest common subsequence.
                - "sequences" (list): The sequences that contain the LCS.
                - "length" (int): The length of the LCS.
        Raises:
            ValueError: If no valid DNA sequences are found in the file.
            ValueError: If a sequence is empty when calculating GC content or codon frequency.
            ValueError: If no codon frequencies are provided when determining the most frequent codon.
            logging.error: If an error occurs while processing a sequence.
        """
        # Load sequences from the file
        try:
            self._load_sequences()
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.file_path}")
        except ValueError as e:
            raise ValueError(f"Invalid data in file: {str(e)}")

        sequences_data = []
        codon_frequencies = []

        # Process each sequence, if its not valid, skip it
        for seq in self.dna_sequences:
            try:
                gc_content = self._gc_content(seq)
                codon_freq = self._codon_frequency(seq)
                sequences_data.append({"gc_content": gc_content, "codons": codon_freq})
                codon_frequencies.append(codon_freq)
            except ValueError as e:
                logging.error(f"Error processing sequence {seq}: {e}")
                continue

        # Determine the most common codon across all sequences
        most_common_codon = self._most_frequent_codons(codon_frequencies)

        # Compute the longest common subsequence (LCS) among all sequences
        lcs = self._longest_common_subsequence_among_all()

        # Return the processed data as a dictionary
        return {
            "sequences": sequences_data,
            "most_common_codon": most_common_codon,
            "lcs": lcs
        }

    def _load_sequences(self) -> List:
        """
    Loads DNA sequences from a file.
    This method reads the file specified by `self.file_path`, processes each line to remove
    any leading or trailing whitespace, and filters out any empty lines. It returns a list
    of non-empty DNA sequences.

    Raises:
        ValueError: If no valid DNA sequences are found in the file.
    """
        with open(self.file_path, 'r') as file:
            self.dna_sequences = [line.strip() for line in file.readlines() if line.strip()]
        if not self.dna_sequences:
            raise ValueError("No valid DNA sequences found in the file.")

    def _gc_content(self, sequence: str) -> float:
        """
        Calculate the GC content of a DNA sequence.
        The GC content is the percentage of bases in the sequence that are either
        guanine (G) or cytosine (C).
        Args:
            sequence (str): A string representing the DNA sequence.
        Returns:
            float: The GC content of the sequence as a percentage, rounded to two decimal places.
        """
        if not sequence:
            raise ValueError("The sequence cannot be empty.")

        gc_count = 0

        # Count the number of G and C bases in the sequence
        for base in sequence:
            if base == 'G' or base == 'C':
                gc_count += 1

        # Calculate the GC content as a percentage of the total sequence length
        return round((gc_count / len(sequence)) * 100, 2)

    def _codon_frequency(self, sequence: str) -> Dict:
        """
        Calculate the frequency of each codon in a given DNA sequence.
        A codon is a sequence of three nucleotides. This function counts the
        occurrences of each codon in the provided DNA sequence and returns a
        dictionary with codons as keys and their frequencies as values.
        Args:
            sequence (str): A string representing the DNA sequence. The length
                        of the sequence should be a multiple of 3.
        Returns:
             dict: A dictionary where keys are codons (str) and values are their
                respective frequencies (int).
        Raises:
            ValueError: If the input sequence is empty.
        """
        # Check if the sequence is empty and raise an error if it is
        if not sequence:
            raise ValueError("The sequence cannot be empty.")

        # Initialize a defaultdict to count codon frequencies
        codon_freq = defaultdict(int)

        # Iterate over the sequence in steps of 3 to count each codon
        for i in range(0, len(sequence) - len(sequence) % 3, 3):
            codon_freq[sequence[i:i+3]] += 1

        # Convert the defaultdict to a regular dictionary and return it
        return dict(codon_freq)

    def _most_frequent_codons(self, codon_freqs: List) -> List:
        """
        Find the most frequent codons among a list of codon frequency dictionaries.

        This function takes a list of dictionaries where keys are codons and values
        are their frequencies. It combines the frequencies of each codon from all
        dictionaries and returns a list of codons with the highest frequency.

        Args:
            codon_freqs (list): A list of dictionaries where keys are codons and
                                 values are their frequencies.
        Returns:
            list: A list of codons with the highest frequency among all dictionaries.

        Raises:
            ValueError: If the input list is empty or contains empty dictionaries.
        """
        if not codon_freqs:
            raise ValueError("No codon frequencies provided.")

        combined_freq = {}
        # Combine frequencies from all dictionaries
        for freq in codon_freqs:
            if not freq:
                continue
            for codon, count in freq.items():
                if codon in combined_freq:
                    combined_freq[codon] += count
                else:
                    combined_freq[codon] = count

        # Find the maximum frequency
        max_freq = max(combined_freq.values(), default=0)

        # Return a list of codons with the highest frequency
        return [codon for codon, count in combined_freq.items() if count == max_freq]

    def _longest_common_subsequence_among_all(self) -> List:
        """
       Finds the longest common subsequences (LCS) among a list of DNA sequences.
        This method compares all pairs of sequences in the input list and determines the longest common subsequences
        shared by any two sequences. It returns a list of dictionaries, each containing the LCS value,
        the associated sequences (indices), and the length of the LCS.

        The function compares each pair of sequences to find the longest common subsequence between them.
        If a subsequence is the longest found so far, it updates the dictionary. If a subsequence has the same length
        as the longest found so far, the function adds the pair of sequences to the dictionary.

        The final result is a list of dictionaries,
        each representing a longest common subsequence with the following keys:
            - "value" (str): The LCS itself.
            - "sequences" (list): A list of unique sequence indices (1-based) that share this LCS.
            - "length" (int): The length of the LCS.

        Args:
            None

        Returns:
            List: A list of dictionaries where each dictionary contains:
                - "value" (str): The LCS value (subsequence).
                - "sequences" (list): A list of unique sequence indices that contain this LCS.
                - "length" (int): The length of the LCS.

        Raises:
            ValueError: If there are fewer than two sequences to compare.

        """

        def _processe_lcs_dict(lcs_dict: Dict) -> Dict:
            """
            Processes the LCS dictionary and transforms it into a specific format.

            Args:
                lcs_dict (dict): A dictionary with LCS as keys and a list of sequence indices as values.

            Returns:
                dict: A list of dictionaries, each containing the LCS, associated sequences, and the LCS length.
            """
            result = []

            for lcs, sequences in lcs_dict.items():
                # Remove duplicate sequence indices
                unique_sequences = list(set(sequences))

                result.append({
                                "value": lcs,
                                "sequences": unique_sequences,
                                "length": len(lcs)
                            })

            return result

        if len(self.dna_sequences) < 2:
            return []

        lcs_dict = {}
        max_len = 0

        for i, j in combinations(range(len(self.dna_sequences)), 2):

            # Find the LCS between the two sequences
            lcs_candidate = self._lcs_between_two(self.dna_sequences[i], self.dna_sequences[j])

            # Update the LCS dictionary if a longer LCS is found
            if len(lcs_candidate) > max_len:
                max_len = len(lcs_candidate)
                lcs_dict = {lcs_candidate: [i + 1, j + 1]}

            # If the LCS has the same length as the max found so far, append to the dictionary
            elif len(lcs_candidate) == max_len:
                if lcs_candidate in lcs_dict:
                    lcs_dict[lcs_candidate].extend([i + 1, j + 1])
                else:
                    lcs_dict[lcs_candidate] = [i + 1, j + 1]

        # If no LCS is found, return an empty list
        if max_len == 0:
            return []
        return _processe_lcs_dict(lcs_dict)

    def _lcs_between_two(self, word1: str, word2: str) -> str:
        """
        Find the longest continuous common subsequence (substring) between two strings (private function).

        This function uses dynamic programming to find the longest continuous common subsequence
        between two strings. It uses a rolling array to optimize space usage.

        Args:
            word1 (str): The first input string.
            word2 (str): The second input string.
        Returns:
            str: The longest continuous common subsequence between the two input strings.
        """
        # If either input string is empty, return an empty string
        if not word1 or not word2:
            return ""

        n, m = len(word1), len(word2)

        # Use a rolling array to optimize space complexity
        prev = [0] * (m + 1)
        curr = [0] * (m + 1)

        max_length = 0
        end_index = 0
        # Iterate over each character in word1 and word2
        for i in range(1, n + 1):
            for j in range(1, m + 1):

                # If characters match, update the current cell with the value from the previous diagonal cell + 1
                if word1[i - 1] == word2[j - 1]:

                    curr[j] = prev[j - 1] + 1
                    # Update max_length and end_index if a longer common substring is found
                    if curr[j] > max_length:
                        max_length = curr[j]
                        end_index = i
                else:
                    # If characters do not match, reset the current cell to 0
                    curr[j] = 0
            # Swap rows: the current row becomes the previous row for the next iteration
            prev, curr = curr, prev

        # Extract the longest common substring
        longest_common_substring = word1[end_index - max_length:end_index]
        return longest_common_substring
