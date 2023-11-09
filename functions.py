from Bio import pairwise2, PDB, SeqIO


def get_sequence_and_metadata(pdb_id, chain_id, columns):
    pdbl = PDB.PDBList()
    pdb_parser = PDB.PDBParser()

    # Download PDB file (or use fetch if the file is already downloaded)
    pdb_file = pdbl.retrieve_pdb_file(pdb_id, pdir='./data/', file_format='pdb')
    structure = pdb_parser.get_structure(pdb_id, pdb_file)

    # Access the header of the PDB file
    header = structure.header

    # Fetch the specified metadata
    metadata_values = {column: header.get(column, None) for column in columns}

    # Extract the sequence of the specified chain
    query_seqres = SeqIO.parse(pdb_file, 'pdb-seqres')
    for chain in query_seqres:
        print(chain.id)
        print(f'{pdb_id}:{chain_id}')
        print(chain.seq)
        if chain.id == f'{pdb_id}:{chain_id}':
            sequence = chain.seq
            break




    # Return both the sequence and the metadata
    return sequence, metadata_values

def add_sequence_and_metadata(row, pair, metadata_fields):
    sequence, metadata = get_sequence_and_metadata(row[f"PDB_{pair}"], row[f"Chain_{pair}"], metadata_fields)

    row[f"Sequence_{pair}"] = sequence

    for field in metadata_fields:
        row[f"{field}_{pair}"] = metadata.get(field, None)
    return row






def calculate_distance(seq1, seq2):
    # Perform a global alignment using a simple scoring method
    alignments = pairwise2.align.globalxx(seq1, seq2)

    # Take the highest-scoring alignment
    top_alignment = alignments[0]

    # Calculate the distance score based on the number of mismatches and gaps
    score = top_alignment[2]  # This is the alignment score
    length = top_alignment[4]  # This is the end position of the alignment

    return score

def calculate_identity(seq1, seq2):
    # Perform a global alignment using a simple scoring method
    alignments = pairwise2.align.globalxx(seq1, seq2)

    # Take the highest-scoring alignment
    top_alignment = alignments[0]

    # Alignment is returned as a tuple (seqA, seqB, score, begin, end)
    aligned_seq1, aligned_seq2, score, begin, end = top_alignment

    # Calculate matches and the length of the alignment
    matches = sum(res1 == res2 for res1, res2 in zip(aligned_seq1[begin:end], aligned_seq2[begin:end]))
    alignment_length = end - begin

    # Calculate the percentage of identity
    identity_percentage = (matches / alignment_length) * 100

    return identity_percentage

