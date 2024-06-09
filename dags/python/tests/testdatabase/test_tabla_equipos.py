import pytest

def test_tabla_equipos_vacia(conexion):

	conexion.c.execute("SELECT * FROM equipos")

	assert not conexion.c.fetchall()

def test_insertar_equipo(conexion):

	conexion.insertarEquipo("atleti-madrid")

	conexion.c.execute("SELECT * FROM equipos")

	assert len(conexion.c.fetchall())==1

def test_existe_equipo_no_existe(conexion):

	assert not conexion.existe_equipo("atleti-madrid")

def test_existe_equipo_existe(conexion):

	conexion.insertarEquipo("atleti-madrid")

	assert conexion.existe_equipo("atleti-madrid")

def test_actualizar_datos_equipo_no_existe(conexion):

	assert not conexion.existe_equipo("atleti-madrid")

	datos=["Club Atletico de Madrid", "Atleti", "ATM", "España", "es", "Madrid", "Primera", "primera",
			22, "Calderon", 1903, "Nacho", "nacho-dorado", 16]

	conexion.actualizarDatosEquipo(datos, "atleti-madrid")

	assert not conexion.existe_equipo("atleti-madrid")

@pytest.mark.parametrize(["datos_nuevos"],
	[
		(["Club Atletico de Madrid", "Atleti", "ATM", "España", "es", "Madrid", "Primera", "primera",
			22, "Calderon", 1903, "Nacho", "nacho-dorado", 16],),
		(["Club Atletico", "AtletiMadrid", "ATM", "Españita", "aa", "Madrid", "Primera","primera",
			22, "Calderon", 1903, "Golden", "nacho-dorado", 16],),
		(["Club Atletico de Madrid", "Atleti", "ATM", "España", "es", "Piramides", "Primera Division",
			"primera-division", 2019, "Eterno Calderon", 2019, "Golden", "nacho-dorado", None],)
	]
)
def test_actualizar_datos_equipo(conexion, datos_nuevos):

	conexion.insertarEquipo("atleti-madrid")

	assert conexion.existe_equipo("atleti-madrid")

	conexion.actualizarDatosEquipo(datos_nuevos, "atleti-madrid")

	conexion.c.execute("SELECT * FROM equipos WHERE Equipo_Id='atleti-madrid'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["nombre_completo"]==datos_nuevos[0]
	assert datos_actualizados["nombre"]==datos_nuevos[1]
	assert datos_actualizados["siglas"]==datos_nuevos[2]
	assert datos_actualizados["pais"]==datos_nuevos[3]
	assert datos_actualizados["codigo_pais"]==datos_nuevos[4]
	assert datos_actualizados["ciudad"]==datos_nuevos[5]
	assert datos_actualizados["competicion"]==datos_nuevos[6]
	assert datos_actualizados["codigo_competicion"]==datos_nuevos[7]
	assert datos_actualizados["temporadas"]==datos_nuevos[8]
	assert datos_actualizados["estadio"]==datos_nuevos[9]
	assert datos_actualizados["fundacion"]==datos_nuevos[10]
	assert datos_actualizados["presidente"]==datos_nuevos[11]
	assert datos_actualizados["presidente_url"]==datos_nuevos[12]
	assert datos_actualizados["codigo_presidente"]==datos_nuevos[13]

def test_obtener_equipos_no_hay(conexion):

	assert not conexion.obtenerEquipos()

def test_obtener_equipos(conexion):

	for numero in range(1,11):

		conexion.insertarEquipo(f"atleti-madrid-{numero}")

	equipos=conexion.obtenerEquipos()

	assert len(equipos)==10

def test_actualizar_escudo_equipo_no_existe(conexion):

	assert not conexion.existe_equipo("atleti-madrid")

	datos=[1234, 99]

	conexion.actualizarEscudoEquipo(datos, "atleti-madrid")

	assert not conexion.existe_equipo("atleti-madrid")

@pytest.mark.parametrize(["datos_nuevos"],
	[
		([1234, 99],),
		([0, 999],),
		([124356, 0],),
		([1, 1],)
	]
)
def test_actualizar_escudo_equipo(conexion, datos_nuevos):

	conexion.insertarEquipo("atleti-madrid")

	assert conexion.existe_equipo("atleti-madrid")

	conexion.actualizarEscudoEquipo(datos_nuevos, "atleti-madrid")

	conexion.c.execute("SELECT * FROM equipos WHERE Equipo_Id='atleti-madrid'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["escudo"]==datos_nuevos[0]
	assert datos_actualizados["puntuacion"]==datos_nuevos[1]