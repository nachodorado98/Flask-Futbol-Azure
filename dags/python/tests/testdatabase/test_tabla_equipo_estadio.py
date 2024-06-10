def test_tabla_equipo_estadio_vacia(conexion):

	conexion.c.execute("SELECT * FROM equipo_estadio")

	assert not conexion.c.fetchall()

def test_insertar_equipo_estadio(conexion):

	conexion.insertarEquipo("atleti-madrid")

	estadio=["vicente-calderon", 1, "Calderon", "Paseo de los Melancolicos",
				40, -3, "Madrid", 55, 1957, 100, 50, "Telefono", "Cesped"]

	conexion.insertarEstadio(estadio)

	conexion.insertarEquipoEstadio(("atleti-madrid", "vicente-calderon"))

	conexion.c.execute("SELECT * FROM equipo_estadio")

	assert len(conexion.c.fetchall())==1

def test_existe_equipo_estadio_no_existe(conexion):

	assert not conexion.existe_equipo_estadio("atleti-madrid", "vicente-calderon")

def test_existe_equipo_estadio_existe(conexion):

	conexion.insertarEquipo("atleti-madrid")

	estadio=["vicente-calderon", 1, "Calderon", "Paseo de los Melancolicos",
				40, -3, "Madrid", 55, 1957, 100, 50, "Telefono", "Cesped"]

	conexion.insertarEstadio(estadio)

	conexion.insertarEquipoEstadio(("atleti-madrid", "vicente-calderon"))

	assert conexion.existe_equipo_estadio("atleti-madrid", "vicente-calderon")