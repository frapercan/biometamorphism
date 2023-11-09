from Bio import SeqIO

PDB_file_path = 'C:/Users/frape\PycharmProjects/biometamorphism/data/pdb1cee.ent'

# Is there a 1-liner for this ?
query_seqres = SeqIO.parse(PDB_file_path, 'pdb-seqres')

for chain in query_seqres:
    if chain.id == '1CEE:B':
        query_chain = chain.seq

