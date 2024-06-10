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