def test_tabla_partido_estadio_vacia(conexion):

	conexion.c.execute("SELECT * FROM partido_estadio")

	assert not conexion.c.fetchall()

def test_insertar_partido_estadio(conexion):

	conexion.insertarEquipo("atleti-madrid")

	partido=["1", "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	estadio=["vicente-calderon", 1, "Calderon", "Paseo de los Melancolicos",
				40, -3, "Madrid", 55, 1957, 100, 50, "Telefono", "Cesped"]

	conexion.insertarEstadio(estadio)

	conexion.insertarPartidoEstadio(("1", "vicente-calderon"))

	conexion.c.execute("SELECT * FROM partido_estadio")

	assert len(conexion.c.fetchall())==1

def test_existe_partido_estadio_no_existe(conexion):

	assert not conexion.existe_partido_estadio("1", "vicente-calderon")

def test_existe_partido_estadio_existe(conexion):

	conexion.insertarEquipo("atleti-madrid")

	partido=["1", "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	estadio=["vicente-calderon", 1, "Calderon", "Paseo de los Melancolicos",
				40, -3, "Madrid", 55, 1957, 100, 50, "Telefono", "Cesped"]

	conexion.insertarEstadio(estadio)

	conexion.insertarPartidoEstadio(("1", "vicente-calderon"))

	assert conexion.existe_partido_estadio("1", "vicente-calderon")