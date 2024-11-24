import pytest
import os
import geopandas as gpd

from src.utilidades.utils import usuario_correcto, nombre_correcto, apellido_correcto, contrasena_correcta
from src.utilidades.utils import fecha_correcta, equipo_correcto, correo_correcto, datos_correctos
from src.utilidades.utils import generarHash, comprobarHash, enviarCorreo, correo_enviado, anadirPuntos
from src.utilidades.utils import limpiarResultadosPartidos, obtenerNombrePaisSeleccionado, obtenerPaisesNoSeleccionados
from src.utilidades.utils import crearCarpeta, borrarCarpeta, vaciarCarpeta, vaciarCarpetaMapasUsuario
from src.utilidades.utils import obtenerCentroide, crearMapaMisEstadios, crearMapaMisEstadiosDetalle
from src.utilidades.utils import leerGeoJSON, obtenerGeometriaPais, obtenerGeometriasPaises, crearMapaMisEstadiosDetallePaises

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

def HTML()->str:

	return 	"""<html>
					<body>
						<h1>¡Hola!</h1>
						<p>Este es un <b>correo electrónico</b> enviado desde un script</p>
					</body>
				</html>
			"""

def test_enviar_correo_error():

	with pytest.raises(Exception):

		enviarCorreo("ignaciodoradoruiz@gmail.com", "asunto", HTML(), "ignaciodoradoruiz@gmail.com", "1234")

def test_enviar_correo():

	assert not enviarCorreo("ignaciodoradoruiz@gmail.com", "asunto", HTML())

def test_correo_enviado_no_enviado():

	assert not correo_enviado("ignaciodoradoruiz@gmail.com", "nombre", "ignaciodoradoruiz@gmail.com", "1234")

def test_correo_enviado():

	assert correo_enviado("ignaciodoradoruiz@gmail.com", "nombre")

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