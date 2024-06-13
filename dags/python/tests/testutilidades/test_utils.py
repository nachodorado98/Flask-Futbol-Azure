import pytest
import os
import time

from src.utils import limpiarCodigoImagen, limpiarFecha, limpiarTiempo, normalizarNombre
from src.utils import obtenerCoordenadasEstadio, limpiarTamano, realizarDescarga, url_disponible
from src.utils import descargarImagen, entorno_creado, crearEntornoDataLake, subirArchivosDataLake

def test_limpiar_codigo_imagen_cadena_vacia():

	assert not limpiarCodigoImagen("")

@pytest.mark.parametrize(["codigo", "resultado"],
	[
		("hola","hola"),
		("imagen.png", "imagen"),
		("fsddfg/codigo.jpg/dgfd755", "codigo")
	]
)
def test_limpiar_codigo_imagen(codigo, resultado):

	assert limpiarCodigoImagen(codigo)==resultado

@pytest.mark.parametrize(["fecha"],
	[("",),("fecha",),("2019-06-22",),("22/6/19",),("22/13/2019",)]
)
def test_limpiar_fecha_incorrecta(fecha):

	assert not limpiarFecha(fecha)

@pytest.mark.parametrize(["fecha", "resultado"],
	[
		("22/6/2019", "2019-06-22"),
		("13/12/2023","2023-12-13")
	]
)
def test_limpiar_fecha(fecha, resultado):

	assert limpiarFecha(fecha)==resultado

@pytest.mark.parametrize(["tiempo"],
	[("",),("tiempo",),("tiempo meses",),("hola anos",)]
)
def test_limpiar_tiempo_incorrecto(tiempo):

	assert not limpiarTiempo(tiempo)

@pytest.mark.parametrize(["tiempo", "resultado"],
	[
		("10 años", 10),
		("1 meses", 1),
		("10 meses años", 10),
	]
)
def test_limpiar_tiempo(tiempo, resultado):

	assert limpiarTiempo(tiempo)==resultado

@pytest.mark.parametrize(["nombre", "nombre_normalizado"],
	[
		("Cívitas Metropolitano", "Civitas Metropolitano"),
		("El Molinón", "El Molinon"),
		("Estádio Do Dragão", "Estadio Do Dragao")
	]
)
def test_normalizar_nombre(nombre, nombre_normalizado):

	assert normalizarNombre(nombre)==nombre_normalizado

@pytest.mark.parametrize(["estadio"],
	[
		("Cívitas Metropolitano",),
		("Estadio El Molinón-Enrique Castro Quini",),
		("Estádio Do Dragão",),
		("Estadio La Rosaleda",),
		("Municipal Football Santa Amalia",),
		("estadio afdhfdhfghgfja",)
	]
)
def test_obtener_coordenadas_estadio(estadio):

	coordenadas=obtenerCoordenadasEstadio(estadio)

	assert isinstance(coordenadas, tuple)

def test_limpiar_tamano_vacio():

	tamano_limpio=limpiarTamano("")

	assert tamano_limpio.count(None)==2

@pytest.mark.parametrize(["tamano"],
	[("105 x 10",),("105x10",),("105 X 10",),("105X10",),("105 X 10 metros",),("105 x 10 metros",)]
)
def test_limpiar_tamano(tamano):

	tamano_limpio=limpiarTamano(tamano)

	assert tamano_limpio.count(None)==0

@pytest.mark.parametrize(["url"],
	[
		("https://cdn.resfu.com/img_data/equipos/183.jpg",),
		("https://cdn.resfu.com/img_data/equipos/1.png",),
		("https://cdn.resfu.com/img_data/people/original/27257.png",),
		("url",)
	]
)
def test_url_disponible_no_disponible(url):

	assert not url_disponible(url)

@pytest.mark.parametrize(["url"],
	[
		("https://cdn.resfu.com/img_data/equipos/183.png",),
		("https://cdn.resfu.com/img_data/equipos/369.png",),
		("https://cdn.resfu.com/img_data/people/original/27257.jpg",),
		("https://cdn.resfu.com/img_data/estadios/original_new/estadio_nofoto.png",),
		("https://cdn.resfu.com/img_data/estadios/original_new/23.jpg",)
	]
)
def test_url_disponible(url):

	assert url_disponible(url)

@pytest.mark.parametrize(["url"],
	[(None,), ("url_antigua",), ("url_nueva",),("url",)]
)
def test_realizar_descarga_error(url):

	with pytest.raises(Exception):

		realizarDescarga(url, "ruta", "nombre")

def borrarCarpeta(ruta:str)->None:

	if os.path.exists(ruta):

		os.rmdir(ruta)

def crearCarpeta(ruta:str)->None:

	if not os.path.exists(ruta):

		os.mkdir(ruta)

def vaciarCarpeta(ruta:str)->None:

	if os.path.exists(ruta):

		for archivo in os.listdir(ruta):

			os.remove(os.path.join(ruta, archivo))

@pytest.mark.parametrize(["url_imagen", "nombre_imagen"],
	[
		("https://cdn.resfu.com/img_data/equipos/183.png", "almeria"),
		("https://cdn.resfu.com/img_data/equipos/369.png", "atleti"),
		("https://cdn.resfu.com/img_data/people/original/27257.jpg", "cerezo"),
		("https://cdn.resfu.com/img_data/estadios/original_new/estadio_nofoto.png", "sin_estadio"),
		("https://cdn.resfu.com/img_data/estadios/original_new/23.jpg", "metropolitano"),
		("https://cdn.resfu.com/media/img/league_logos/primera-division-ea.png", "la-liga"),
		("https://cdn.resfu.com/media/img/flags/round/es.png", "espana")
	]
)
def test_realizar_descarga(url_imagen, nombre_imagen):

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Imagenes_Tests")

	crearCarpeta(ruta_carpeta)

	vaciarCarpeta(ruta_carpeta)

	realizarDescarga(url_imagen, ruta_carpeta, nombre_imagen)

	assert os.path.exists(os.path.join(ruta_carpeta, f"{nombre_imagen}.png"))

	vaciarCarpeta(ruta_carpeta)

	borrarCarpeta(ruta_carpeta)

@pytest.mark.parametrize(["url"],
	[(None,), ("url_antigua",), ("url_nueva",),("url",)]
)
def test_descargar_imagen_error_url(url):

	with pytest.raises(Exception):

		descargarImagen(url, 369, "ruta")

def test_descargar_imagen_error_codigo():

	with pytest.raises(Exception):

		descargarImagen("https://cdn.resfu.com/img_data/equipos/", 1, "ruta")

@pytest.mark.parametrize(["url_imagen", "codigo_imagen"],
	[
		("https://cdn.resfu.com/img_data/equipos/", 183),
		("https://cdn.resfu.com/img_data/equipos/", 369),
		("https://cdn.resfu.com/img_data/people/original/", 27257),
		("https://cdn.resfu.com/img_data/estadios/original_new/", "estadio_nofoto"),
		("https://cdn.resfu.com/img_data/estadios/original_new/", 23),
		("https://cdn.resfu.com/media/img/league_logos/", "primera-division-ea"),
		("https://cdn.resfu.com/media/img/flags/round/", "es")
	]
)
def test_descargar_imagen(url_imagen, codigo_imagen):

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Imagenes_Tests")

	crearCarpeta(ruta_carpeta)

	vaciarCarpeta(ruta_carpeta)

	descargarImagen(url_imagen, codigo_imagen, ruta_carpeta)

	assert os.path.exists(os.path.join(ruta_carpeta, f"{codigo_imagen}.png"))

	vaciarCarpeta(ruta_carpeta)

	borrarCarpeta(ruta_carpeta)

def test_entorno_creado_no_creado():

	assert not entorno_creado("contenedor3")

def test_entorno_creado(datalake):

	datalake.crearContenedor("contenedor3")

	time.sleep(2)

	assert entorno_creado("contenedor3")

	datalake.eliminarContenedor("contenedor3")

	datalake.cerrarConexion()

@pytest.mark.parametrize(["carpetas", "contenedor"],
	[
		(["carpeta4", "carpeta5"], 1),
		(["carpeta6"], 2),
		(["carpeta7", "carpeta8", "carpeta9"], 3),
		(["carpeta10", "carpeta11", "carpeta12", "carpeta13", "carpeta14"], 4)
	]
)
def test_crear_entorno_data_lake(datalake, carpetas, contenedor):

	crearEntornoDataLake(f"contenedornuevo{contenedor}", carpetas)

	time.sleep(2)

	assert entorno_creado(f"contenedornuevo{contenedor}")
	assert len(datalake.paths_contenedor(f"contenedornuevo{contenedor}"))==len(carpetas)

	for carpeta in carpetas:

		datalake.eliminarCarpeta(f"contenedornuevo{contenedor}", carpeta)

	datalake.eliminarContenedor(f"contenedornuevo{contenedor}")

	time.sleep(1)

	datalake.cerrarConexion()

def test_subir_archivo_data_lake_contenedor_no_existe():

	with pytest.raises(Exception):

		subirArchivosDataLake("contenedornacho", "carpeta", "ruta_local")

def test_subir_archivo_data_lake_carpeta_no_existe():

	with pytest.raises(Exception):

		subirArchivosDataLake("contenedor4", "carpeta", "ruta_local")

def test_subir_archivo_data_lake_local_no_existe(datalake):

	crearEntornoDataLake("contenedor4", ["carpeta_creada"])

	with pytest.raises(Exception):

		subirArchivosDataLake("contenedor4", "carpeta_creada", "ruta_local")

	datalake.cerrarConexion()

def test_subir_archivo_data_lake_archivo_no_existen(datalake):

	ruta_carpeta=os.path.join(os.getcwd(), "Archivos_Tests_Data_Lake")

	crearCarpeta(ruta_carpeta)

	subirArchivosDataLake("contenedor4", "carpeta_creada", ruta_carpeta)

	archivos_carpeta_contenedor=datalake.paths_carpeta_contenedor("contenedor4", "carpeta_creada")

	assert not archivos_carpeta_contenedor

	datalake.cerrarConexion()

def crearArchivoTXT(ruta:str, nombre:str)->None:

	ruta_archivo=os.path.join(ruta, nombre)

	with open(ruta_archivo, "w") as file:

	    file.write("Nacho")

def test_subir_archivo_data_lake(datalake):

	ruta_carpeta=os.path.join(os.getcwd(), "Archivos_Tests_Data_Lake")

	nombre_archivo="archivo.txt"

	crearArchivoTXT(ruta_carpeta, nombre_archivo)

	subirArchivosDataLake("contenedor4", "carpeta_creada", ruta_carpeta)

	archivos_carpeta_contenedor_nuevos=datalake.paths_carpeta_contenedor("contenedor4", "carpeta_creada")

	assert len(archivos_carpeta_contenedor_nuevos)==1

	datalake.eliminarContenedor("contenedor4")

	datalake.cerrarConexion()

	vaciarCarpeta(ruta_carpeta)

def test_subir_archivo_data_lake_archivo_existente(datalake):

	crearEntornoDataLake("contenedor5", ["carpeta"])

	ruta_carpeta=os.path.join(os.getcwd(), "Archivos_Tests_Data_Lake")

	nombre_archivo="archivo.txt"

	crearArchivoTXT(ruta_carpeta, nombre_archivo)

	datalake.subirArchivo("contenedor5", "carpeta", ruta_carpeta, nombre_archivo)

	archivos_carpeta_contenedor=datalake.paths_carpeta_contenedor("contenedor5", "carpeta")

	assert len(archivos_carpeta_contenedor)==1

	subirArchivosDataLake("contenedor5", "carpeta", ruta_carpeta)

	archivos_carpeta_contenedor_nuevos=datalake.paths_carpeta_contenedor("contenedor5", "carpeta")

	assert len(archivos_carpeta_contenedor_nuevos)==1

	datalake.eliminarContenedor("contenedor5")

	datalake.cerrarConexion()

	vaciarCarpeta(ruta_carpeta)

def test_subir_archivo_data_lake_archivos_existentes_no_existentes(datalake):

	crearEntornoDataLake("contenedor6", ["carpeta"])

	ruta_carpeta=os.path.join(os.getcwd(), "Archivos_Tests_Data_Lake")

	nombre_archivos_subir=[f"archivo{numero}_subir.txt" for numero in range(1,6)]

	for nombre_archivo in nombre_archivos_subir:

		crearArchivoTXT(ruta_carpeta, nombre_archivo)

		datalake.subirArchivo("contenedor6", "carpeta", ruta_carpeta, nombre_archivo)

	nombre_archivos_no_subir=[f"archivo{numero}_no_subir.txt" for numero in range(1,6)]

	for nombre_archivo in nombre_archivos_no_subir:

		crearArchivoTXT(ruta_carpeta, nombre_archivo)

	archivos_carpeta_contenedor=datalake.paths_carpeta_contenedor("contenedor6", "carpeta")

	assert len(archivos_carpeta_contenedor)==5
	assert len(os.listdir(ruta_carpeta))==10

	subirArchivosDataLake("contenedor6", "carpeta", ruta_carpeta)

	archivos_carpeta_contenedor_nuevos=datalake.paths_carpeta_contenedor("contenedor6", "carpeta")

	assert len(archivos_carpeta_contenedor_nuevos)==10

	datalake.eliminarContenedor("contenedor6")

	datalake.cerrarConexion()

	vaciarCarpeta(ruta_carpeta)

	borrarCarpeta(ruta_carpeta)