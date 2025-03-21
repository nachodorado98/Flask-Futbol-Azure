from typing import Optional, List, Any
from datetime import datetime
import unicodedata
from geopy.geocoders import Nominatim
import wget
import os
import requests
import pandas as pd
import re

from .datalake.conexion_data_lake import ConexionDataLake
from .database.conexion import Conexion

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

	nombre_normalizado="".join([valor for valor in nfkd if not unicodedata.combining(valor)])

	for caracter in ["(", ")", "–"]:

		nombre_normalizado=nombre_normalizado.replace(caracter, "")

	return nombre_normalizado.replace("  ", " ")

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

	return int(largo.strip()), int(ancho.split("metros")[0].split("m")[0].strip())

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

def entorno_creado(nombre_contenedor:str)->bool:

	datalake=ConexionDataLake()

	contenedores=datalake.contenedores_data_lake()

	datalake.cerrarConexion()

	contenedor_existe=[contenedor for contenedor in contenedores if nombre_contenedor in contenedor["name"]]

	return False if not contenedor_existe else True

def crearEntornoDataLake(nombre_contenedor:str, nombres_carpetas:List[str])->None:

	datalake=ConexionDataLake()

	datalake.crearContenedor(nombre_contenedor)

	for nombre_carpeta in nombres_carpetas:

		datalake.crearCarpeta(nombre_contenedor, nombre_carpeta)

	datalake.cerrarConexion()

def subirArchivosDataLake(nombre_contenedor:str, nombre_carpeta:str, ruta_local_carpeta:str)->None:

	datalake=ConexionDataLake()

	archivos_carpeta_contenedor=datalake.paths_carpeta_contenedor(nombre_contenedor, nombre_carpeta)

	archivos_carpeta_contenedor_limpios=[archivo.name.split(f"{nombre_carpeta}/")[1] for archivo in archivos_carpeta_contenedor]

	try:

		archivos_local=os.listdir(ruta_local_carpeta)

	except Exception:

		raise Exception("La ruta de la carpeta local de los archivos es incorrecta")

	for archivo_local in archivos_local:

		if archivo_local not in archivos_carpeta_contenedor_limpios:

			datalake.subirArchivo(nombre_contenedor, nombre_carpeta, ruta_local_carpeta, archivo_local)

	datalake.cerrarConexion()

def limpiarFechaInicio(fecha_inicio:str)->tuple:

	try:

		objeto_fecha=datetime.strptime(fecha_inicio, "%Y-%m-%dT%H:%M:%S%z")

		return objeto_fecha.strftime("%Y-%m-%d"), objeto_fecha.strftime("%H:%M")

	except Exception:

		return None, None

def ganador_goles(goles:str)->str:

	try:

		goles_local, goles_visitante=map(int, goles.split("-"))

		if goles_local>goles_visitante:

			return "Victoria Local"

		elif goles_local<goles_visitante:

			return "Victoria Visitante"

		else:

			return "Empate"

	except Exception:

		return "Sin Resultado"

def obtenerResultado(marcador:str)->str:

	if "(" not in marcador or ")" not in marcador:

		return ganador_goles(marcador)

	else:

		marcador_penaltis=marcador.split("(")[1].split(")")[0]

		return ganador_goles(marcador_penaltis)+" Penaltis"

def generarTemporadas(ano_inicio:int, mes_limite:int=7)->List[Optional[int]]:

	hoy=datetime.now()
	ano_actual=hoy.year
	mes_actual=hoy.month

	ano_final=ano_actual if mes_actual<=mes_limite else ano_actual+1
	
	return list(range(ano_inicio, ano_final+1))

def obtenerBoolCadena(cadena_bool:str)->bool:

	try:

		return eval(cadena_bool)

	except Exception:

		raise Exception("No es bool")

def subirTablaDataLake(tabla:str, contenedor:str, carpeta:str)->None:

	conexion=Conexion()

	datalake=ConexionDataLake()

	try:

		if conexion.tabla_vacia(tabla):

			raise Exception("La tabla esta vacia")

		df=pd.read_sql(f"SELECT * FROM {tabla}", conexion.bbdd)

		if not datalake.existe_contenedor(contenedor) or not datalake.existe_carpeta(contenedor, carpeta):

			raise Exception("El contendor o la carpeta no existen en el data lake")

		ruta_archivo=f"abfs://{contenedor}@{datalake.cuenta}.dfs.core.windows.net/{carpeta}/"

		nombre_archivo=f"tabla_{tabla}_backup_{datetime.now().strftime('%Y%m%d')}.csv"

		df.to_csv(ruta_archivo+nombre_archivo, storage_options={"account_key":datalake.clave}, index=False)

	except Exception as e:

		raise Exception(f"Error al subir la tabla {tabla} al data lake: {e}")

	finally:

		datalake.cerrarConexion()

		conexion.cerrarConexion()

def limpiarMinuto(minuto:str)->tuple:

	minuto_numero, anadido=minuto.split("'")

	return (int(minuto_numero), 0) if anadido=="" else (int(minuto_numero), int(anadido.split("+")[-1]))

def obtenerArchivosNoExistenDataLake(nombre_contenedor:str, nombre_carpeta:str, archivos_comprobar:List[Any], extension:str="png")->List[Any]:

	datalake=ConexionDataLake()

	archivos_carpeta_contenedor=datalake.paths_carpeta_contenedor(nombre_contenedor, nombre_carpeta)

	datalake.cerrarConexion()

	archivos_carpeta_contenedor_limpios=[archivo.name.split(f"{nombre_carpeta}/")[1] for archivo in archivos_carpeta_contenedor]

	return list(filter(lambda archivo: f"{archivo}.{extension}" not in archivos_carpeta_contenedor_limpios, archivos_comprobar))

def obtenerCiudadMasCercana(latitud:float, longitud:str, distancia_minima:int=2, umbral_maximo:int=5, umbral_minimo:int=2)->tuple:

	conexion=Conexion()

	ciudades=conexion.obtenerCiudadesMasCercanas(latitud, longitud)

	conexion.cerrarConexion()

	if not ciudades:

		raise Exception("No hay ciudades cercanas")

	if len(ciudades)==1:

		return ciudades[0][0], ciudades[0][1]

	ciudad_distancia, ciudad_prioridad=ciudades[0], ciudades[1]

	diferencia_distancias=ciudad_prioridad[2]-ciudad_distancia[2]

	if ciudad_distancia[2]<1:

		return ciudad_distancia[0], ciudad_distancia[1]

	elif diferencia_distancias>=umbral_maximo:

		return ciudad_distancia[0], ciudad_distancia[1]

	elif diferencia_distancias<=umbral_minimo:

		return ciudad_prioridad[0], ciudad_prioridad[1]

	else:

		if ciudad_prioridad[3]<ciudad_distancia[3]:

			return ciudad_prioridad[0], ciudad_prioridad[1]

		else:

			return ciudad_distancia[0], ciudad_distancia[1]

def obtenerPosiblesCiudadesCaracteres(direccion:str)->List[Optional[str]]:

	try:

		if not direccion.strip():

			return []

		direccion=direccion.replace("/", ",").replace("(", ",").replace(")", ",").replace("-", ",")
		
		partes=direccion.split(",")

		posibles_ciudades=[]

		for parte in partes:

			parte=re.sub(r"\d+", "", parte)

			parte=re.sub(r"\W+", " ", parte, flags=re.UNICODE)

			parte=parte.strip()
			

			if len(parte)>2:

				posibles_ciudades.append(parte)

		return posibles_ciudades

	except Exception:

		return []

def filtrarCiudadesPalabrasIrrelevantes(ciudades:List[str])->List[Optional[str]]:

	PALABRAS_IRRELEVANTES=["calle", "c.", "av", "avenida", "paseo", "p.º", "plaza", "carrer", "rua", "via",
							"bulevar", "boulevard", "camino", "paseig", "road", "strasse", "allee", "stadium", "dr",
							"stadionstraße", "street", "rue", "corso", "viale", "autopista", "carretera", "ul", "s/n",
							"p º", "ul ", "camí", "rúa", "c del", "ctra", "c los", "straße", "c "]

	PALABRAS_IRRELEVANTES_INCLUIDAS=["airport", "universidad", "street", "piazzale", "plaza", "paseo", "calle", " rd", "club",
									"ciudad", "dirección", "finca", "passeig", " road", " gate", "kalea", " way", "platz",
									"väg"]

	ciudades_filtradas=[]

	try:

		for ciudad in ciudades:

			ciudad_minuscula=ciudad.lower()

			ciudad_palabra_irrelevante=[ciudad_minuscula for palabra_irrelevante in PALABRAS_IRRELEVANTES if ciudad_minuscula.startswith(palabra_irrelevante)]

			ciudad_palabra_irrelevante_incluidas=[ciudad_minuscula for palabra_irrelevante in PALABRAS_IRRELEVANTES_INCLUIDAS if palabra_irrelevante in ciudad_minuscula]

			if not ciudad_palabra_irrelevante and not ciudad_palabra_irrelevante_incluidas:

				ciudades_filtradas.append(ciudad)

		return ciudades_filtradas

	except Exception:

		return []

def filtrarCiudadDireccion(direccion:str)->List[Optional[str]]:

	posibles_ciudades=obtenerPosiblesCiudadesCaracteres(direccion)

	posibles_ciudades_filtradas=filtrarCiudadesPalabrasIrrelevantes(posibles_ciudades)

	conexion=Conexion()

	ciudades_existen=list(filter(lambda ciudad: conexion.existe_ciudad(ciudad), posibles_ciudades_filtradas))

	conexion.cerrarConexion()

	return ciudades_existen

def obtenerCiudadMasAcertada(latitud:float, longitud:str, direccion:str)->str:

	ciudad_coordenadas, pais_corrdenadas=obtenerCiudadMasCercana(latitud, longitud)

	ciudades_existen=filtrarCiudadDireccion(direccion)

	if not ciudades_existen:

		return ciudad_coordenadas

	elif ciudad_coordenadas in ciudades_existen:

		return ciudad_coordenadas

	else:

		if len(ciudades_existen)==1:

			return ciudades_existen[0]

		else:

			return ciudad_coordenadas