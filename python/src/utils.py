from typing import Optional
from datetime import datetime

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