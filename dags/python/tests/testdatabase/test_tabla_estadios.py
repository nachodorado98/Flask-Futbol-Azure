import pytest

def test_tabla_estadios_vacia(conexion):

	conexion.c.execute("SELECT * FROM estadios")

	assert not conexion.c.fetchall()

def test_insertar_estadio(conexion):

	estadio=["vicente-calderon", 1, "Calderon", "Paseo de los Melancolicos",
				40, -3, "Madrid", 55, 1957, 100, 50, "Telefono", "Cesped"]

	conexion.insertarEstadio(estadio)

	conexion.c.execute("SELECT * FROM estadios")

	assert len(conexion.c.fetchall())==1

def test_existe_estadio_no_existe(conexion):

	assert not conexion.existe_estadio("vicente-calderon")

def test_existe_estadio_existe(conexion):

	estadio=["vicente-calderon", 1, "Calderon", "Paseo de los Melancolicos",
				40, -3, "Madrid", 55, 1957, 100, 50, "Telefono", "Cesped"]

	conexion.insertarEstadio(estadio)

	assert conexion.existe_estadio("vicente-calderon")

def test_obtener_codigo_estadios_no_hay(conexion):

	assert not conexion.obtenerCodigoEstadios()

@pytest.mark.parametrize(["codigos", "numero_estadios"],
	[
		([1, 2, 3], 3),
		([1, 2, None], 2),
		([1, 2, 3, None], 3),
		([None, None, 3], 1)
	]
)
def test_obtener_codigo_estadios(conexion, codigos, numero_estadios):

	for posicion, codigo in enumerate(codigos):

		estadio=[f"vicente-calderon-{posicion}", codigo, "Calderon", "Paseo de los Melancolicos",
					40, -3, "Madrid", 55, 1957, 100, 50, "Telefono", "Cesped"]

		conexion.insertarEstadio(estadio)

	codigo_estadios=conexion.obtenerCodigoEstadios()

	assert len(codigo_estadios)==numero_estadios

def test_actualizar_datos_estadios_no_existe(conexion):

	assert not conexion.existe_estadio("estadio")

	datos=["España", "es"]

	conexion.actualizarDatosEstadio(datos, "estadio")

	assert not conexion.existe_estadio("estadio")

@pytest.mark.parametrize(["datos_nuevos"],
	[(["Argentina", "ar"],), ([None, "ar"],), (["Argentina", None],), (["España", "es"],)]
)
def test_actualizar_datos_estadio(conexion, datos_nuevos):

	estadio=["vicente-calderon", 1, "Calderon", "Paseo de los Melancolicos",
				40, -3, "Madrid", 55, 1957, 100, 50, "Telefono", "Cesped"]

	conexion.insertarEstadio(estadio)

	assert conexion.existe_estadio("vicente-calderon")

	conexion.actualizarDatosEstadio(datos_nuevos, "vicente-calderon")

	conexion.c.execute("SELECT Pais, Codigo_Pais FROM estadios WHERE Estadio_Id='vicente-calderon'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["pais"]==datos_nuevos[0]
	assert datos_actualizados["codigo_pais"]==datos_nuevos[1]

def test_obtener_estadios_no_hay(conexion):

	assert not conexion.obtenerEstadios()

def test_obtener_estadios(conexion):

	for numero in range(1,11):

		estadio=[f"vicente-calderon-{numero}", numero, "Calderon", "Paseo de los Melancolicos",
				40, -3, "Madrid", 55, 1957, 100, 50, "Telefono", "Cesped"]

		conexion.insertarEstadio(estadio)

	estadios=conexion.obtenerEstadios()

	assert len(estadios)==10

def test_obtener_codigo_paises_estadios_no_hay(conexion):

	assert not conexion.obtenerCodigoPaisesEstadios()

def test_obtener_codigo_paises_estadios_son_nulos(conexion):

	for numero in range(1,11):

		estadio=[f"vicente-calderon-{numero}", 1, "Calderon", "Paseo de los Melancolicos",
				40, -3, "Madrid", 55, 1957, 100, 50, "Telefono", "Cesped"]

		conexion.insertarEstadio(estadio)

	assert not conexion.obtenerCodigoPaisesEstadios()

@pytest.mark.parametrize(["datos", "numero_paises"],
	[
		([["Argentina", "ar"], [None, "ar"], ["Argentina", None], ["España", "es"]], 2),
		([["Argentina", "ar"], [None, "ar"], ["Argentina", None], ["Argentina", "ar"]], 1),
		([["Argentina", None], [None, "ar"], ["Argentina", None], ["España", "es"]], 2),
		([["Argentina", "ar"], [None, "ar"], ["Argentina", None], ["España", "es"], ["Francia", "fr"]], 3),
	]
)
def test_obtener_codigo_paises_estadios(conexion, datos, numero_paises):

	for numero, dato in enumerate(datos):

		estadio=[f"vicente-calderon-{numero}", 1, "Calderon", "Paseo de los Melancolicos",
				40, -3, "Madrid", 55, 1957, 100, 50, "Telefono", "Cesped"]

		conexion.insertarEstadio(estadio)

		conexion.actualizarDatosEstadio(dato, f"vicente-calderon-{numero}")

	paises=conexion.obtenerCodigoPaisesEstadios()

	assert len(paises)==numero_paises