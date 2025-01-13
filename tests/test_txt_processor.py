import pytest
import os
 
def test_gc_content():
    from src.txt_processor import _gc_content
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
