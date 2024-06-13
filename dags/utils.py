from datetime import datetime
import os

def existe_entorno()->str:

	return "entorno.entorno_creado" if os.path.exists(os.path.join(os.getcwd(), "dags", "entorno")) else "entorno.carpeta_logs"

def vaciarCarpeta(ruta:str)->None:

	if os.path.exists(ruta):

		for archivo in os.listdir(ruta):

			os.remove(os.path.join(ruta, archivo))

def crearArchivoLog(motivo:str)->None:

	archivo_log=f"log_{datetime.now().strftime('%Y%m%d_%H%M%S.%f')}.txt"

	ruta_log=os.path.join(os.getcwd(), "dags", "entorno", "logs", archivo_log)

	with open(ruta_log, "w") as archivo:

		archivo.write(f"Error!!! {motivo}")