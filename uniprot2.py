from Bio import ExPASy
from Bio import SwissProt
import requests
from urllib.parse import quote

def descargar_ids_proteinas(criterio_busqueda):
    criterio_busqueda_codificado = quote(criterio_busqueda)
    url = f"https://rest.uniprot.org/uniprotkb/stream?query={criterio_busqueda_codificado}&format=list"
    print(url)
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        ids = respuesta.text.strip().split('\n')
        return ids
    except Exception as e:
        print(f"Error al descargar datos: {e}")
        return []
def descargar_uniprot(ids):
    """ Descarga entradas de UniProt dado un conjunto de IDs de UniProt. """
    for uniprot_id in ids:
        try:
            handle = ExPASy.get_sprot_raw(uniprot_id)

            record = SwissProt.read(handle)
            print("keys:", record.__dict__)
        except Exception as e:
            print(f"Error al descargar la entrada {uniprot_id}: {e}")

# Lista de IDs de UniProt para descargar
uniprot_ids = descargar_ids_proteinas(criterio_busqueda='(structure_3d:true) AND (reviewed:true)')[:5]  # Reemplaza con los IDs de tu interés


descargar_uniprot(uniprot_ids)