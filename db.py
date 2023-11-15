from Bio.PDB import PDBList

# Crear una instancia de PDBList
pdb_list = PDBList()

# Obtener la lista de índices del PDB
pdb_indices = pdb_list.get_all_entries()

pdb_list.download_pdb_files(pdb_indices[:500],pdir='./data')
# Imprimir los índices
print(len(pdb_indices))





