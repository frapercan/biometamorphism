from Bio.PDB import MMCIFParser
from tmtools.io import get_residue_data

parser = MMCIFParser()
structure = parser.get_structure(structure_id='hola',filename='./chains/1AP8_chain_A.cif')

chain = next(structure.get_chains())

print(chain)

coords, seq = get_residue_data(chain)
print(coords)
print(seq)