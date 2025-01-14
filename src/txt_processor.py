from itertools import combinations
from collections import defaultdict

class TXTProcessor:

    def __init__(self, file_path: str):
        self.file_path = file_path

    def process(self) -> dict:
        """
        Processes DNA sequences to compute various metrics and statistics.
        This method performs the following operations:
        1. Loads DNA sequences.
        2. Computes the GC content and codon frequency for each sequence.
        3. Determines the most common codon across all sequences.
        4. Computes the longest common subsequence (LCS) among all sequences.
        Returns:
            dict: A dictionary containing the following keys:
                - "sequences" (list): A list of dictionaries, each containing:
                - "gc_content" (float): The GC content of the sequence.
                - "codons" (dict): A dictionary with codon frequencies.
            - "most_common_codon" (str): The most frequently occurring codon across all sequences.
            - "lcs" (dict): A dictionary containing:
                - "value" (str): The longest common subsequence.
                - "sequences" (list): The sequences that contain the LCS.
                - "length" (int): The length of the LCS.
        Raises:
            ValueError: If no valid DNA sequences are found in the file.
            ValueError: If a sequence is empty when calculating GC content or codon frequency.
            ValueError: If no codon frequencies are provided when determining the most frequent codon.
        """
        # Load sequences from the file
        sequences = self._load_sequences()
        sequence_data = []
        codon_frequencies = []

        # Process each sequence, if its not valid, skip it
        for seq in sequences:
            try:
                gc_content = self._gc_content(seq)
                codon_freq = self._codon_frequency(seq)
                sequence_data.append({"gc_content": gc_content, "codons": codon_freq})
                codon_frequencies.append(codon_freq)
            except ValueError as e:
                continue
    
        # Determine the most common codon across all sequences
        most_common_codon = self._most_frequent_codon(codon_frequencies)

        # Compute the longest common subsequence (LCS) among all sequences
        lcs, lcs_sequences = self._longest_common_subsequence_among_all(sequences)
    
        # Return the processed data as a dictionary
        return {
            "sequences": sequence_data,
            "most_common_codon": most_common_codon,
            "lcs": {
                "value": lcs,
                "sequences": lcs_sequences,
                "length": len(lcs)
            }
        }

    def _load_sequences(self) -> list:
        """
    Loads DNA sequences from a file.
    This method reads the file specified by `self.file_path`, processes each line to remove
    any leading or trailing whitespace, and filters out any empty lines. It returns a list
    of non-empty DNA sequences.
    Returns:
        list: A list of DNA sequences read from the file.
    Raises:
        ValueError: If no valid DNA sequences are found in the file.
    """
        with open(self.file_path, 'r') as file:
            sequences = [line.strip() for line in file.readlines() if line.strip()]
        if not sequences:
            raise ValueError("No valid DNA sequences found in the file.")
        return sequences

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
        return round((gc_count / len(sequence)) * 100,2)

    def _codon_frequency(self, sequence: str) -> dict:
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

    def _most_frequent_codon(self, codon_freqs: list) -> str:
        """
        Find the most frequent codon among a list of codon frequency dictionaries.

        This function takes a list of dictionaries where keys are codons and values
        are their frequencies. It combines the frequencies of each codon from all
        dictionaries and returns the codon with the highest frequency.

        Args:   
            codon_freqs (list): A list of dictionaries where keys are codons and
                                values are their frequencies.
        Returns:
            str: The codon with the highest frequency among all dictionaries.
    
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
        # Return the codon with the highest frequency
        return "" if  max(combined_freq.values()) == 0 else max(combined_freq, key=combined_freq.get)

    def _longest_common_subsequence_among_all(self, sequences: list) -> tuple:
        """
        Finds the longest common subsequence (LCS) among a list of sequences.
        This method compares all pairs of sequences in the input list and determines the longest common subsequence
        shared by any two sequences. It returns the LCS and the indices of the sequences that contain this LCS.
        Args:
            sequences (list): A list of sequences (strings) to be compared.
        Returns:
            tuple: A tuple containing:
            -str: The longest common subsequence found.
            -list: A list of two integers representing the 1-based indices of the sequences that contain the LCS.
        Notes:
            - If the input list contains fewer than two sequences, the method returns an empty string and an empty list.
            - The method assumes that the input sequences are non-empty strings.
        """
       
        if len(sequences) < 2:
            return "", []

        lcs = ""
        lcs_sequences = []
        for i, j in combinations(range(len(sequences)), 2):
            lcs_candidate = self._lcs_between_two(sequences[i], sequences[j])
            if len(lcs_candidate) > len(lcs):
                lcs = lcs_candidate
                lcs_sequences = [i + 1, j + 1]
        return lcs, lcs_sequences

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
        # TODO: Try to optimize this function further for large strings
        if not word1 or not word2:
            return ""

        n, m = len(word1), len(word2)

        # Use a rolling array to optimize space complexity
        prev = [0] * (m + 1)
        curr = [0] * (m + 1)

        max_length = 0
        end_index = 0

        for i in range(1, n + 1):
            for j in range(1, m + 1):
                if word1[i - 1] == word2[j - 1]:
                    curr[j] = prev[j - 1] + 1
                    if curr[j] > max_length:
                        max_length = curr[j]
                        end_index = i
                else:
                    curr[j] = 0
            # Swap rows: the current row becomes the previous row for the next iteration
            prev, curr = curr, prev

        # Extract the longest common substring
        longest_common_substring = word1[end_index - max_length:end_index]
        return longest_common_substring