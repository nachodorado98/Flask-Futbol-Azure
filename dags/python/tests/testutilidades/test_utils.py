import pytest
import os
import time
from datetime import datetime
from unittest.mock import patch

from src.utils import limpiarCodigoImagen, limpiarFecha, limpiarTiempo, normalizarNombre
from src.utils import obtenerCoordenadasEstadio, limpiarTamano, realizarDescarga, url_disponible
from src.utils import descargarImagen, entorno_creado, crearEntornoDataLake, subirArchivosDataLake
from src.utils import limpiarFechaInicio, ganador_goles, obtenerResultado, generarTemporadas
from src.utils import obtenerBoolCadena, subirTablaDataLake, limpiarMinuto, obtenerArchivosNoExistenDataLake

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

def test_subir_archivo_data_lake_carpeta_no_existe(datalake):

	datalake.crearContenedor("contenedor45")

	with pytest.raises(Exception):

		subirArchivosDataLake("contenedor45", "carpeta", "ruta_local")

	datalake.eliminarContenedor("contenedor45")

	datalake.cerrarConexion()

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

@pytest.mark.parametrize(["fecha_inicio"],
	[("",),("fecha",),("2019-06-22",),("22/6/19",),("22/13/2019",),("2019-06-2222:22",)]
)
def test_limpiar_fecha_inicio_incorrecta(fecha_inicio):

	assert limpiarFechaInicio(fecha_inicio)==(None, None)

@pytest.mark.parametrize(["fecha_inicio", "resultado"],
	[
		("2024-03-23T16:15:00+01:00", ("2024-03-23", "16:15")),
		("2024-06-22T10:00:00+03:00", ("2024-06-22", "10:00")),
		("2019-04-13T00:00:00+01:00", ("2019-04-13", "00:00"))
	]
)
def test_limpiar_fecha_inicio(fecha_inicio, resultado):

	assert limpiarFechaInicio(fecha_inicio)==resultado

def test_ganador_goles_erroneo():

	assert ganador_goles("resultado goles")=="Sin Resultado"

@pytest.mark.parametrize(["goles", "ganador"],
	[
		("0-0", "Empate"),
		("1-0", "Victoria Local"),
		("1-3", "Victoria Visitante")
	]
)
def test_ganador_goles(goles, ganador):

	assert ganador_goles(goles)==ganador

def test_obtener_resultado_erroneo():

	assert obtenerResultado("000")=="Sin Resultado"

@pytest.mark.parametrize(["marcador", "ganador"],
	[
		("0-0", "Empate"),
		("1-0", "Victoria Local"),
		("1-3", "Victoria Visitante"),
		("1(3-4)1", "Victoria Visitante Penaltis"),
		("1(10-4)1", "Victoria Local Penaltis"),
		("1(2-2)1", "Empate Penaltis")
	]
)
def test_obtener_resultado(marcador, ganador):

	assert obtenerResultado(marcador)==ganador

def test_generar_temporadas_ano_actual():

	ano_actual=datetime.now().year

	with patch("src.utils.datetime") as mock_datetime:

		mock_datetime.now.return_value=datetime(ano_actual, 1, 1)

		mock_datetime.side_effect=lambda *args, **kw: datetime(*args, **kw)

		temporadas=generarTemporadas(ano_actual)

	assert len(temporadas)==1
	assert temporadas[0]==ano_actual

@pytest.mark.parametrize(["numero"],
	[(1,),(3,),(2,),(10,),(5,),(100,),(22,)]
)
def test_generar_temporadas_vacio(numero):

	ano_actual=datetime.now().year

	with patch("src.utils.datetime") as mock_datetime:

		mock_datetime.now.return_value=datetime(ano_actual, 1, 1)

		mock_datetime.side_effect=lambda *args, **kw: datetime(*args, **kw)

		assert not generarTemporadas(ano_actual+numero)

@pytest.mark.parametrize(["ano_inicio", "mes_anterior_limite"],
	[(2023, 6),(2019, 1),(1998, 5),(1999, 4),(1900, 2),(1800, 1),(1950, 7),(1922, 3)]
)
def test_generar_temporadas_mes_anterior_limite(ano_inicio, mes_anterior_limite):

	ano_actual=datetime.now().year

	with patch("src.utils.datetime") as mock_datetime:

		mock_datetime.now.return_value=datetime(ano_actual, mes_anterior_limite, 28)

		mock_datetime.side_effect=lambda *args, **kw: datetime(*args, **kw)

		temporadas=generarTemporadas(ano_inicio)

	assert len(temporadas)==ano_actual+1-ano_inicio
	assert temporadas[0]==ano_inicio

@pytest.mark.parametrize(["ano_inicio", "mes_superior_limite"],
	[(2023, 8),(2019, 10),(1998, 9),(1999, 11),(1900, 12),(1800, 8),(1950, 12),(1922, 9)]
)
def test_generar_temporadas_mes_superior_limite(ano_inicio, mes_superior_limite):

	ano_actual=datetime.now().year

	with patch("src.utils.datetime") as mock_datetime:

		mock_datetime.now.return_value=datetime(ano_actual, mes_superior_limite, 1)

		mock_datetime.side_effect=lambda *args, **kw: datetime(*args, **kw)

		temporadas=generarTemporadas(ano_inicio)

	assert len(temporadas)==ano_actual+2-ano_inicio
	assert temporadas[0]==ano_inicio

def test_obtener_bool_cadena_true():

	valor=obtenerBoolCadena("True")

	assert valor is True
	assert isinstance(valor, bool)

def test_obtener_bool_cadena_false():

	valor=obtenerBoolCadena("False")

	assert valor is False
	assert isinstance(valor, bool)

def test_obtener_bool_cadena_error():

	with pytest.raises(Exception):

		obtenerBoolCadena("no_soy_bool")

def test_subir_tabla_data_lake_tabla_no_existe():

	with pytest.raises(Exception):

		subirTablaDataLake("no_existo", "contenedor", "carpeta")

def test_subir_tabla_data_lake_tabla_vacia(conexion):

	with pytest.raises(Exception):

		subirTablaDataLake("equipos", "contenedor", "carpeta")

def test_subir_tabla_data_lake_contenedor_no_existe(conexion):

	conexion.insertarEquipo("atletico-madrid")

	with pytest.raises(Exception):

		subirTablaDataLake("equipos", "contenedor", "carpeta")

def test_subir_tabla_data_lake_carpeta_no_existe(conexion, datalake):

	conexion.insertarEquipo("atletico-madrid")

	datalake.crearContenedor("contenedor7")

	with pytest.raises(Exception):

		subirTablaDataLake("equipos", "contenedor7", "carpeta")

	datalake.eliminarContenedor("contenedor7")

	datalake.cerrarConexion()

def test_subir_tabla_data_lake(conexion, datalake):

	conexion.insertarEquipo("atletico-madrid")

	crearEntornoDataLake("contenedor8", ["carpeta/tabla"])

	time.sleep(5)

	subirTablaDataLake("equipos", "contenedor8", "carpeta/tabla")

	archivo=datalake.paths_carpeta_contenedor("contenedor8", "carpeta/tabla")[0]["name"]

	assert archivo.startswith("carpeta/tabla/tabla_equipos_backup_")
	assert archivo.endswith(".csv")

	datalake.eliminarContenedor("contenedor8")

	datalake.cerrarConexion()

@pytest.mark.parametrize(["minuto", "minuto_numero", "anadido_numero"],
	[
		("39'", 39, 0),
		("100'", 100, 0),
		("45'+1", 45, 1),
		("0'", 0, 0),
		("120'+8", 120, 8)
	]
)
def test_limpiar_minuto(minuto, minuto_numero, anadido_numero):

	assert limpiarMinuto(minuto)==(minuto_numero, anadido_numero)

def test_obtener_archivos_no_existen_data_lake_contenedor_no_existe():

	with pytest.raises(Exception):

		obtenerArchivosNoExistenDataLake("contenedornacho", "carpeta", ["archivo1", "archivo2"])

def test_obtener_archivos_no_existen_data_lake_carpeta_no_existe(datalake):

	datalake.crearContenedor("contenedor85")

	with pytest.raises(Exception):

		obtenerArchivosNoExistenDataLake("contenedor9", "carpeta", ["archivo1", "archivo2"])

	datalake.eliminarContenedor("contenedor85")

	datalake.cerrarConexion()

def test_obtener_archivos_no_existen_data_lake_archivos_comprobar_no_existen(datalake):

	crearEntornoDataLake("contenedor9", ["carpeta_creada"])

	ruta_carpeta=os.path.join(os.getcwd(), "Archivos_Tests_Data_Lake")

	nombre_archivo="archivo.txt"

	crearArchivoTXT(ruta_carpeta, nombre_archivo)

	subirArchivosDataLake("contenedor9", "carpeta_creada", ruta_carpeta)

	archivos_carpeta_contenedor=datalake.paths_carpeta_contenedor("contenedor9", "carpeta_creada")

	assert len(archivos_carpeta_contenedor)==1

	assert not obtenerArchivosNoExistenDataLake("contenedor9", "carpeta_creada", [])

	datalake.eliminarContenedor("contenedor9")

	datalake.cerrarConexion()

	vaciarCarpeta(ruta_carpeta)

def test_obtener_archivos_no_existen_data_lake_archivos_datalake_no_existen(datalake):

	crearEntornoDataLake("contenedor10", ["carpeta_creada"])

	archivos_carpeta_contenedor=datalake.paths_carpeta_contenedor("contenedor10", "carpeta_creada")

	assert not archivos_carpeta_contenedor

	archivos_comprobar=obtenerArchivosNoExistenDataLake("contenedor10", "carpeta_creada", ["archivo1", "archivo2"])

	assert len(archivos_comprobar)==2

	datalake.eliminarContenedor("contenedor10")

	datalake.cerrarConexion()

def test_obtener_archivos_no_existen_data_lake(datalake):

	crearEntornoDataLake("contenedor11", ["carpeta_creada"])

	ruta_carpeta=os.path.join(os.getcwd(), "Archivos_Tests_Data_Lake")

	nombre_archivo="archivo.txt"

	crearArchivoTXT(ruta_carpeta, nombre_archivo)

	subirArchivosDataLake("contenedor11", "carpeta_creada", ruta_carpeta)

	archivos_carpeta_contenedor=datalake.paths_carpeta_contenedor("contenedor11", "carpeta_creada")

	assert len(archivos_carpeta_contenedor)==1

	assert not obtenerArchivosNoExistenDataLake("contenedor11", "carpeta_creada", ["archivo"], "txt")

	datalake.eliminarContenedor("contenedor11")

	datalake.cerrarConexion()

	vaciarCarpeta(ruta_carpeta)

def test_obtener_archivos_no_existen_data_lake_varios_existen_todos(datalake):

	crearEntornoDataLake("contenedor12", ["carpeta_creada"])

	ruta_carpeta=os.path.join(os.getcwd(), "Archivos_Tests_Data_Lake")

	for numero in range(15):

		nombre_archivo=f"archivo{numero}.txt"

		crearArchivoTXT(ruta_carpeta, nombre_archivo)

	subirArchivosDataLake("contenedor12", "carpeta_creada", ruta_carpeta)

	archivos_carpeta_contenedor=datalake.paths_carpeta_contenedor("contenedor12", "carpeta_creada")

	assert len(archivos_carpeta_contenedor)==15

	assert not obtenerArchivosNoExistenDataLake("contenedor12", "carpeta_creada", ["archivo1", "archivo13", "archivo7"], "txt")

	datalake.eliminarContenedor("contenedor12")

	datalake.cerrarConexion()

	vaciarCarpeta(ruta_carpeta)

def test_obtener_archivos_no_existen_data_lake_varios_no_existen_todos(datalake):

	crearEntornoDataLake("contenedor13", ["carpeta_creada"])

	ruta_carpeta=os.path.join(os.getcwd(), "Archivos_Tests_Data_Lake")

	for numero in range(15):

		nombre_archivo=f"archivo{numero}.txt"

		crearArchivoTXT(ruta_carpeta, nombre_archivo)

	subirArchivosDataLake("contenedor13", "carpeta_creada", ruta_carpeta)

	archivos_carpeta_contenedor=datalake.paths_carpeta_contenedor("contenedor13", "carpeta_creada")

	assert len(archivos_carpeta_contenedor)==15

	archivos_comprobar=obtenerArchivosNoExistenDataLake("contenedor13", "carpeta_creada", ["archivo1", "archivo13", "archivo17"], "txt")

	assert len(archivos_comprobar)==1
	assert archivos_comprobar[0]=="archivo17"

	datalake.eliminarContenedor("contenedor13")

	datalake.cerrarConexion()

	vaciarCarpeta(ruta_carpeta)

	borrarCarpeta(ruta_carpeta)