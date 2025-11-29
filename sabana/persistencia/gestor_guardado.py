import pickle
import json
import os
import shutil
from datetime import datetime

class Gestor_Guardado:
    def __init__(self):
        # Obtenemos la ruta donde está este archivo (gestor_guardado.py)
        ruta_base = os.path.dirname(__file__) 
        self.carpeta_guardado = os.path.join(ruta_base, "partidas_guardadas")
        
        # Si la carpeta no existe, la crea
        if not os.path.exists(self.carpeta_guardado):
            os.makedirs(self.carpeta_guardado)

    def _ruta_archivo(self, nombre_slot, extension):
        return os.path.join(self.carpeta_guardado, f"{nombre_slot}.{extension}")

    def guardar_partida(self, nombre_slot, datos_modelo, metadatos):
        ruta_pickle = self._ruta_archivo(nombre_slot, "pkl")
        ruta_json = self._ruta_archivo(nombre_slot, "json")

        # 1. Sistema de Backups automaticos
        if os.path.exists(ruta_pickle):
            shutil.copy(ruta_pickle, ruta_pickle + ".bak")
        if os.path.exists(ruta_json):
            shutil.copy(ruta_json, ruta_json + ".bak")

        # 2. Guardado
        try:
            # Guardamos los objetos (animales, comidas, etc)
            with open(ruta_pickle, "wb") as f:
                pickle.dump(datos_modelo, f)
            
            # Guardamos la fecha y datos resumen
            metadatos["fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(ruta_json, "w") as f:
                json.dump(metadatos, f, indent=4)
            
            return True, "Guardado exitoso"
        except Exception as e:
            return False, f"Error al guardar: {str(e)}"

    def cargar_partida(self, nombre_slot):
        ruta_pickle = self._ruta_archivo(nombre_slot, "pkl")
        
        if not os.path.exists(ruta_pickle):
            return None, "El archivo no existe"

        try:
            with open(ruta_pickle, "rb") as f:
                datos = pickle.load(f)
            return datos, "Carga exitosa"
        except Exception:
            # Si el archivo principal falla, buscamos el backup
            ruta_backup = ruta_pickle + ".bak"
            if os.path.exists(ruta_backup):
                try:
                    with open(ruta_backup, "rb") as f:
                        datos = pickle.load(f)
                    return datos, "Archivo dañado. Se cargo el respaldo"
                except:
                    return None, "Archivo y respaldo dañados"
            return None, "Archivo dañado y sin respaldo"

    def listar_partidas(self):
        partidas = []
        if not os.path.exists(self.carpeta_guardado):
            return partidas

        for archivo in os.listdir(self.carpeta_guardado):
            if archivo.endswith(".json"):
                nombre_slot = archivo.replace(".json", "")
                ruta_json = os.path.join(self.carpeta_guardado, archivo)
                try:
                    with open(ruta_json, "r") as f:
                        meta = json.load(f)
                    partidas.append({"slot": nombre_slot, "info": meta})
                except:
                    continue
        return partidas