import pytest
import os
import geopandas as gpd

from src.utilidades.utils import usuario_correcto, nombre_correcto, apellido_correcto, contrasena_correcta
from src.utilidades.utils import fecha_correcta, equipo_correcto, correo_correcto, datos_correctos
from src.utilidades.utils import generarHash, comprobarHash, anadirPuntos
from src.utilidades.utils import limpiarResultadosPartidos, obtenerNombrePaisSeleccionado, obtenerPaisesNoSeleccionados
from src.utilidades.utils import crearCarpeta, borrarCarpeta, vaciarCarpeta, vaciarCarpetaMapasUsuario
from src.utilidades.utils import obtenerCentroide, crearMapaMisEstadios, crearMapaMisEstadiosDetalle
from src.utilidades.utils import leerGeoJSON, obtenerGeometriaPais, obtenerGeometriasPaises, crearMapaMisEstadiosDetallePaises
from src.utilidades.utils import crearMapaEstadio, obtenerCompeticionesPartidosUnicas, extraerExtension, comprobarFechas
from src.utilidades.utils import obtenerPrimerUltimoDiaAnoMes, mapearAnoMes, obtenerAnoMesFechas, generarCalendario
from src.utilidades.utils import cruzarPartidosCalendario, ano_mes_anterior, ano_mes_siguiente, limpiarResultadosPartidosCalendario
from src.utilidades.utils import datos_trayectos_correctos, crearMapaTrayecto, obtenerCentroideCoordenadas, crearMapaTrayectos
from src.utilidades.utils import crearMapaTrayectosIdaVuelta

@pytest.mark.parametrize(["usuario"],
	[("ana_maria",),("carlos_456",),("",),(None,)]
)
def test_usuario_incorrecto(usuario):

	assert not usuario_correcto(usuario)

@pytest.mark.parametrize(["usuario"],
	[("juan123",),("usuario1",),("12345",)]
)
def test_usuario_correcto(usuario):

	assert usuario_correcto(usuario)

@pytest.mark.parametrize(["nombre"],
	[("123",),("Juan Maria",),(None,),("",),("Nacho1998",)]
)
def test_nombre_incorrecto(nombre):

	assert not nombre_correcto(nombre)

@pytest.mark.parametrize(["nombre"],
	[("Nacho",),("Pérez",),("Ana",),("López",),("Carlos",),("González",),("Amanda",)]
)
def test_nombre_correcto(nombre):

	assert nombre_correcto(nombre)

@pytest.mark.parametrize(["apellido"],
	[("123",),("Aranda Gonzalez",),(None,),("",),("Dorado1998",)]
)
def test_apellido_incorrecto(apellido):

	assert not apellido_correcto(apellido)

@pytest.mark.parametrize(["apellido"],
	[("Nacho",),("Pérez",),("Ana",),("López",),("Carlos",),("González",),("Amanda",)]
)
def test_apellido_correcto(apellido):

	assert apellido_correcto(apellido)

@pytest.mark.parametrize(["contrasena"],
	[("clave",),("CONTRASENA",),("12345678",),("Abcdefg",),("",),("A1b2C3d4",),("abcd",),("1234",),
	 ("Ab CdEfGhI",),("Ab!CdEfGhI ",),(" Ab!CdEfGhI",),("Ab!CdEfGhIJKLMN",),("Ab@cdEfG",),
	 ("Ab@cdEf1 G",),("Abcd12 34!",),(None,)]
)
def test_contrasena_incorrecta(contrasena):

	assert not contrasena_correcta(contrasena)

@pytest.mark.parametrize(["contrasena"],
	[("Ab!CdEfGhIJK3LMN",),("Abcd1234!",),("22&NachoD&19",)]
)
def test_contrasena_correcta(contrasena):

	assert contrasena_correcta(contrasena)

@pytest.mark.parametrize(["fecha"],
	[("1800-01-01",),("2100-01-01",),("1900-02-29",),("01-01-2000",),("2000/01/01",)]
)
def test_fecha_incorrecta(fecha):

	assert not fecha_correcta(fecha)

@pytest.mark.parametrize(["fecha"],
	[("1900-01-01",),("2005-01-01",),("2004-02-29",),("1998-02-16",),("1999-08-06",)]
)
def test_fecha_correcta(fecha):

	assert fecha_correcta(fecha)

@pytest.mark.parametrize(["equipo"],
	[("equipo_1",),("atleti?co",),("6jfd-8%",),(None,),("",)]
)
def test_equipo_incorrecto(equipo):

	assert not equipo_correcto(equipo)

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("barcelona",),("1-fc-koln",)]
)
def test_equipo_correcto(equipo):

	assert equipo_correcto(equipo)

@pytest.mark.parametrize(["correo"],
	[("correo_sin_arroba.com",),("usuario@sin_punto",),("correo@falta_punto_com",),("sin_local_part@.com",),("@falta_local_part.com",)]
)
def test_correo_incorrecto(correo):

	assert not correo_correcto(correo)

@pytest.mark.parametrize(["correo"],
	[("usuario@gmail.com",),("ejemplo123@yahoo.com",),("mi_correo-123@dominio.com",),
	("usuario+etiqueta@dominio.com",), ("ejemplo.123@subdominio.dominio.co.uk",)]
)
def test_correo_correcto(correo):

	assert correo_correcto(correo)

@pytest.mark.parametrize(["usuario", "nombre", "apellido", "contrasena", "fecha_nacimiento", "equipo", "correo"],
	[
		(None, "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "atleti", "correo@correo.es"),
		("golden98", None, "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "atleti", "correo@correo.es"),
		("golden98", "nacho", None, "Ab!CdEfGhIJK3LMN", "1998-02-16", "atleti", "correo@correo.es"),
		("golden98", "nacho", "dorado", None, "1998-02-16", "atleti", "correo@correo.es"),
		("golden98", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", None, "atleti", "correo@correo.es"),
		("golden98", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", None, "correo@correo.es"),
		("golden98", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "atleti", None),
		("carlos_456", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "atleti", "correo@correo.es"),
		("golden98", "nacho1", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "atleti", "correo@correo.es"),
		("golden98", "nacho", "dorado2", "Ab!CdEfGhIJK3LMN", "1998-02-16", "atleti", "correo@correo.es"),
		("golden98", "nacho", "dorado", "12345678", "1998-02-16", "atleti", "correo@correo.es"),
		("golden98", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "2098-02-16", "atleti", "correo@correo.es"),
		("golden98", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "atleti?co", "correo@correo.es"),
		("golden98", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "atletico", "correo@.es")
	]
)
def test_datos_incorrectos(usuario, nombre, apellido, contrasena, fecha_nacimiento, equipo, correo):

	assert not datos_correctos(usuario, nombre, apellido, contrasena, fecha_nacimiento, equipo, correo)

@pytest.mark.parametrize(["usuario", "nombre", "apellido", "contrasena", "fecha_nacimiento", "equipo", "correo"],
	[
		("nacho98", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "atleti", "correo@correo.es"),
		("golden98", "nachogolden", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "atleti", "correo@gmail.es"),
	]
)
def test_datos_correctos(usuario, nombre, apellido, contrasena, fecha_nacimiento, equipo, correo):

	assert datos_correctos(usuario, nombre, apellido, contrasena, fecha_nacimiento, equipo, correo)

@pytest.mark.parametrize(["contrasena"],
	[("contrasena1234",),("123456789",),("contrasena_secreta",)]
)
def test_generar_hash_contrasena(contrasena):

	contrasena_hash=generarHash(contrasena)

	assert len(contrasena_hash)==60
	assert contrasena not in contrasena_hash

@pytest.mark.parametrize(["contrasena", "contrasena_mal"],
	[
		("contrasena1234","contrasena123"),
		("123456789","1234567899"),
		("contrasena_secreta","contrasenasecreta")
	]
)
def test_comprobar_hash_contrasena_incorrecta(contrasena, contrasena_mal):

	contrasena_hash=generarHash(contrasena)

	assert not comprobarHash(contrasena_mal, contrasena_hash)

@pytest.mark.parametrize(["contrasena"],
	[("contrasena1234",),("123456789",),("contrasena_secreta",)]
)
def test_comprobar_hash_contrasena_correcta(contrasena):

	contrasena_hash=generarHash(contrasena)

	assert comprobarHash(contrasena, contrasena_hash)

@pytest.mark.parametrize(["numero", "numero_puntos"],
	[
		("100", "100"),
		("1234", "1.234"),
		("987654", "987.654"),
		("1", "1"),
		("1000000", "1.000.000")
	]
)
def test_anadir_puntos(numero, numero_puntos):

	assert anadirPuntos(numero)==numero_puntos

def test_limpiar_resultados_partidos_no_hay():

	resultados=limpiarResultadosPartidos([])

	assert isinstance(resultados, dict)
	assert resultados["ganados"]==0
	assert resultados["perdidos"]==0
	assert resultados["empatados"]==0

@pytest.mark.parametrize(["partidos", "ganados", "perdidos", "empatados"],
	[
		([(1, 0, 0), (0, 0, 1), (1, 0, 0), (0, 1, 0), (1, 0, 0), (1, 0, 0)], 4, 1, 1),
		([(0, 0, 0), (0, 0, 1), (1, 0, 0), (0, 1, 0), (1, 0, 0), (1, 0, 0)], 3, 1, 1),
		([(1, 0, 0), (0, 0, 1), (1, 0, 0), (0, 1, 0), (1, 0, 0)], 3, 1, 1),
		([(1, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 0), (0, 1, 0), (1, 0, 0)], 2, 3, 1),
		([(1, 1, 1), (0, 0, 1), (1, 0, 0), (0, 1, 0), (1, 0, 0), (1, 0, 0)], 4, 2, 2),
	]
)
def test_limpiar_resultados_partidos(partidos, ganados, perdidos, empatados):

	resultados=limpiarResultadosPartidos(partidos)

	assert isinstance(resultados, dict)
	assert resultados["ganados"]==ganados
	assert resultados["perdidos"]==perdidos
	assert resultados["empatados"]==empatados

@pytest.mark.parametrize(["codigo_pais"],
	[("fr",),("uk",),("gb",),("ch",)]
)
def test_obtener_nombre_pais_seleccionado_no_esta(codigo_pais):

	paises=[("es", "España", 12), ("it", "Italia", 1), ("nl", "Países Bajos", 1),
			("pt", "Portugal", 1), ("ss", "Escocia", 1)] 

	assert not obtenerNombrePaisSeleccionado(paises, codigo_pais)

@pytest.mark.parametrize(["codigo_pais", "nombre_pais"],
	[
		("es", "España"),
		("pt", "Portugal"),
		("ss", "Escocia"),
		("nl", "Países Bajos"),
		("it", "Italia")
	]
)
def test_obtener_nombre_pais_seleccionado_no_esta(codigo_pais, nombre_pais):

	paises=[("es", "España", 12), ("it", "Italia", 1), ("nl", "Países Bajos", 1),
			("pt", "Portugal", 1), ("ss", "Escocia", 1)] 

	assert obtenerNombrePaisSeleccionado(paises, codigo_pais)==nombre_pais

def test_obtener_paises_no_seleccionados_no_existen():

	assert not obtenerPaisesNoSeleccionados([], "es")

def test_obtener_paises_no_seleccionados_solo_pais():

	paises=[("es", "España", 12)] 

	assert not obtenerPaisesNoSeleccionados(paises, "es")

@pytest.mark.parametrize(["codigo_pais"],
	[("es",),("pt",),("ss",),("nl",),("it",)]
)
def test_obtener_paises_no_seleccionados(codigo_pais):

	paises=[("es", "España", 12), ("it", "Italia", 1), ("nl", "Países Bajos", 1),
			("pt", "Portugal", 1), ("ss", "Escocia", 1)] 

	paises_no_seleccionados=obtenerPaisesNoSeleccionados(paises, codigo_pais)

	assert len(paises_no_seleccionados)

def test_crear_carpeta_no_existe():

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

	assert not os.path.exists(ruta_carpeta)

	crearCarpeta(ruta_carpeta)

	assert os.path.exists(ruta_carpeta)

def test_crear_carpeta_existe():

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

	assert os.path.exists(ruta_carpeta)

	crearCarpeta(ruta_carpeta)

	assert os.path.exists(ruta_carpeta)

	os.rmdir(ruta_carpeta)

def test_borrar_carpeta_no_existe():

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

	assert not os.path.exists(ruta_carpeta)

	borrarCarpeta(ruta_carpeta)

	assert not os.path.exists(ruta_carpeta)

def test_borrar_carpeta_existe():

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

	crearCarpeta(ruta_carpeta)

	assert os.path.exists(ruta_carpeta)

	borrarCarpeta(ruta_carpeta)

	assert not os.path.exists(ruta_carpeta)

def test_vaciar_carpeta_vacia():

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

	crearCarpeta(ruta_carpeta)

	assert not os.listdir(ruta_carpeta)

	vaciarCarpeta(ruta_carpeta)

	assert not os.listdir(ruta_carpeta)

def crearHTML(ruta:str)->None:

	contenido="""
			<!DOCTYPE html>
			<html>
			<head>
			    <title>Mi Archivo HTML</title>
			</head>
			<body>
			    <h1>Hola, este es mi archivo HTML creado con Python</h1>
			</body>
			</html>
			"""

	with open(ruta, "w") as html:

	    html.write(contenido)

def test_vaciar_carpeta_llena():

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

	assert not os.listdir(ruta_carpeta)

	ruta_html=os.path.join(ruta_carpeta, "html.html")

	crearHTML(ruta_html)

	assert os.listdir(ruta_carpeta)

	vaciarCarpeta(ruta_carpeta)

	assert not os.listdir(ruta_carpeta)

	borrarCarpeta(ruta_carpeta)

@pytest.mark.parametrize(["numero_archivos"],
	[(1,),(3,),(7,),(4,),(13,)]
)
def test_vaciar_carpeta_llena_varios(numero_archivos):

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

	crearCarpeta(ruta_carpeta)

	assert not os.listdir(ruta_carpeta)

	for numero in range(numero_archivos):

		ruta_html=os.path.join(ruta_carpeta, f"html{numero}.html")

		crearHTML(ruta_html)

	assert len(os.listdir(ruta_carpeta))==numero_archivos

	vaciarCarpeta(ruta_carpeta)

	assert not os.listdir(ruta_carpeta)

def test_vaciar_carpeta_mapas_usuario_vacia():

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

	assert not os.listdir(ruta_carpeta)

	vaciarCarpetaMapasUsuario(ruta_carpeta, "golden")

	assert not os.listdir(ruta_carpeta)

def test_vaciar_carpeta_mapas_usuario_llena_archivo_usuario():

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

	assert not os.listdir(ruta_carpeta)

	ruta_html=os.path.join(ruta_carpeta, "html_golden.html")

	crearHTML(ruta_html)

	assert os.listdir(ruta_carpeta)

	vaciarCarpetaMapasUsuario(ruta_carpeta, "golden")

	assert not os.listdir(ruta_carpeta)

def test_vaciar_carpeta_mapas_usuario_llena_archivo_otro_usuario():

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

	assert not os.listdir(ruta_carpeta)

	ruta_html=os.path.join(ruta_carpeta, "html_otro.html")

	crearHTML(ruta_html)

	assert os.listdir(ruta_carpeta)

	vaciarCarpetaMapasUsuario(ruta_carpeta, "golden")

	assert os.listdir(ruta_carpeta)

	vaciarCarpeta(ruta_carpeta)

	borrarCarpeta(ruta_carpeta)

@pytest.mark.parametrize(["numero_archivos_usuario"],
	[(1,),(3,),(7,),(4,),(13,)]
)
def test_vaciar_carpeta_mapas_usuario_llena_archivos_ambos(numero_archivos_usuario):

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

	crearCarpeta(ruta_carpeta)

	assert not os.listdir(ruta_carpeta)

	for numero in range(numero_archivos_usuario):

		ruta_html=os.path.join(ruta_carpeta, f"html_golden{numero}.html")

		crearHTML(ruta_html)

	for numero in range(numero_archivos_usuario+2):

		ruta_html=os.path.join(ruta_carpeta, f"html_otro{numero}.html")

		crearHTML(ruta_html)

	assert len(os.listdir(ruta_carpeta))==numero_archivos_usuario+numero_archivos_usuario+2

	vaciarCarpetaMapasUsuario(ruta_carpeta, "golden")

	assert len(os.listdir(ruta_carpeta))==numero_archivos_usuario+2

	for archivo in os.listdir(ruta_carpeta):

		assert not archivo.startswith("html_golden")
		assert archivo.startswith("html_otro")

	vaciarCarpeta(ruta_carpeta)

	borrarCarpeta(ruta_carpeta)

def test_obtener_centroide_sin_puntos():

	with pytest.raises(Exception):

		obtenerCentroide([])

@pytest.mark.parametrize(["latitud", "longitud"],
	[
		(40.01, -3.45),
		(30.11, -21.45),
		(1.01, 9.86),
		(-2.34, 40.04),
	]
)
def test_obtener_centroide_un_punto(latitud, longitud):

	assert obtenerCentroide([("Estadio", latitud, longitud, 1, "1")])==(latitud, longitud)

def test_obtener_centroide_puntos_limites():

	estadios=[("Estadio", 90.0, 180.0, 1, "1"),
				("Estadio", -90.0, -180.0, 1, "1")]

	assert obtenerCentroide(estadios)==pytest.approx((0.0, 0.0))

def test_obtener_centroide():

	estadios=[("Estadio", 40.0, -3.0, 1, "1"),
				("Estadio", 41.0, -2.0, 1, "1"),
				("Estadio", 42.0, -4.0, 1, "1")]

	centroide=((40.0+41.0+42.0)/3, (-3.0+-2.0+-4.0)/3)

	assert obtenerCentroide(estadios)==pytest.approx(centroide)

def test_obtener_centroide_datos_reales():

    estadios=[("Estadio Santiago Bernabéu", 40.453054, -3.688344, 1, "1"),
        		("Camp Nou", 41.380898, 2.122820, 1, "1"),
		        ("Estadio Ramón Sánchez-Pizjuán", 37.384049, -5.970579, 1, "1"),
		        ("Estadio de Mestalla", 39.474574, -0.358355, 1, "1"),
		        ("San Mamés", 43.264130, -2.949721, 1, "1"),
		        ("Estadio de Gran Canaria", 28.099731, -15.451081, 1, "1")]

    centroide=((40.453054+41.380898+37.384049+39.474574+43.264130+28.099731)/6,
        		(-3.688344+2.122820+-5.970579+-0.358355+-2.949721+-15.451081)/6)

    assert obtenerCentroide(estadios) == pytest.approx(centroide)

def test_crear_mapa_mis_estadios_sin_puntos():

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

	crearCarpeta(ruta_carpeta)

	vaciarCarpeta(ruta_carpeta)

	ruta_html=os.path.join(ruta_carpeta, "nacho_mapa.html")

	assert not os.path.exists(ruta_html)

	crearMapaMisEstadios(ruta_carpeta, [], "nacho_mapa.html")

	assert os.path.exists(ruta_html)

	with open(ruta_html, "r") as html:

		contenido=html.read()

		assert '<div class="folium-map" id="map_' in contenido
		assert "var map_" in contenido
		assert "L.map" in contenido
		assert "var circle_" not in contenido
		assert "L.circle" not in contenido

	vaciarCarpeta(ruta_carpeta)

	borrarCarpeta(ruta_carpeta)

@pytest.mark.parametrize(["latitud", "longitud"],
	[
		(40.01, -3.45),
		(30.11, -21.45),
		(1.01, 9.86),
		(-2.34, 40.04),
	]
)
def test_crear_mapa_mis_estadios(latitud, longitud):

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

	crearCarpeta(ruta_carpeta)

	vaciarCarpeta(ruta_carpeta)

	ruta_html=os.path.join(ruta_carpeta, "nacho_mapa.html")

	assert not os.path.exists(ruta_html)

	crearMapaMisEstadios(ruta_carpeta, [("Estadio", latitud, longitud, 1, "1")], "nacho_mapa.html")

	assert os.path.exists(ruta_html)

	with open(ruta_html, "r") as html:

		contenido=html.read()

		assert '<div class="folium-map" id="map_' in contenido
		assert "var map_" in contenido
		assert "L.map" in contenido
		assert "var circle_" in contenido
		assert "L.circle" in contenido
		assert f"[{latitud}, {longitud}]" in contenido

	vaciarCarpeta(ruta_carpeta)

	borrarCarpeta(ruta_carpeta)

def test_crear_mapa_mis_estadios_detalle_sin_puntos():

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

	crearCarpeta(ruta_carpeta)

	vaciarCarpeta(ruta_carpeta)

	ruta_html=os.path.join(ruta_carpeta, "nacho_mapa_detalle.html")

	assert not os.path.exists(ruta_html)

	crearMapaMisEstadiosDetalle(ruta_carpeta, [], "nacho_mapa_detalle.html")

	assert os.path.exists(ruta_html)

	with open(ruta_html, "r") as html:

		contenido=html.read()

		assert '<div class="folium-map" id="map_' in contenido
		assert "var map_" in contenido
		assert "L.map" in contenido
		assert "var marker_" not in contenido
		assert "L.marker" not in contenido

	vaciarCarpeta(ruta_carpeta)

	borrarCarpeta(ruta_carpeta)

@pytest.mark.parametrize(["latitud", "longitud"],
	[
		(40.01, -3.45),
		(30.11, -21.45),
		(1.01, 9.86),
		(-2.34, 40.04),
	]
)
def test_crear_mapa_mis_estadios_detalle(latitud, longitud):

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

	crearCarpeta(ruta_carpeta)

	vaciarCarpeta(ruta_carpeta)

	ruta_html=os.path.join(ruta_carpeta, "nacho_mapa_detalle.html")

	assert not os.path.exists(ruta_html)

	crearMapaMisEstadiosDetalle(ruta_carpeta, [("Nombre Estadio", latitud, longitud, 220619, "pais_icono")], "nacho_mapa_detalle.html")

	assert os.path.exists(ruta_html)

	with open(ruta_html, "r") as html:

		contenido=html.read()

		assert '<div class="folium-map" id="map_' in contenido
		assert "var map_" in contenido
		assert "L.map" in contenido
		assert "var marker_" in contenido
		assert "L.marker" in contenido
		assert f"[{latitud}, {longitud}]" in contenido
		assert "Nombre Estadio" in contenido
		assert "220619.png" in contenido
		assert "pais_icono.png" in contenido
		assert "/static/imagenes/iconos/estadio_mapa.png" in contenido

	vaciarCarpeta(ruta_carpeta)

	borrarCarpeta(ruta_carpeta)

def test_leer_geojson_paises_error():

	ruta_relativa=os.path.join(os.path.abspath(".."), "src", "static")

	with pytest.raises(Exception):

		leerGeoJSON(ruta_relativa)

def test_leer_geojson_paises():

	ruta_relativa=os.path.join(os.path.abspath(".."), "src", "static", "geojson")

	geodataframe=leerGeoJSON(ruta_relativa)

	assert not geodataframe.empty
	assert isinstance(geodataframe, gpd.geodataframe.GeoDataFrame)

def test_obtener_geometria_pais_error():

	ruta_relativa=os.path.join(os.path.abspath(".."), "src", "static")

	with pytest.raises(Exception):

		obtenerGeometriaPais(ruta_relativa, 40.4168, -3.7038)

def test_obtener_geometria_pais_no_existen():

	ruta_relativa=os.path.join(os.path.abspath(".."), "src", "static", "geojson")

	geodataframe=obtenerGeometriaPais(ruta_relativa, 0, 0)

	assert geodataframe.empty
	assert isinstance(geodataframe, gpd.geodataframe.GeoDataFrame)

@pytest.mark.parametrize(["latitud", "longitud", "pais"],
    [
        (40.4168, -3.7038, "Spain"),
        (48.8566, 2.3522, "France"), 
        (51.5074, -0.1278, "England"),
        (39.5696, 2.6502, "Spain-Mallorca"),
        (28.1235, -15.4363, "Spain-LasPalmas"),
        (41.9028, 12.4964, "Italy")
    ]
)
def test_obtener_geometria_pais(latitud, longitud, pais):

	ruta_relativa=os.path.join(os.path.abspath(".."), "src", "static", "geojson")

	geodataframe=obtenerGeometriaPais(ruta_relativa, latitud, longitud)

	assert not geodataframe.empty
	assert isinstance(geodataframe, gpd.geodataframe.GeoDataFrame)
	assert geodataframe["name"].iloc[0]==pais

def test_obtener_geometrias_paises_error():

	ruta_relativa=os.path.join(os.path.abspath(".."), "src", "static")

	with pytest.raises(Exception):

		obtenerGeometriasPaises(ruta_relativa, [(40.4168, -3.7038)])

def test_obtener_geometrias_paises_error_puntos():

	ruta_relativa=os.path.join(os.path.abspath(".."), "src", "static", "geojson")

	with pytest.raises(Exception):

		obtenerGeometriasPaises(ruta_relativa, [])

def test_obtener_geometrias_paises_no_existen():

	ruta_relativa=os.path.join(os.path.abspath(".."), "src", "static", "geojson")

	geodataframe=obtenerGeometriasPaises(ruta_relativa, [(0, 0)])

	assert geodataframe.empty
	assert isinstance(geodataframe, gpd.geodataframe.GeoDataFrame)

def test_obtener_geometrias_paises():

	ruta_relativa=os.path.join(os.path.abspath(".."), "src", "static", "geojson")

	coordenadas=[(40.4168, -3.7038),(48.8566, 2.3522),(51.5074, -0.1278),(39.5696, 2.6502),
        		(28.1235, -15.4363),(41.9028, 12.4964)]

	geodataframe=obtenerGeometriasPaises(ruta_relativa, coordenadas)

	assert not geodataframe.empty
	assert isinstance(geodataframe, gpd.geodataframe.GeoDataFrame)
	assert len(geodataframe)==6

def test_obtener_geometrias_paises_mismo_pais():

	ruta_relativa=os.path.join(os.path.abspath(".."), "src", "static", "geojson")

	coordenadas=[(40.4168, -3.7038),(41.4168, -4.7039),(41.2168, -4.1039),(39.4168, -4.7039)]

	geodataframe=obtenerGeometriasPaises(ruta_relativa, coordenadas)

	assert not geodataframe.empty
	assert isinstance(geodataframe, gpd.geodataframe.GeoDataFrame)
	assert len(geodataframe)==1

def test_crear_mapa_mis_estadios_detalle_paises_error():

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

	crearCarpeta(ruta_carpeta)

	vaciarCarpeta(ruta_carpeta)

	ruta_html=os.path.join(ruta_carpeta, "nacho_mapa.html")

	assert not os.path.exists(ruta_html)

	with pytest.raises(Exception):

		crearMapaMisEstadiosDetallePaises(ruta_carpeta, [], "nacho_mapa.html")

	assert not os.path.exists(ruta_html)

	borrarCarpeta(ruta_carpeta)

def test_crear_mapa_mis_estadios_detalle_paises_sin_puntos():

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

	crearCarpeta(ruta_carpeta)

	vaciarCarpeta(ruta_carpeta)

	ruta_html=os.path.join(ruta_carpeta, "nacho_mapa.html")

	assert not os.path.exists(ruta_html)

	crearMapaMisEstadiosDetallePaises(ruta_carpeta, [(0.0, 0.0)], "nacho_mapa.html")

	assert os.path.exists(ruta_html)

	with open(ruta_html, "r") as html:

		contenido=html.read()

		assert '<div class="folium-map" id="map_' in contenido
		assert "var map_" in contenido
		assert "L.map" in contenido
		assert "var geo_json_" in contenido
		assert "function geo_json_" in contenido
		assert '"bbox": [NaN, NaN, NaN, NaN]' in contenido
		assert '"features": []' in contenido
		assert '"type": "FeatureCollection"' in contenido

	vaciarCarpeta(ruta_carpeta)

	borrarCarpeta(ruta_carpeta)

def test_crear_mapa_mis_estadios_detalle_paises_con_punto():

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

	crearCarpeta(ruta_carpeta)

	vaciarCarpeta(ruta_carpeta)

	ruta_html=os.path.join(ruta_carpeta, "nacho_mapa.html")

	assert not os.path.exists(ruta_html)

	crearMapaMisEstadiosDetallePaises(ruta_carpeta, [(40.01, -3.45)], "nacho_mapa.html")

	assert os.path.exists(ruta_html)

	with open(ruta_html, "r") as html:

		contenido=html.read()

		assert '<div class="folium-map" id="map_' in contenido
		assert "var map_" in contenido
		assert "L.map" in contenido
		assert "var geo_json_" in contenido
		assert "function geo_json_" in contenido
		assert '"bbox": [NaN, NaN, NaN, NaN]' not in contenido
		assert '"features": []' not in contenido
		assert '"type": "FeatureCollection"' in contenido
		assert '{"name": "Spain"}' in contenido

	vaciarCarpeta(ruta_carpeta)

	borrarCarpeta(ruta_carpeta)

@pytest.mark.parametrize(["latitud", "longitud", "pais"],
    [
        (40.4168, -3.7038, "Spain"),
        (48.8566, 2.3522, "France"), 
        (51.5074, -0.1278, "England"),
        (39.5696, 2.6502, "Spain-Mallorca"),
        (28.1235, -15.4363, "Spain-LasPalmas"),
        (41.9028, 12.4964, "Italy")
    ]
)
def test_crear_mapa_mis_estadios_detalle_paises_con_punto_paises(latitud, longitud, pais):

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

	crearCarpeta(ruta_carpeta)

	vaciarCarpeta(ruta_carpeta)

	ruta_html=os.path.join(ruta_carpeta, "nacho_mapa.html")

	assert not os.path.exists(ruta_html)

	crearMapaMisEstadiosDetallePaises(ruta_carpeta, [(latitud, longitud)], "nacho_mapa.html")

	assert os.path.exists(ruta_html)

	with open(ruta_html, "r") as html:

		contenido=html.read()

		assert '<div class="folium-map" id="map_' in contenido
		assert "var map_" in contenido
		assert "L.map" in contenido
		assert "var geo_json_" in contenido
		assert "function geo_json_" in contenido
		assert '"bbox": [NaN, NaN, NaN, NaN]' not in contenido
		assert '"features": []' not in contenido
		assert '"type": "FeatureCollection"' in contenido
		assert '{"name": "'+pais+'"}' in contenido

	vaciarCarpeta(ruta_carpeta)

	borrarCarpeta(ruta_carpeta)

def test_crear_mapa_mis_estadios_detalle_paises_con_puntos():

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

	crearCarpeta(ruta_carpeta)

	vaciarCarpeta(ruta_carpeta)

	ruta_html=os.path.join(ruta_carpeta, "nacho_mapa.html")

	assert not os.path.exists(ruta_html)

	coordenadas=[(40.4168, -3.7038),(48.8566, 2.3522),(41.9028, 12.4964),(51.5074, -0.1278)]

	crearMapaMisEstadiosDetallePaises(ruta_carpeta, coordenadas, "nacho_mapa.html")

	assert os.path.exists(ruta_html)

	with open(ruta_html, "r") as html:

		contenido=html.read()

		assert '<div class="folium-map" id="map_' in contenido
		assert "var map_" in contenido
		assert "L.map" in contenido
		assert "var geo_json_" in contenido
		assert "function geo_json_" in contenido
		assert '"bbox": [NaN, NaN, NaN, NaN]' not in contenido
		assert '"features": []' not in contenido
		assert '"type": "FeatureCollection"' in contenido
		assert '{"name": "Spain"}' in contenido
		assert '{"name": "France"}' in contenido
		assert '{"name": "Italy"}' in contenido
		assert '{"name": "England"}' in contenido

	vaciarCarpeta(ruta_carpeta)

	borrarCarpeta(ruta_carpeta)

def test_crear_mapa_estadio_sin_punto_error():

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

	crearCarpeta(ruta_carpeta)

	vaciarCarpeta(ruta_carpeta)

	ruta_html=os.path.join(ruta_carpeta, "nacho_mapa_estadio.html")

	assert not os.path.exists(ruta_html)

	with pytest.raises(Exception):

		crearMapaEstadio(ruta_carpeta, (0, 1, 2, None, None), "nacho_mapa_estadio.html")

	assert not os.path.exists(ruta_html)

	borrarCarpeta(ruta_carpeta)

@pytest.mark.parametrize(["latitud", "longitud"],
	[
		(40.01, -3.45),
		(30.11, -21.45),
		(1.01, 9.86),
		(-2.34, 40.04),
	]
)
def test_crear_mapa_estadio(latitud, longitud):

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

	crearCarpeta(ruta_carpeta)

	vaciarCarpeta(ruta_carpeta)

	ruta_html=os.path.join(ruta_carpeta, "nacho_mapa_estadio.html")

	assert not os.path.exists(ruta_html)

	crearMapaEstadio(ruta_carpeta, (0, 1, 2, latitud, longitud, 220619, "pais_icono"), "nacho_mapa_estadio.html")

	assert os.path.exists(ruta_html)

	with open(ruta_html, "r") as html:

		contenido=html.read()

		assert '<div class="folium-map" id="map_' in contenido
		assert "var map_" in contenido
		assert "L.map" in contenido
		assert "var marker_" in contenido
		assert "L.marker" in contenido
		assert f"[{latitud}, {longitud}]" in contenido
		assert "/static/imagenes/iconos/estadio_mapa.png" in contenido

	vaciarCarpeta(ruta_carpeta)

	borrarCarpeta(ruta_carpeta)

def test_obtener_competiciones_unicas_no_hay():

	competiciones_unicas=obtenerCompeticionesPartidosUnicas([])

	assert len(competiciones_unicas)==1
	assert competiciones_unicas[0]=="Todo"

def test_obtener_competiciones_unicas_repetidas():

	partidos=[(0,1,2,3,4,5,6,7,8,"Primera") for numero_partidos in range(10)]

	competiciones_unicas=obtenerCompeticionesPartidosUnicas(partidos)

	assert len(competiciones_unicas)==2

def test_obtener_competiciones_unicas():

	partidos=[(0,1,2,3,4,5,6,7,8,"Primera"),(0,1,2,3,4,5,6,7,8,"Segunda"), (0,1,2,3,4,5,6,7,8,"Champions"),
				(0,1,2,3,4,5,6,7,8,"Copa"),(0,1,2,3,4,5,6,7,8,"Mundial"),(0,1,2,3,4,5,6,7,8,"Eurocopa")]

	competiciones_unicas=obtenerCompeticionesPartidosUnicas(partidos)

	assert len(competiciones_unicas)==7

@pytest.mark.parametrize(["archivo", "extension"],
	[
		("mipdf.pdf", "pdf"),
		("miimagen.jpeg", "jpeg"),
		("imagen", "jpg"),
		("mitxt.txt", "txt"),
	]
)
def test_extraer_extension(archivo, extension):

	assert extraerExtension(archivo)==extension

@pytest.mark.parametrize(["fecha_ida", "fecha_vuelta"],
	[
		("201811-01", "2019-06-23"),
		("2018-11-01", "2019-0623"),
		("01-11-2018", "2019-06-23"),
		("2018-11-01", "23-06-2019"),
		("2018-11-01", "2019-06-21"),
		("2019-06-23", "2019-06-24"),
		("2019-06-24", "2019-06-23")
	]
)
def test_comprobar_fechas_fechas_invalidas(fecha_ida, fecha_vuelta):

	assert not comprobarFechas(fecha_ida, fecha_vuelta, "2019-06-22")

@pytest.mark.parametrize(["fecha_ida", "fecha_vuelta"],
	[
		("2018-11-01", "2019-06-22"),
		("2019-06-22", "2019-06-24"),
		("2019-06-21", "2019-06-23")
	]
)
def test_comprobar_fechas_fechas_validas(fecha_ida, fecha_vuelta):

	assert comprobarFechas(fecha_ida, fecha_vuelta, "2019-06-22")

@pytest.mark.parametrize(["ano_mes"],
	[("202211",),("2019-13",),("11-2022",),("2019",),("06",)]
)
def test_obtener_primer_ultimo_dia_ano_mes_fechas_invalidas(ano_mes):

	assert not obtenerPrimerUltimoDiaAnoMes(ano_mes)

@pytest.mark.parametrize(["ano_mes", "primer_dia", "ultimo_dia"],
	[
		("2022-11", "2022-11-01", "2022-11-30"),
		("2019-12", "2019-12-01", "2019-12-31"),
		("2019-06", "2019-06-01", "2019-06-30"),
		("2025-02", "2025-02-01", "2025-02-28")
	]
)
def test_obtener_primer_ultimo_dia_ano_mes(ano_mes, primer_dia, ultimo_dia):

	primer_ultimo_dia=obtenerPrimerUltimoDiaAnoMes(ano_mes)

	assert primer_ultimo_dia[0]==primer_dia
	assert primer_ultimo_dia[1]==ultimo_dia

@pytest.mark.parametrize(["ano_mes"],
	[("202211",),("2019-13",),("11-2022",),("2019",),("06",)]
)
def test_mapear_ano_mes_fechas_invalidas(ano_mes):

	assert not mapearAnoMes(ano_mes)

@pytest.mark.parametrize(["ano_mes", "mapeo"],
	[
		("2022-11", "Noviembre 2022"),
		("2019-12", "Diciembre 2019"),
		("2019-06", "Junio 2019"),
		("2025-02", "Febrero 2025")
	]
)
def test_mapear_ano_mes(ano_mes, mapeo):

	assert mapearAnoMes(ano_mes)==mapeo

@pytest.mark.parametrize(["fecha_inicio", "fecha_fin"],
	[
		("201811-01", "2019-06-23"),
		("2018-11-01", "2019-0623"),
		("01-11-2018", "2019-06-23"),
		("2018-11-01", "23-06-2019"),
		("2019-06-22", "2019-04-13")
	]
)
def test_obtener_ano_mes_fechas_fechas_invalidas(fecha_inicio, fecha_fin):

	assert not obtenerAnoMesFechas(fecha_inicio, fecha_fin)

@pytest.mark.parametrize(["fecha_inicio", "fecha_fin", "ano_mes"],
	[
		("2019-06-13", "2019-06-22", ["2019-06", "Junio 2019"]),
		("2019-08-06", "2019-08-15", ["2019-08", "Agosto 2019"]),
		("1998-02-15", "1998-02-16", ["1998-02", "Febrero 1998"])
	]
)
def test_obtener_ano_mes_fechas_mismo_mes(fecha_inicio, fecha_fin, ano_mes):

	anos_meses=obtenerAnoMesFechas(fecha_inicio, fecha_fin)

	assert anos_meses[0]==ano_mes

@pytest.mark.parametrize(["fecha_inicio", "fecha_fin", "rango_anos_meses"],
	[
		("2019-04-13", "2019-06-22", [["2019-04", "Abril 2019"], ["2019-05", "Mayo 2019"], ["2019-06", "Junio 2019"]]),
		("2019-02-01", "2019-03-05", [["2019-02", "Febrero 2019"], ["2019-03", "Marzo 2019"]]),
		("2020-02-16", "2020-03-15", [["2020-02", "Febrero 2020"], ["2020-03", "Marzo 2020"]]),
		("2019-11-22", "2020-02-16", [["2019-11", "Noviembre 2019"], ["2019-12", "Diciembre 2019"], ["2020-01", "Enero 2020"], ["2020-02", "Febrero 2020"]]),
	]
)
def test_obtener_ano_mes_fechas(fecha_inicio, fecha_fin, rango_anos_meses):

	anos_meses=obtenerAnoMesFechas(fecha_inicio, fecha_fin)

	assert len(anos_meses)==len(rango_anos_meses)

	for ano_mes in anos_meses:

		assert ano_mes in rango_anos_meses

@pytest.mark.parametrize(["fecha_inicio", "fecha_fin"],
	[
		("201811-01", "2019-06-23"),
		("2018-11-01", "2019-0623"),
		("01-11-2018", "2019-06-23"),
		("2018-11-01", "23-06-2019")
	]
)
def test_generar_calendario_fechas_invalidas(fecha_inicio, fecha_fin):

	assert not generarCalendario(fecha_inicio, fecha_fin)

def test_generar_calendario_fechas_inversa():

	semanas=generarCalendario("2019-06-22", "2019-04-13")

	for semana in semanas:

		for dia in semana:

			assert dia==""

def test_generar_calendario():

	semanas=generarCalendario("2019-06-13", "2019-06-22")

	assert len(semanas)==2
	assert "" in semanas[0]
	assert "" in semanas[1]

def test_cruzar_partidos_calendario_sin_calendario():

	assert not cruzarPartidosCalendario([], [])

def test_cruzar_partidos_calendario_sin_partidos():

	semanas=generarCalendario("2019-06-01", "2019-06-30")

	partidos_calendario=cruzarPartidosCalendario([], semanas)

	partidos_filtrados= [[valor for valor in sublista if isinstance(valor, tuple) and valor[2] is not None] for sublista in partidos_calendario]

	assert not [sublista for sublista in partidos_filtrados if sublista]

@pytest.mark.parametrize(["fechas_partidos", "numero_partidos"],
	[
		(["2019-06-22", "2019-06-06", "2019-06-13", "2019-06-30"], 4),
		(["2019-07-22", "2019-06-06", "2019-06-13", "2019-06-30"], 3),
		(["2020-06-22", "2019-06-06", "2019-06-13", "2019-06-31"], 2),
		(["2019-06-22", "2019-06-06"], 2)
	]
)
def test_cruzar_partidos_calendario(fechas_partidos, numero_partidos):

	partidos=[["id", "1-0", "22/06/2019", fecha] for fecha in fechas_partidos]

	semanas=generarCalendario("2019-06-01", "2019-06-30")

	partidos_calendario=cruzarPartidosCalendario(partidos, semanas)

	partidos_filtrados= [[valor for valor in sublista if isinstance(valor, tuple) and valor[2] is not None] for sublista in partidos_calendario]

	partidos_existen=[sublista for sublista in partidos_filtrados if sublista]

	assert len(partidos_existen)==numero_partidos

@pytest.mark.parametrize(["ano_mes"],
	[("202211",),("2019-13",),("11-2022",),("2019",),("06",)]
)
def test_ano_mes_anterior_fechas_invalidas(ano_mes):

	assert not ano_mes_anterior(ano_mes)

@pytest.mark.parametrize(["ano_mes", "anterior"],
	[
		("2022-11", "2022-10"),
		("2019-12", "2019-11"),
		("2019-06", "2019-05"),
		("2025-01", "2024-12")
	]
)
def test_ano_mes_anterior(ano_mes, anterior):

	assert ano_mes_anterior(ano_mes)==anterior

@pytest.mark.parametrize(["ano_mes"],
	[("202211",),("2019-13",),("11-2022",),("2019",),("06",)]
)
def test_ano_mes_siguiente_fechas_invalidas(ano_mes):

	assert not ano_mes_siguiente(ano_mes)

@pytest.mark.parametrize(["ano_mes", "siguiente"],
	[
		("2022-11", "2022-12"),
		("2019-12", "2020-01"),
		("2019-06", "2019-07"),
		("2025-01", "2025-02")
	]
)
def test_ano_mes_siguiente(ano_mes, siguiente):

	assert ano_mes_siguiente(ano_mes)==siguiente

def test_limpiar_resultados_partidos_calendario_no_hay():

	resultados=limpiarResultadosPartidosCalendario([])

	assert isinstance(resultados, dict)
	assert resultados["ganados"]==0
	assert resultados["perdidos"]==0
	assert resultados["empatados"]==0

@pytest.mark.parametrize(["partidos", "ganados", "perdidos", "empatados"],
	[
		([(1, 0, 0, "-"), (0, 0, 1, "-"), (1, 0, 0, "-"), (0, 1, 0, "-"), (1, 0, 0, "-"), (1, 0, 0, "-")], 4, 1, 1),
		([(0, 0, 0, "-"), (0, 0, 1, "-"), (1, 0, 0, "-"), (0, 1, 0, "-"), (1, 0, 0, "-"), (1, 0, 0, "-")], 3, 1, 1),
		([(1, 0, 0, "-"), (0, 0, 1, "-"), (1, 0, 0, "-"), (0, 1, 0, "-"), (1, 0, 0, "-")], 3, 1, 1),
		([(1, 0, 0, "-"), (0, 0, 1, "-"), (0, 1, 0, "-"), (0, 1, 0, "-"), (0, 1, 0, "-"), (1, 0, 0, "-")], 2, 3, 1),
		([(1, 1, 1, "-"), (0, 0, 1, "-"), (1, 0, 0, "-"), (0, 1, 0, "-"), (1, 0, 0, "-"), (1, 0, 0, "-")], 4, 2, 2),
	]
)
def test_limpiar_resultados_partidos_calendario(partidos, ganados, perdidos, empatados):

	resultados=limpiarResultadosPartidosCalendario(partidos)

	assert isinstance(resultados, dict)
	assert resultados["ganados"]==ganados
	assert resultados["perdidos"]==perdidos
	assert resultados["empatados"]==empatados

@pytest.mark.parametrize(["codigo_ciudad_ida", "codigo_ciudad_vuelta", "ciudad_ida_estadio", "ciudad_vuelta_estadio", "ciudad_estadio_partido", "transporte_ida", "transporte_vuelta"],
	[
		(None, 2, "Madrid", "Madrid", "Madrid", "Avion", "Avion"),
		(1, None, "Madrid", "Madrid", "Madrid",  "Avion", "Avion"),
		(1, 2, "Otra", "Madrid", "Madrid",  "Avion", "Avion"),
		(1, 2, "Madrid", "Otra", "Madrid",  "Avion", "Avion"),
		(1, 2, "Madrid", "Madrid", "Otra",  "Avion", "Avion"),
		(1, 2, "Madrid", "Madrid", "Madrid",  "transporte", "Avion"),
		(1, 2, "Madrid", "Madrid", "Madrid", "Avion", "transporte")
	]
)
def test_datos_trayectos_correctos_no_correctos(codigo_ciudad_ida, codigo_ciudad_vuelta, ciudad_ida_estadio, ciudad_vuelta_estadio, ciudad_estadio_partido, transporte_ida, transporte_vuelta):

	assert not datos_trayectos_correctos(codigo_ciudad_ida, codigo_ciudad_vuelta, ciudad_ida_estadio, ciudad_vuelta_estadio, ciudad_estadio_partido, transporte_ida, transporte_vuelta)

@pytest.mark.parametrize(["codigo_ciudad_ida", "codigo_ciudad_vuelta", "ciudad_ida_estadio", "ciudad_vuelta_estadio", "ciudad_estadio_partido", "transporte_ida", "transporte_vuelta"],
	[
		(1, 2, "Madrid", "Madrid", "Madrid",  "Autobus", "Avion"),
		(2, 2, "Madrid", "Madrid", "Madrid",  "Avion", "Avion"),
		(1, 2, "Otra", "Otra", "Otra",  "Avion", "Tren"),
		(1, 2, "Otra", "Otra", "Otra",  "Coche", "Coche")
	]
)
def test_datos_trayectos_correctos(codigo_ciudad_ida, codigo_ciudad_vuelta, ciudad_ida_estadio, ciudad_vuelta_estadio, ciudad_estadio_partido, transporte_ida, transporte_vuelta):

	assert datos_trayectos_correctos(codigo_ciudad_ida, codigo_ciudad_vuelta, ciudad_ida_estadio, ciudad_vuelta_estadio, ciudad_estadio_partido, transporte_ida, transporte_vuelta)

def test_obtener_centroide_coordenadas_sin_puntos():

	with pytest.raises(Exception):

		obtenerCentroideCoordenadas([])

@pytest.mark.parametrize(["latitud", "longitud"],
	[
		(40.01, -3.45),
		(30.11, -21.45),
		(1.01, 9.86),
		(-2.34, 40.04),
	]
)
def test_obtener_centroide_coordenadas_un_punto(latitud, longitud):

	assert obtenerCentroideCoordenadas([(latitud, longitud)])==(latitud, longitud)

def test_obtener_centroide_coordenadas_puntos_limites():

	coordenadas=[(90.0, 180.0),(-90.0, -180.0)]

	assert obtenerCentroideCoordenadas(coordenadas)==pytest.approx((0.0, 0.0))

def test_obtener_centroide_coordenadas():

	coordenadas=[(40.0, -3.0),(41.0, -2.0),(42.0, -4.0)]

	centroide=((40.0+41.0+42.0)/3, (-3.0+-2.0+-4.0)/3)

	assert obtenerCentroideCoordenadas(coordenadas)==pytest.approx(centroide)

def test_obtener_centroide_coordenadas_datos_reales():

    coordenadas=[(40.453054, -3.688344),(41.380898, 2.122820),(37.384049, -5.970579),
		        (39.474574, -0.358355),(43.264130, -2.949721),(28.099731, -15.451081)]

    centroide=((40.453054+41.380898+37.384049+39.474574+43.264130+28.099731)/6,
        		(-3.688344+2.122820+-5.970579+-0.358355+-2.949721+-15.451081)/6)

    assert obtenerCentroideCoordenadas(coordenadas)==pytest.approx(centroide)

def test_crear_mapa_trayecto_sin_punto_error():

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

	crearCarpeta(ruta_carpeta)

	vaciarCarpeta(ruta_carpeta)

	ruta_html=os.path.join(ruta_carpeta, "nacho_mapa_trayecto.html")

	assert not os.path.exists(ruta_html)

	with pytest.raises(Exception):

		crearMapaTrayecto(ruta_carpeta, ('I', 'Transporte', 'Madrid', None, None, 'Metropolitano', None, None), "nacho_mapa_trayecto.html")

	assert not os.path.exists(ruta_html)

	borrarCarpeta(ruta_carpeta)

def test_crear_mapa_trayecto_tipo_error():

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

	crearCarpeta(ruta_carpeta)

	vaciarCarpeta(ruta_carpeta)

	ruta_html=os.path.join(ruta_carpeta, "nacho_mapa_trayecto.html")

	assert not os.path.exists(ruta_html)

	with pytest.raises(Exception):

		crearMapaTrayecto(ruta_carpeta, ('N', 'Transporte', 'Madrid', 40.01, -3.45, 'Metropolitano', 40.01, -3.45), "nacho_mapa_trayecto.html")

	assert not os.path.exists(ruta_html)

	borrarCarpeta(ruta_carpeta)

@pytest.mark.parametrize(["latitud_origen", "longitud_origen", "latitud_destino", "longitud_destino", "ida_vuelta"],
	[
		(40.01, -3.45, 30.11, -21.45, False),
		(30.11, -21.45, 1.01, 9.86, True),
		(1.01, 9.86, 30.11, -21.45, True),
		(-2.34, 40.04, 40.01, -3.45, False)
	]
)
def test_crear_mapa_trayecto(latitud_origen, longitud_origen, latitud_destino, longitud_destino, ida_vuelta):

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

	crearCarpeta(ruta_carpeta)

	vaciarCarpeta(ruta_carpeta)

	ruta_html=os.path.join(ruta_carpeta, "nacho_mapa_trayecto.html")

	assert not os.path.exists(ruta_html)

	crearMapaTrayecto(ruta_carpeta, ('I', 'Transporte', 'Madrid', latitud_origen, longitud_origen, 'Metropolitano', latitud_destino, longitud_destino), "nacho_mapa_trayecto.html", ida_vuelta)

	assert os.path.exists(ruta_html)

	with open(ruta_html, "r") as html:

		contenido=html.read()

		assert '<div class="folium-map" id="map_' in contenido
		assert "var map_" in contenido
		assert "L.map" in contenido
		assert "var marker_" in contenido
		assert "L.marker" in contenido
		assert f"[{latitud_origen}, {longitud_origen}]" in contenido
		assert "/static/imagenes/iconos/inicio.png" in contenido
		assert "Madrid" in contenido
		assert f"[{latitud_destino}, {longitud_destino}]" in contenido
		assert "/static/imagenes/iconos/estadio_mapa.png" in contenido
		assert "Metropolitano" in contenido
		assert "var poly_line_" in contenido
		assert "L.polyline" in contenido
		assert f"[[{latitud_origen}, {longitud_origen}], [{latitud_destino}, {longitud_destino}]]" in contenido

	vaciarCarpeta(ruta_carpeta)

	borrarCarpeta(ruta_carpeta)

def test_crear_mapa_trayecto_color_ida():

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

	crearCarpeta(ruta_carpeta)

	vaciarCarpeta(ruta_carpeta)

	ruta_html=os.path.join(ruta_carpeta, "nacho_mapa_trayecto.html")

	assert not os.path.exists(ruta_html)

	crearMapaTrayecto(ruta_carpeta, ('I', 'Transporte', 'Madrid', 40.01, -3.45, 'Metropolitano', 30.11, -21.45), "nacho_mapa_trayecto.html")

	assert os.path.exists(ruta_html)

	with open(ruta_html, "r") as html:

		contenido=html.read()

		assert '<div class="folium-map" id="map_' in contenido
		assert "var map_" in contenido
		assert "L.map" in contenido
		assert "var marker_" in contenido
		assert "L.marker" in contenido
		assert "var poly_line_" in contenido
		assert "L.polyline" in contenido
		assert "solid red" in contenido
		assert "solid blue" not in contenido
		assert "solid orange" not in contenido
		assert '"color": "red"' in contenido
		assert '"color": "blue"' not in contenido
		assert '"color": "orange"' not in contenido
		assert "background-color: #ffcccc" in contenido
		assert "background-color: #95ebf7" not in contenido
		assert "background-color: #ffdd73" not in contenido

	vaciarCarpeta(ruta_carpeta)

	borrarCarpeta(ruta_carpeta)

def test_crear_mapa_trayecto_color_vuelta():

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

	crearCarpeta(ruta_carpeta)

	vaciarCarpeta(ruta_carpeta)

	ruta_html=os.path.join(ruta_carpeta, "nacho_mapa_trayecto.html")

	assert not os.path.exists(ruta_html)

	crearMapaTrayecto(ruta_carpeta, ('V', 'Transporte', 'Madrid', 40.01, -3.45, 'Metropolitano', 30.11, -21.45), "nacho_mapa_trayecto.html")

	assert os.path.exists(ruta_html)

	with open(ruta_html, "r") as html:

		contenido=html.read()

		assert '<div class="folium-map" id="map_' in contenido
		assert "var map_" in contenido
		assert "L.map" in contenido
		assert "var marker_" in contenido
		assert "L.marker" in contenido
		assert "var poly_line_" in contenido
		assert "L.polyline" in contenido
		assert "solid red" not in contenido
		assert "solid blue" in contenido
		assert "solid orange" not in contenido
		assert '"color": "red"' not in contenido
		assert '"color": "blue"' in contenido
		assert '"color": "orange"' not in contenido
		assert "background-color: #ffcccc" not in contenido
		assert "background-color: #95ebf7" in contenido
		assert "background-color: #ffdd73" not in contenido

	vaciarCarpeta(ruta_carpeta)

	borrarCarpeta(ruta_carpeta)

def test_crear_mapa_trayecto_color_ida_vuelta():

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

	crearCarpeta(ruta_carpeta)

	vaciarCarpeta(ruta_carpeta)

	ruta_html=os.path.join(ruta_carpeta, "nacho_mapa_trayecto.html")

	assert not os.path.exists(ruta_html)

	crearMapaTrayecto(ruta_carpeta, ('V', 'Transporte', 'Madrid', 40.01, -3.45, 'Metropolitano', 30.11, -21.45), "nacho_mapa_trayecto.html", True)

	assert os.path.exists(ruta_html)

	with open(ruta_html, "r") as html:

		contenido=html.read()

		assert '<div class="folium-map" id="map_' in contenido
		assert "var map_" in contenido
		assert "L.map" in contenido
		assert "var marker_" in contenido
		assert "L.marker" in contenido
		assert "var poly_line_" in contenido
		assert "L.polyline" in contenido
		assert "solid red" not in contenido
		assert "solid blue" not in contenido
		assert "solid orange" in contenido
		assert '"color": "red"' not in contenido
		assert '"color": "blue"' not in contenido
		assert '"color": "orange"' in contenido
		assert "background-color: #ffcccc" not in contenido
		assert "background-color: #95ebf7" not in contenido
		assert "background-color: #ffdd73" in contenido

	vaciarCarpeta(ruta_carpeta)

	borrarCarpeta(ruta_carpeta)

def test_crear_mapa_trayectos_sin_datos_error():

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

	crearCarpeta(ruta_carpeta)

	vaciarCarpeta(ruta_carpeta)

	ruta_html=os.path.join(ruta_carpeta, "nacho_mapa_trayecto.html")

	assert not os.path.exists(ruta_html)

	with pytest.raises(Exception):

		crearMapaTrayectos(ruta_carpeta, [], "nacho_mapa_trayecto.html")

	assert not os.path.exists(ruta_html)

	borrarCarpeta(ruta_carpeta)

@pytest.mark.parametrize(["latitud_origen", "longitud_origen", "latitud_destino", "longitud_destino"],
	[(None, None, None, None), (None, None, 30.11, -21.45), (30.11, -21.45, None, None)]
)
def test_crear_mapa_trayectos_sin_puntos_error(latitud_origen, longitud_origen, latitud_destino, longitud_destino):

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

	crearCarpeta(ruta_carpeta)

	vaciarCarpeta(ruta_carpeta)

	ruta_html=os.path.join(ruta_carpeta, "nacho_mapa_trayecto.html")

	assert not os.path.exists(ruta_html)

	with pytest.raises(Exception):

		datos_trayectos=[('I', 'Transporte', 'Madrid', latitud_origen, longitud_origen, 'Metropolitano', latitud_destino, longitud_destino),
							('V', 'Transporte', 'Madrid', latitud_origen, longitud_origen, 'Metropolitano', latitud_destino, longitud_destino)]

		crearMapaTrayectos(ruta_carpeta, datos_trayectos, "nacho_mapa_trayecto.html")

	assert not os.path.exists(ruta_html)

	borrarCarpeta(ruta_carpeta)

@pytest.mark.parametrize(["tipo_ida", "tipo_vuelta"],
	[("N", "N"), ("I", "N"), ("N", "V")]
)
def test_crear_mapa_trayectos_tipos_error(tipo_ida, tipo_vuelta):

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

	crearCarpeta(ruta_carpeta)

	vaciarCarpeta(ruta_carpeta)

	ruta_html=os.path.join(ruta_carpeta, "nacho_mapa_trayecto.html")

	assert not os.path.exists(ruta_html)

	with pytest.raises(Exception):

		datos_trayectos=[(tipo_ida, 'Transporte', 'Madrid', 40.01, -3.45, 'Metropolitano', 40.01, -3.45),
							(tipo_vuelta, 'Transporte', 'Madrid', 40.01, -3.45, 'Metropolitano', 40.01, -3.45)]

		crearMapaTrayectos(ruta_carpeta, datos_trayectos, "nacho_mapa_trayecto.html")

	assert not os.path.exists(ruta_html)

	borrarCarpeta(ruta_carpeta)

def test_crear_mapa_trayectos():

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

	crearCarpeta(ruta_carpeta)

	vaciarCarpeta(ruta_carpeta)

	ruta_html=os.path.join(ruta_carpeta, "nacho_mapa_trayecto.html")

	assert not os.path.exists(ruta_html)

	datos_trayectos=[("I", 'Transporte', 'Madrid', 40.01, -3.45, 'Metropolitano', 30.11, -21.45),
						("V", 'Transporte', 'Cuenca',-2.34, 40.04, 'Do Dragao', 1.01, 9.86)]

	crearMapaTrayectos(ruta_carpeta, datos_trayectos, "nacho_mapa_trayecto.html")

	assert os.path.exists(ruta_html)

	with open(ruta_html, "r") as html:

		contenido=html.read()

		assert '<div class="folium-map" id="map_' in contenido
		assert "var map_" in contenido
		assert "L.map" in contenido
		assert "var marker_" in contenido
		assert "L.marker" in contenido
		assert "[40.01, -3.45]" in contenido
		assert "/static/imagenes/iconos/inicio.png" in contenido
		assert "Madrid" in contenido
		assert "[30.11, -21.45]" in contenido
		assert "/static/imagenes/iconos/estadio_mapa.png" in contenido
		assert "Metropolitano" in contenido
		assert "var poly_line_" in contenido
		assert "L.polyline" in contenido
		assert "[[40.01, -3.45], [30.11, -21.45]]" in contenido
		assert "[-2.34, 40.04]" in contenido
		assert "Cuenca" in contenido
		assert "[1.01, 9.86]" in contenido
		assert "Do Dragao" in contenido
		assert "[[-2.34, 40.04], [1.01, 9.86]]" in contenido
		assert "solid red" in contenido
		assert "solid blue" in contenido
		assert "solid orange" not in contenido
		assert '"color": "red"' in contenido
		assert '"color": "blue"' in contenido
		assert '"color": "orange"' not in contenido
		assert "background-color: #ffcccc" in contenido
		assert "background-color: #95ebf7" in contenido
		assert "background-color: #ffdd73" not in contenido
		
	vaciarCarpeta(ruta_carpeta)

	borrarCarpeta(ruta_carpeta)

def test_crear_mapa_trayectos_ida_vuelta_sin_datos_error():

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

	crearCarpeta(ruta_carpeta)

	vaciarCarpeta(ruta_carpeta)

	ruta_html=os.path.join(ruta_carpeta, "nacho_mapa_trayecto.html")

	assert not os.path.exists(ruta_html)

	with pytest.raises(Exception):

		crearMapaTrayectosIdaVuelta(ruta_carpeta, [], "nacho_mapa_trayecto.html")

	assert not os.path.exists(ruta_html)

	borrarCarpeta(ruta_carpeta)

@pytest.mark.parametrize(["latitud_origen", "longitud_origen", "latitud_destino", "longitud_destino"],
	[(None, None, None, None), (None, None, 30.11, -21.45), (30.11, -21.45, None, None)]
)
def test_crear_mapa_trayectos_ida_vuelta_sin_puntos_error(latitud_origen, longitud_origen, latitud_destino, longitud_destino):

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

	crearCarpeta(ruta_carpeta)

	vaciarCarpeta(ruta_carpeta)

	ruta_html=os.path.join(ruta_carpeta, "nacho_mapa_trayecto.html")

	assert not os.path.exists(ruta_html)

	with pytest.raises(Exception):

		datos_trayectos=[('I', 'Transporte', 'Madrid', latitud_origen, longitud_origen, 'Metropolitano', latitud_destino, longitud_destino),
							('V', 'Transporte', 'Madrid', latitud_origen, longitud_origen, 'Metropolitano', latitud_destino, longitud_destino)]

		crearMapaTrayectosIdaVuelta(ruta_carpeta, datos_trayectos, "nacho_mapa_trayecto.html")

	assert not os.path.exists(ruta_html)

	borrarCarpeta(ruta_carpeta)

@pytest.mark.parametrize(["tipo_ida", "tipo_vuelta"],
	[("N", "N"), ("I", "N"), ("N", "V")]
)
def test_crear_mapa_trayectos_ida_vuelta_tipos_error(tipo_ida, tipo_vuelta):

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

	crearCarpeta(ruta_carpeta)

	vaciarCarpeta(ruta_carpeta)

	ruta_html=os.path.join(ruta_carpeta, "nacho_mapa_trayecto.html")

	assert not os.path.exists(ruta_html)

	with pytest.raises(Exception):

		datos_trayectos=[(tipo_ida, 'Transporte', 'Madrid', 41.01, -5.45, 'Metropolitano', 43.01, -3.45),
							(tipo_vuelta, 'Transporte', 'Madrid', 40.01, -3.45, 'Metropolitano', 30.01, -3.45)]

		crearMapaTrayectosIdaVuelta(ruta_carpeta, datos_trayectos, "nacho_mapa_trayecto.html")

	assert not os.path.exists(ruta_html)

	borrarCarpeta(ruta_carpeta)

def test_crear_mapa_trayectos_ida_vuelta_igual():

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

	crearCarpeta(ruta_carpeta)

	vaciarCarpeta(ruta_carpeta)

	ruta_html=os.path.join(ruta_carpeta, "nacho_mapa_trayecto.html")

	assert not os.path.exists(ruta_html)

	datos_trayectos=[("I", 'Transporte', 'Madrid', 40.01, -3.45, 'Metropolitano', 30.11, -21.45),
						("V", 'Transporte', 'Madrid', 40.01, -3.45, 'Metropolitano', 30.11, -21.45)]

	crearMapaTrayectosIdaVuelta(ruta_carpeta, datos_trayectos, "nacho_mapa_trayecto.html")

	assert os.path.exists(ruta_html)

	with open(ruta_html, "r") as html:

		contenido=html.read()

		assert '<div class="folium-map" id="map_' in contenido
		assert "var map_" in contenido
		assert "L.map" in contenido
		assert "var marker_" in contenido
		assert "L.marker" in contenido
		assert "[40.01, -3.45]" in contenido
		assert "/static/imagenes/iconos/inicio.png" in contenido
		assert "Madrid" in contenido
		assert "[30.11, -21.45]" in contenido
		assert "/static/imagenes/iconos/estadio_mapa.png" in contenido
		assert "Metropolitano" in contenido
		assert "var poly_line_" in contenido
		assert "L.polyline" in contenido
		assert "[[40.01, -3.45], [30.11, -21.45]]" in contenido
		assert "solid red" not in contenido
		assert "solid blue" not in contenido
		assert "solid orange" in contenido
		assert '"color": "red"' not in contenido
		assert '"color": "blue"' not in contenido
		assert '"color": "orange"' in contenido
		assert "background-color: #ffcccc" not in contenido
		assert "background-color: #95ebf7" not in contenido
		assert "background-color: #ffdd73" in contenido
		
	vaciarCarpeta(ruta_carpeta)

	borrarCarpeta(ruta_carpeta)

def test_crear_mapa_trayectos_ida_vuelta_diferente():

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

	crearCarpeta(ruta_carpeta)

	vaciarCarpeta(ruta_carpeta)

	ruta_html=os.path.join(ruta_carpeta, "nacho_mapa_trayecto.html")

	assert not os.path.exists(ruta_html)

	datos_trayectos=[("I", 'Transporte', 'Madrid', 40.01, -3.45, 'Metropolitano', 30.11, -21.45),
						("V", 'Transporte', 'Cuenca', 45.01, -6.45, 'Metropolitano', 30.11, -21.45)]

	crearMapaTrayectosIdaVuelta(ruta_carpeta, datos_trayectos, "nacho_mapa_trayecto.html")

	assert os.path.exists(ruta_html)

	with open(ruta_html, "r") as html:

		contenido=html.read()

		assert '<div class="folium-map" id="map_' in contenido
		assert "var map_" in contenido
		assert "L.map" in contenido
		assert "var marker_" in contenido
		assert "L.marker" in contenido
		assert "[40.01, -3.45]" in contenido
		assert "/static/imagenes/iconos/inicio.png" in contenido
		assert "Madrid" in contenido
		assert "[30.11, -21.45]" in contenido
		assert "/static/imagenes/iconos/estadio_mapa.png" in contenido
		assert "Metropolitano" in contenido
		assert "var poly_line_" in contenido
		assert "L.polyline" in contenido
		assert "[[40.01, -3.45], [30.11, -21.45]]" in contenido
		assert "[45.01, -6.45]" in contenido
		assert "Cuenca" in contenido
		assert "[30.11, -21.45]" in contenido
		assert "[[45.01, -6.45], [30.11, -21.45]]" in contenido
		assert "solid red" in contenido
		assert "solid blue" in contenido
		assert "solid orange" not in contenido
		assert '"color": "red"' in contenido
		assert '"color": "blue"' in contenido
		assert '"color": "orange"' not in contenido
		assert "background-color: #ffcccc" in contenido
		assert "background-color: #95ebf7" in contenido
		assert "background-color: #ffdd73" not in contenido
		
	vaciarCarpeta(ruta_carpeta)

	borrarCarpeta(ruta_carpeta)