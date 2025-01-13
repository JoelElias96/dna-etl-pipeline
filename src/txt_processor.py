from itertools import combinations

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
    gc_count = sequence.count('G') + sequence.count('C')

    # Calculate the GC content as a percentage of the total sequence length
    return (gc_count / len(sequence)) * 100

def _codon_frequency(sequence : str) -> dict:
    """
    Calculate the frequency of codons in a DNA sequence (private function).

    A codon is a triplet of nucleotides. This function iterates through the
    DNA sequence in steps of three and counts the occurrence of each codon.
    The last one or two nucleotides are ignored if the sequence length is
    not divisible by three.
   
    Args:
        sequence (str): A string representing a DNA sequence. The sequence
                        is expected to contain only 'A', 'T', 'G', and 'C'.
    Returns:
        dict: A dictionary where keys are codons (triplets of nucleotides)
              and values are their frequencies in the sequence.
    Raises:
        ValueError: If the input sequence is empty.
    """
    if not sequence:
        raise ValueError("The sequence cannot be empty.")

    # Initialize an empty dictionary to store codon frequencies
    codon_freq = {}

    # Iterate through the sequence in steps of three to extract codons
    for i in range(0, len(sequence) - len(sequence) % 3, 3):
        codon = sequence[i:i+3]
        if codon in codon_freq:
            codon_freq[codon] += 1
        else:
            codon_freq[codon] = 1

    return codon_freq

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
    """
    combined_freq = {}
    # Combine frequencies from all dictionaries
    for freq in codon_freqs:
        for codon, count in freq.items():
            if codon in combined_freq:
                combined_freq[codon] += count
            else:
                combined_freq[codon] = count
    # Return the codon with the highest frequency
    return max(combined_freq, key=combined_freq.get)

def _longest_common_subsequence(word1: str, word2: str) -> str:
    """
    Find the longest continuous common subsequence (substring) between two strings (private function).

    This function uses dynamic programming to find the longest continuous common subsequence
    between two strings. It constructs a matrix to store the length of the longest
    continuous subsequence between prefixes of the two strings.

    Args:
        word1 (str): The first input string.
        word2 (str): The second input string.
    Returns:
        str: The longest continuous common subsequence between the two input strings.
    """
    if not word1 or not word2:
        return ""

    n = len(word1)
    m = len(word2)

    # Initialize the DP table with zeros
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    max_length = 0
    end_index = 0

    # Fill the DP table
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > max_length:
                    max_length = dp[i][j]
                    end_index = i
            else:
                dp[i][j] = 0

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
        for seq1, seq2 in combinations(sequences, 2):
            lcs_candidate = _longest_common_subsequence(seq1, seq2)
            if len(lcs_candidate) > len(lcs):
                lcs = lcs_candidate
                lcs_sequences = [sequences.index(seq1) + 1, sequences.index(seq2) + 1]
            elif len(lcs_candidate) == len(lcs):
                lcs_sequences.extend([sequences.index(seq1) + 1, sequences.index(seq2) + 1])
                lcs_sequences = list(set(lcs_sequences))
    
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
    
    Args:
        file_path (str): Path to the TXT file.

    Returns:
        dict: Processed data including GC content, codon frequencies, most common codon, and LCS.
    """
    try:
        return _process_txt_file(file_path)
    except FileNotFoundError:
        raise FileNotFoundError("The specified file was not found.")
    except Exception as e:
        raise Exception(f"An error occurred while processing the file: {str(e)}")