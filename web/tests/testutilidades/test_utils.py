import pytest

from src.utilidades.utils import usuario_correcto, nombre_correcto, apellido_correcto, contrasena_correcta
from src.utilidades.utils import fecha_correcta, equipo_correcto, correo_correcto, datos_correctos
from src.utilidades.utils import generarHash, comprobarHash, enviarCorreo, correo_enviado, anadirPuntos
from src.utilidades.utils import limpiarResultadosPartidos, obtenerNombrePaisSeleccionado, obtenerPaisesNoSeleccionados

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