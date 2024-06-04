from typing import Optional
from datetime import datetime
import unicodedata
from geopy.geocoders import Nominatim

def limpiarCodigoImagen(link:str)->Optional[str]:

	if link=="":

		return None

	try:

		return link.split(".png")[0].split("/")[-1] if ".png" in link else link.split(".jpg")[0].split("/")[-1]

	except Exception:

		return None

def limpiarFecha(fecha:str)->Optional[str]:

	try:

		return datetime.strptime(fecha, "%d/%m/%Y").strftime("%Y-%m-%d")

	except Exception:

		return None

def limpiarTiempo(tiempo:str)->Optional[int]:

	try:

		return int(tiempo.split(" ")[0])

	except Exception:

		return None

def normalizarNombre(nombre:str)->str:

	nfkd=unicodedata.normalize("NFKD", nombre)

	return "".join([valor for valor in nfkd if not unicodedata.combining(valor)])

def obtenerCoordenadasEstadio(estadio:str)->tuple:

	try:

		loc=Nominatim(user_agent="Geopy Library")

		localizacion=loc.geocode(estadio)

		if localizacion is None:

			return (None, None)

		return localizacion.latitude, localizacion.longitude

	except Exception:

		return (None, None)

def limpiarTamano(tamano:str)->tuple:

	if tamano=="":

		return None, None

	largo, ancho=tamano.split("x") if "x" in tamano else tamano.split("X")

	return int(largo.strip()), int(ancho.split("metros")[0].strip())