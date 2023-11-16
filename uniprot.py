import sys

from urllib.parse import quote
import pprint
import requests


def descargar_informacion_proteina(id_proteina):
    url = f"https://rest.uniprot.org/uniprotkb/{id_proteina}.json"
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        return respuesta.json()
    except Exception as e:
        print(f"Error al descargar información de la proteína {id_proteina}: {e}")
        return None

def obtener_numero_estructuras(info_proteina):
    # Esta función debe analizar la información de la proteína para encontrar el número de estructuras
    # Debes ajustar esta función según el formato exacto de la respuesta de UniProt
    # Por ejemplo, si las estructuras están en info_proteina['estructuras']:
    pdb_entries = [entry for entry in info_proteina['uniProtKBCrossReferences'] if entry['database'] == 'PDB']
    print(len(pdb_entries))
    return len(pdb_entries)

def descargar_ids_proteinas(criterio_busqueda, limite):
    criterio_busqueda_codificado = quote(criterio_busqueda)
    url = f"https://rest.uniprot.org/uniprotkb/stream?query={criterio_busqueda_codificado}&format=list&size={limite}"
    print(url)
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        ids = respuesta.text.strip().split('\n')
        return ids
    except Exception as e:
        print(f"Error al descargar datos: {e}")
        return []

# Descargar IDs de proteínas
criterio = '(structure_3d:true) AND (reviewed:true)'
limite = 10
ids_proteinas = descargar_ids_proteinas(criterio, limite)



