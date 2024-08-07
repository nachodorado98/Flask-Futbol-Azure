import pytest

def test_tabla_competiciones_vacia(conexion):

	conexion.c.execute("SELECT * FROM competiciones")

	assert not conexion.c.fetchall()

def test_insertar_competicion(conexion):

	conexion.insertarCompeticion("competicion")

	conexion.c.execute("SELECT * FROM competiciones")

	assert len(conexion.c.fetchall())==1

def test_existe_competicion_no_existe(conexion):

	assert not conexion.existe_competicion("competicion")

def test_existe_competicion_existe(conexion):

	conexion.insertarCompeticion("competicion")

	assert conexion.existe_competicion("competicion")

def test_actualizar_datos_competicion_no_existe(conexion):

	assert not conexion.existe_competicion("competicion")

	datos=["Primera", "primera", "es"]

	conexion.actualizarDatosCompeticion(datos, "competicion")

	assert not conexion.existe_competicion("competicion")

@pytest.mark.parametrize(["datos_nuevos"],
	[
		(["Primera", "primera", "es"],),
		(["Segunda", "seg", "es"],),
		(["Primera", None, "es"],),
		(["Primera", "primera", None],),
		([None, "primera", "es"],)
	]
)
def test_actualizar_datos_competicion(conexion, datos_nuevos):

	conexion.insertarCompeticion("primera")

	assert conexion.existe_competicion("primera")

	conexion.actualizarDatosCompeticion(datos_nuevos, "primera")

	conexion.c.execute("SELECT * FROM competiciones WHERE Competicion_Id='primera'")

	datos_actualizados=conexion.c.fetchone()

	assert datos_actualizados["nombre"]==datos_nuevos[0]
	assert datos_actualizados["codigo_logo"]==datos_nuevos[1]
	assert datos_actualizados["codigo_pais"]==datos_nuevos[2]

def test_obtener_competiciones_no_hay(conexion):

	assert not conexion.obtenerCompeticiones()

def test_obtener_competiciones(conexion):

	for numero in range(1,11):

		conexion.insertarCompeticion(f"primera-{numero}")

	competiciones=conexion.obtenerCompeticiones()

	assert len(competiciones)==10

def test_obtener_competiciones_equipos_no_hay(conexion):

	assert not conexion.obtenerCompeticionesEquipos()

def test_obtener_competiciones_equipos_unicas(conexion):

	for numero in range(1,11):

		conexion.c.execute(f"""INSERT INTO equipos (Equipo_Id, Codigo_Competicion) VALUES('atletico-madrid-{numero}', 'primera-{numero}')""")

	conexion.confirmar()

	competiciones=conexion.obtenerCompeticionesEquipos()

	assert len(competiciones)==10

def test_obtener_competiciones_equipos_duplicados(conexion):

	for numero in range(1,11):

		conexion.c.execute(f"""INSERT INTO equipos (Equipo_Id, Codigo_Competicion) VALUES('atletico-madrid-{numero}', 'primera')""")

	conexion.confirmar()

	competiciones=conexion.obtenerCompeticionesEquipos()

	assert len(competiciones)==1