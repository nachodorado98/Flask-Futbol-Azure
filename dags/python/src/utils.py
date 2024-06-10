from typing import Optional
from datetime import datetime
import unicodedata
from geopy.geocoders import Nominatim
import wget
import os
import requests

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

def url_disponible(url:str)->bool:

	try:

		peticion=requests.get(url)

		return False if peticion.status_code!=200 else True

	except Exception:

		return False

def realizarDescarga(url_imagen:str, ruta_imagenes:str, nombre_imagen:str)->None:

	try:
		
		wget.download(url_imagen, os.path.join(ruta_imagenes, f"{nombre_imagen}.png"))
	
	except Exception as e:
	
		raise Exception(f"No se ha podido descargar la imagen de {nombre_imagen}")

def descargarImagen(url_imagen:str, codigo_imagen:str, ruta_imagenes:str)->None:

	if url_disponible(f"{url_imagen}{codigo_imagen}.png"):

		realizarDescarga(f"{url_imagen}{codigo_imagen}.png", ruta_imagenes, codigo_imagen)

	else:

		realizarDescarga(f"{url_imagen}{codigo_imagen}.jpg", ruta_imagenes, codigo_imagen)