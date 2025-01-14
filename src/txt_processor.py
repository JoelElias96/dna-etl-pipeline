from itertools import combinations
from collections import defaultdict

def _gc_content(sequence: str) -> float:
    """
    Calculate the GC content of a DNA sequence (private function).
    The GC content is the percentage of nucleotides in the DNA sequence
    that are either Guanine ('G') or Cytosine ('C').

    Args:
        sequence (str): A string representing a DNA sequence. The sequence
                        is expected to contain only 'A', 'T', 'G', and 'C'.
    Returns:
        float: The GC content as a percentage of the sequence.
    Raises:
        ValueError: If the input sequence is empty.
    """
    # Check if the sequence is empty and raise an error if it is
    if not sequence:
        raise ValueError("The sequence cannot be empty.")

    # Count the number of 'G' and 'C' in the sequence
    gc_count = 0
    for base in sequence:
        if base == 'G' or base == 'C':
            gc_count += 1

    # Calculate the GC content as a percentage of the total sequence length
    return round((gc_count / len(sequence)) * 100,2)

def _codon_frequency(sequence: str) -> dict:
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

def _most_frequent_codon(codon_freqs: list) -> str:
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

def _longest_common_subsequence(word1: str, word2: str) -> str:
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

def _process_txt_file(file_path: str) -> dict:
    """
    Process a TXT file containing DNA sequences.
    
    Args:
        file_path (str): Path to the TXT file.
    
    Returns:
        dict: Processed data including GC content, codon frequencies, most common codon, and LCS.
    """
    # Open the file and read all lines, stripping whitespace and ignoring empty lines
    with open(file_path, 'r') as file:
        sequences = [line.strip() for line in file.readlines() if line.strip()]
    
    # Check if there are no valid sequences and raise an error if true
    if len(sequences) == 0:
        raise ValueError("No valid DNA sequences found in the file.")
    
    sequence_data = []
    codon_frequencies = []
    
    # Process each sequence to calculate GC content and codon frequencies
    for seq in sequences:
        try:
            gc_content = _gc_content(seq)
            codon_freq = _codon_frequency(seq)
            sequence_data.append({"gc_content": gc_content, "codons": codon_freq})
            codon_frequencies.append(codon_freq)
        except ValueError as e:
            continue
    
    # Determine the most common codon across all sequences
    most_common_codon = _most_frequent_codon(codon_frequencies)
    
    lcs = ""
    lcs_sequences = []
    # If there are multiple sequences, find the longest common subsequence (LCS)
   
    if len(sequences) > 1:
        lcs_sequences = []
        for i, j in combinations(range(len(sequences)), 2):  # Iterate over indices
            seq1, seq2 = sequences[i], sequences[j]
            lcs_candidate = _longest_common_subsequence(seq1, seq2)
            if len(lcs_candidate) > len(lcs):
                lcs = lcs_candidate
                # Store the 1-based indices of the first pair with the longest LCS
                lcs_sequences = [i + 1, j + 1]
            
    
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

def process_dna_txt_file(file_path: str) -> dict:
    """
    Process a TXT file containing DNA sequences.

    This function analyzes DNA sequences from a TXT file, performing the following steps:
    1. Calculate GC content and codon frequencies for each sequence.
    2. Identify the most common codon across all sequences.
    3. Determine the longest continuous common subsequence (LCS) between sequences (if multiple exist).

    Args:
        file_path (str): Path to the TXT file containing DNA sequences.

    Returns:
        dict: A dictionary with:
            - `"sequences"`: List of GC content and codon frequency data for each sequence.
            - `"most_common_codon"`: The most frequently occurring codon.
            - `"lcs"`: The longest common subsequence, its length, and contributing sequences.

    Raises:
        FileNotFoundError: If the file is not found.
        ValueError: If the file contains no valid DNA sequences.
        Exception: For any other processing errors.

    Example:
        Input file (`dna_sequences.txt`):
            ATGCGTACG
            GCGTACGAT

        Output:
            {
                "sequences": [
                    {"gc_content": 55.56, "codons": {"ATG": 1, "CGT": 1, "ACG": 1}},
                    {"gc_content": 66.67, "codons": {"GCG": 1, "TAC": 1, "GAT": 1}}
                ],
                "most_common_codon": "GCG",
                "lcs": {
                    "value": "GCGTAC",
                    "sequences": [1, 2],
                    "length": 6
                }
            }
    """
    try:
        return _process_txt_file(file_path)
    except FileNotFoundError:
        raise FileNotFoundError("The specified file was not found.")
    except Exception as e:
        raise Exception(f"An error occurred while processing the file: {str(e)}")