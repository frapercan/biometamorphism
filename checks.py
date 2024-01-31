import pandas as pd
import tmtools
from Bio import PDB
import os
from Bio.PDB import CEAligner

# Define the ChainSelect class
class ChainSelect(PDB.Select):
    def __init__(self, chain_id, model_id=0):
        self.chain_id = chain_id
        self.model_id = model_id

    def accept_chain(self, chain):
        return chain.get_id() == self.chain_id

    def accept_model(self, model):
        return model.get_id() == self.model_id

def perform_ce_alignment(ref_chain, target_chain):
    aligner = CEAligner(window_size=4)
    ref_structure = PDB.Structure.Structure(id="ref")
    target_structure = PDB.Structure.Structure(id="target")
    ref_model = PDB.Model.Model(0)
    target_model = PDB.Model.Model(0)
    ref_model.add(ref_chain)
    target_model.add(target_chain)
    ref_structure.add(ref_model)
    target_structure.add(target_model)

    aligner.set_reference(ref_structure)
    aligner.align(target_structure)
    print(ref_structure.get_chains())
    # tmtools.tm_align(ref_structure, target_structure)
    return aligner.rms

def process_data(df, output_dir, pdb_directory):
    pdbl = PDB.PDBList(server="https://files.wwpdb.org/", pdb=pdb_directory)
    pdb_parser = PDB.MMCIFParser()
    io = PDB.MMCIFIO()

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cealign_rms_values = []
    for index, row in df.iterrows():
        pdb_id_1, chain_id_1 = row['pdb_id'], row['chains']
        pdb_id_2, chain_id_2 = row['rep_pdb_id'], row['rep_chains']
        structures = []

        for pdb_id, chain_id in [(pdb_id_1, chain_id_1), (pdb_id_2, chain_id_2)]:
            pdbl.retrieve_pdb_file(pdb_id, file_format="mmCif", pdir=pdb_directory, overwrite=True)
            cif_file = os.path.join(pdb_directory, f"{pdb_id.lower()}.cif")
            structure = pdb_parser.get_structure(pdb_id, cif_file)
            chain = structure[0][chain_id]
            structures.append(chain)

        alignment = perform_ce_alignment(structures[0], structures[1])
        cealign_rms_values.append(alignment)

    print("Processing complete.")
    return cealign_rms_values

# Path configuration
csv_file_path = './data/metamorfismos_previos.csv'
csv_file_path_result = './data/metamorfismos_result.csv'
pdb_directory = './pdb/'
output_directory = './chains/'

# Load the CSV file
metamorphisms = pd.read_csv(csv_file_path)

# Process the data and get CE alignment RMS values
cealign_rms_values = process_data(metamorphisms, output_directory, pdb_directory)

# Add the new column to the DataFrame and save it back to CSV
metamorphisms['cealign_rms'] = cealign_rms_values
metamorphisms.to_csv(csv_file_path_result, index=False)
