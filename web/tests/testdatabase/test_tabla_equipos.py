import pytest

def test_tabla_equipos_vacia(conexion):

	conexion.c.execute("SELECT * FROM equipos")

	assert not conexion.c.fetchall()

def test_existe_equipo_no_existe(conexion):

	assert not conexion.existe_equipo("atletico-madrid")

def test_existe_equipo(conexion_entorno):

	assert conexion_entorno.existe_equipo("atletico-madrid")

def test_obtener_nombre_equipo_no_existe(conexion):

	assert not conexion.obtenerNombreEquipo("atletico-madrid")

def test_obtener_nombre_equipo_sin_nombre(conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id)  VALUES('atletico-madrid')""")

	conexion.confirmar()

	assert not conexion.obtenerNombreEquipo("atletico-madrid")

@pytest.mark.parametrize(["nombre_completo"],
	[("atleti",),("atm",),("Club Atletico de Madrid",)]
)
def test_obtener_nombre_equipo(conexion, nombre_completo):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Nombre_Completo)
						VALUES('atletico-madrid', %s)""", (nombre_completo,))

	conexion.confirmar()

	assert conexion.obtenerNombreEquipo("atletico-madrid")==nombre_completo

def test_obtener_equipo_no_existe(conexion):

	assert not conexion.obtenerDatosEquipo("atletico-madrid")

def test_obtener_equipo(conexion_entorno):

	assert conexion_entorno.obtenerDatosEquipo("atletico-madrid")

def test_obtener_equipos_competicion_no_existe(conexion):

	assert not conexion.obtenerEquiposCompeticion("primera")

def test_obtener_equipos_competicion(conexion_entorno):

	assert conexion_entorno.obtenerEquiposCompeticion("primera")

@pytest.mark.parametrize(["numero_competicion", "numero_no_competicion"],
	[(10, 5), (0, 2), (4, 8), (7, 3)]
)
def test_obtener_equipos_competicion_multiples_equipos(conexion_entorno, numero_competicion, numero_no_competicion):

	conexion_entorno.c.execute("""DELETE FROM equipos""")

	conexion_entorno.confirmar()

	for numero in range(numero_competicion):

		conexion_entorno.c.execute(f"""INSERT INTO equipos (Equipo_Id, Codigo_Competicion)
										VALUES('equipo-si-{numero}', 'primera')""")

		conexion_entorno.confirmar()

	for numero in range(numero_no_competicion):

		conexion_entorno.c.execute(f"""INSERT INTO equipos (Equipo_Id, Codigo_Competicion)
										VALUES('equipo-no-{numero}', 'segunda')""")

		conexion_entorno.confirmar()

	equipos_competicion=conexion_entorno.obtenerEquiposCompeticion("primera")

	assert len(equipos_competicion)==numero_competicion

	conexion_entorno.c.execute("SELECT * FROM equipos")

	equipo_totales=conexion_entorno.c.fetchall()

	assert len(equipo_totales)==numero_competicion+numero_no_competicion

def test_obtener_equipos_no_existe(conexion):

	assert not conexion.obtenerDatosEquipos()

def test_obtener_equipos(conexion_entorno):

	assert conexion_entorno.obtenerDatosEquipos()

def test_obtener_equipos_top_no_existe(conexion):

	assert not conexion.obtenerDatosEquiposTop(5)

def test_obtener_equipos_top(conexion):

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Puntuacion)
									VALUES('equipo1', 10),('equipo2', 100),('equipo3', 22),('equipo4', 101),('equipo5', 5),
											('equipo6', 15),('equipo7', 13),('equipo8', 1000),('equipo9', 11),('equipo10', 1)""")

	conexion.confirmar()

	equipos_top=conexion.obtenerDatosEquiposTop(5)

	assert equipos_top[0][0]=="equipo8"
	assert equipos_top[-1][0]=="equipo6"