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

def test_existe_estadio_equipo_no_existe(conexion):

	assert not conexion.existe_estadio_equipo("atleti-madrid")

def test_existe_estadio_equipo_existe(conexion):

	conexion.insertarEquipo("atleti-madrid")

	estadio=["vicente-calderon", 1, "Calderon", "Paseo de los Melancolicos",
				40, -3, "Madrid", 55, 1957, 100, 50, "Telefono", "Cesped"]

	conexion.insertarEstadio(estadio)

	conexion.insertarEquipoEstadio(("atleti-madrid", "vicente-calderon"))

	assert conexion.existe_estadio_equipo("atleti-madrid")

def test_existe_estadio_equipo_existen(conexion):

	conexion.insertarEquipo("atleti-madrid")

	for numero in range(1,10):

		estadio=[f"vicente-calderon-{numero}", 1, "Calderon", "Paseo de los Melancolicos",
					40, -3, "Madrid", 55, 1957, 100, 50, "Telefono", "Cesped"]

		conexion.insertarEstadio(estadio)

		conexion.insertarEquipoEstadio(("atleti-madrid", f"vicente-calderon-{numero}"))

	assert conexion.existe_estadio_equipo("atleti-madrid")

def test_obtener_estadio_equipo_no_existe(conexion):

	assert not conexion.obtenerEstadioEquipo("atleti-madrid")

def test_obtener_estadio_equipo_existe(conexion):

	conexion.insertarEquipo("atleti-madrid")

	estadio=["vicente-calderon", 1, "Calderon", "Paseo de los Melancolicos",
				40, -3, "Madrid", 55, 1957, 100, 50, "Telefono", "Cesped"]

	conexion.insertarEstadio(estadio)

	conexion.insertarEquipoEstadio(("atleti-madrid", "vicente-calderon"))

	assert conexion.obtenerEstadioEquipo("atleti-madrid")=="vicente-calderon"

def test_obtener_estadio_equipo_existen(conexion):

	conexion.insertarEquipo("atleti-madrid")

	for numero in range(1,10):

		estadio=[f"vicente-calderon-{numero}", 1, "Calderon", "Paseo de los Melancolicos",
					40, -3, "Madrid", 55, 1957, 100, 50, "Telefono", "Cesped"]

		conexion.insertarEstadio(estadio)

		conexion.insertarEquipoEstadio(("atleti-madrid", f"vicente-calderon-{numero}"))

	assert conexion.obtenerEstadioEquipo("atleti-madrid").startswith("vicente-calderon")