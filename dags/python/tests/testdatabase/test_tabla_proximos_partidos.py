import pytest

def test_tabla_proximos_partidos_vacia(conexion):

	conexion.c.execute("SELECT * FROM proximos_partidos")

	assert not conexion.c.fetchall()

def test_insertar_proximo_partido(conexion):

	conexion.insertarEquipo("atleti-madrid")

	proximo_partido=["1", "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga"]

	conexion.insertarProximoPartido(proximo_partido)

	conexion.c.execute("SELECT * FROM proximos_partidos")

	assert len(conexion.c.fetchall())==1

def test_existe_proximo_partido_no_existe(conexion):

	assert not conexion.existe_proximo_partido("1")

def test_existe_proximo_partido_existe(conexion):

	conexion.insertarEquipo("atleti-madrid")

	proximo_partido=["1", "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga"]

	conexion.insertarProximoPartido(proximo_partido)

	assert conexion.existe_proximo_partido("1")

def test_vaciar_tabla_proximos_partidos_no_hay(conexion):

	conexion.c.execute("SELECT * FROM proximos_partidos")

	assert not conexion.c.fetchall()

	conexion.vaciar_proximos_partidos("atleti-madrid")

	conexion.c.execute("SELECT * FROM proximos_partidos")

	assert not conexion.c.fetchall()

def test_vaciar_tabla_proximos_partidos(conexion):

	conexion.insertarEquipo("atleti-madrid")

	proximo_partido=["1", "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga"]

	conexion.insertarProximoPartido(proximo_partido)

	conexion.c.execute("SELECT * FROM proximos_partidos")

	assert conexion.c.fetchall()

	conexion.vaciar_proximos_partidos("atleti-madrid")

	conexion.c.execute("SELECT * FROM proximos_partidos")

	assert not conexion.c.fetchall()

def test_vaciar_tabla_proximos_partidos_otros_equipos(conexion):

	conexion.insertarEquipo("atleti-madrid")

	conexion.insertarEquipo("inter")

	proximo_partido=["1", "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga"]

	conexion.insertarProximoPartido(proximo_partido)

	proximo_partido=["2", "inter", "inter", "2019-06-22", "20:00", "Liga"]

	conexion.insertarProximoPartido(proximo_partido)

	conexion.c.execute("SELECT * FROM proximos_partidos")

	assert conexion.c.fetchall()

	conexion.vaciar_proximos_partidos("atleti-madrid")

	conexion.c.execute("SELECT * FROM proximos_partidos")

	assert conexion.c.fetchall()

def test_obtener_equipos_proximos_partidos_equipo_no_hay(conexion):

	assert not conexion.obtenerEquiposProximosPartidosEquipo("atleti-madrid")

def test_obtener_equipos_proximos_partidos_equipo_no_tiene(conexion):

	conexion.insertarEquipo("atleti-madrid")

	proximo_partido=["1", "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga"]

	conexion.insertarProximoPartido(proximo_partido)

	assert not conexion.obtenerEquiposProximosPartidosEquipo("inter")

def test_obtener_equipos_proximos_partidos_equipo(conexion):

	conexion.insertarEquipo("atleti-madrid")

	conexion.insertarEquipo("inter")

	proximo_partido=["1", "atleti-madrid", "inter", "2019-06-22", "20:00", "Liga"]

	conexion.insertarProximoPartido(proximo_partido)

	equipos=conexion.obtenerEquiposProximosPartidosEquipo("atleti-madrid")

	assert len(equipos)==1
	assert equipos[0][0]=="inter"

@pytest.mark.parametrize(["numero_equipos"],
	[(3,),(5,),(7,),(3,)]
)
def test_obtener_equipos_proximos_partidos_equipo_repetido(conexion, numero_equipos):

	conexion.insertarEquipo("atleti-madrid")

	conexion.insertarEquipo("inter")

	for numero in range(numero_equipos):

		proximo_partido=[numero, "atleti-madrid", "inter", "2019-06-22", "20:00", "Liga"]

		conexion.insertarProximoPartido(proximo_partido)

	equipos=conexion.obtenerEquiposProximosPartidosEquipo("atleti-madrid")

	assert len(equipos)==1
	assert equipos[0][0]=="inter"

@pytest.mark.parametrize(["numero_equipos"],
	[(3,),(5,),(17,),(3,)]
)
def test_obtener_equipos_proximos_partidos_equipo_varios(conexion, numero_equipos):

	conexion.insertarEquipo("atleti-madrid")

	for numero in range(numero_equipos):

		conexion.insertarEquipo(f"equipo_{numero}")

		proximo_partido=[numero, "atleti-madrid", f"equipo_{numero}", "2019-06-22", "20:00", "Liga"]

		conexion.insertarProximoPartido(proximo_partido)

	equipos=conexion.obtenerEquiposProximosPartidosEquipo("atleti-madrid")

	assert len(equipos)==numero_equipos

	equipos_rival=[f"equipo_{numero}" for numero in range(numero_equipos)]

	for equipo in equipos:

		assert equipo[0] in equipos_rival