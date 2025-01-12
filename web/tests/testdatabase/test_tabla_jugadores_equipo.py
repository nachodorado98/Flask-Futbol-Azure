import pytest

def test_tabla_jugadores_equipo_vacia(conexion):

	conexion.c.execute("SELECT * FROM jugadores_equipo")

	assert not conexion.c.fetchall()

def test_obtener_equipos_jugador_no_existe_jugador(conexion):

	assert not conexion.obtenerEquiposJugador("julian-alvarez")

def test_obtener_equipos_jugador_no_tiene(conexion_entorno):

	conexion_entorno.c.execute("""INSERT INTO jugadores
								VALUES('nacho', 'Nacho', 'atletico-madrid', 'es', '1324', 100, 100.0, 9, 'DC')""")

	conexion_entorno.confirmar()

	assert not conexion_entorno.obtenerEquiposJugador("nacho")

def test_obtener_equipos_jugador(conexion_entorno):

	equipos=conexion_entorno.obtenerEquiposJugador("julian-alvarez")

	assert len(equipos)==1

@pytest.mark.parametrize(["numero_equipos"],
	[(2,),(10,),(13,),(7,)]
)
def test_obtener_equipos_jugador_varios(conexion_entorno, numero_equipos):

	for numero in range(numero_equipos):

		conexion_entorno.c.execute(f"""INSERT INTO equipos (Equipo_Id)
							VALUES('equipo{numero}')""")

		conexion_entorno.c.execute(f"""INSERT INTO jugadores_equipo
							VALUES('julian-alvarez', 'equipo{numero}', 1, 1, 1)""")

		conexion_entorno.confirmar()

	equipos=conexion_entorno.obtenerEquiposJugador("julian-alvarez")

	assert len(equipos)==numero_equipos+1