import pytest

def test_tabla_partidos_vacia(conexion):

	conexion.c.execute("SELECT * FROM partidos")

	assert not conexion.c.fetchall()

def test_insertar_partido(conexion):

	conexion.insertarEquipo("atleti-madrid")

	partido=["1", "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	conexion.c.execute("SELECT * FROM partidos")

	assert len(conexion.c.fetchall())==1

def test_existe_partido_no_existe(conexion):

	assert not conexion.existe_partido("1")

def test_existe_partido_existe(conexion):

	conexion.insertarEquipo("atleti-madrid")

	partido=["1", "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	assert conexion.existe_partido("1")

def test_fecha_mas_reciente_tabla_vacia(conexion):

	assert conexion.fecha_mas_reciente("atleti-madrid") is None

def test_fecha_mas_reciente(conexion):

	conexion.insertarEquipo("atleti-madrid")

	partidos=[["1", "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga", "1-0", "Victoria"],
				["2", "atleti-madrid", "atleti-madrid", "2018-06-22", "20:00", "Liga", "1-0", "Victoria"],
				["3", "atleti-madrid", "atleti-madrid", "2010-05-22", "20:00", "Liga", "1-0", "Victoria"],
				["4", "atleti-madrid", "atleti-madrid", "2019-07-11", "20:00", "Liga", "1-0", "Victoria"],
				["5", "atleti-madrid", "atleti-madrid", "2024-06-22", "20:00", "Liga", "1-0", "Victoria"],
				["6", "atleti-madrid", "atleti-madrid", "2024-06-21", "20:00", "Liga", "1-0", "Victoria"]]

	for partido in partidos:

		conexion.insertarPartido(partido)

	assert conexion.fecha_mas_reciente("atleti-madrid").strftime("%Y-%m-%d")=="2024-06-22"

def test_fecha_mas_reciente_otros_equipos(conexion):

	conexion.insertarEquipo("atleti-madrid")

	conexion.insertarEquipo("inter")

	partidos=[["1", "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga", "1-0", "Victoria"],
				["2", "atleti-madrid", "atleti-madrid", "2018-06-22", "20:00", "Liga", "1-0", "Victoria"],
				["3", "inter", "atleti-madrid", "2024-06-21", "20:00", "Liga", "1-0", "Victoria"],
				["4", "atleti-madrid", "atleti-madrid", "2010-05-22", "20:00", "Liga", "1-0", "Victoria"],
				["5", "atleti-madrid", "atleti-madrid", "2019-07-11", "20:00", "Liga", "1-0", "Victoria"],
				["6", "inter", "inter", "2024-06-21", "20:00", "Liga", "1-0", "Victoria"],
				["7", "atleti-madrid", "atleti-madrid", "2024-06-22", "20:00", "Liga", "1-0", "Victoria"],
				["8", "atleti-madrid", "atleti-madrid", "2024-06-21", "20:00", "Liga", "1-0", "Victoria"],
				["9", "inter", "inter", "2025-06-21", "20:00", "Liga", "1-0", "Victoria"]]

	for partido in partidos:

		conexion.insertarPartido(partido)

	assert conexion.fecha_mas_reciente("atleti-madrid").strftime("%Y-%m-%d")=="2024-06-22"

def test_ultimo_ano_tabla_vacia(conexion):

	assert conexion.ultimo_ano("atleti-madrid") is None

def test_ultimo_ano(conexion):

	conexion.insertarEquipo("atleti-madrid")

	partidos=[["1", "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga", "1-0", "Victoria"],
				["2", "atleti-madrid", "atleti-madrid", "2018-06-22", "20:00", "Liga", "1-0", "Victoria"],
				["3", "atleti-madrid", "atleti-madrid", "2010-05-22", "20:00", "Liga", "1-0", "Victoria"],
				["4", "atleti-madrid", "atleti-madrid", "2019-07-11", "20:00", "Liga", "1-0", "Victoria"],
				["5", "atleti-madrid", "atleti-madrid", "2024-06-22", "20:00", "Liga", "1-0", "Victoria"],
				["6", "atleti-madrid", "atleti-madrid", "2024-06-21", "20:00", "Liga", "1-0", "Victoria"]]

	for partido in partidos:

		conexion.insertarPartido(partido)

	assert conexion.ultimo_ano("atleti-madrid")==2024

def test_ultimo_ano_otros_equipos(conexion):

	conexion.insertarEquipo("atleti-madrid")

	conexion.insertarEquipo("inter")

	partidos=[["1", "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga", "1-0", "Victoria"],
				["2", "atleti-madrid", "atleti-madrid", "2018-06-22", "20:00", "Liga", "1-0", "Victoria"],
				["3", "inter", "atleti-madrid", "2024-06-21", "20:00", "Liga", "1-0", "Victoria"],
				["4", "atleti-madrid", "atleti-madrid", "2010-05-22", "20:00", "Liga", "1-0", "Victoria"],
				["5", "atleti-madrid", "atleti-madrid", "2019-07-11", "20:00", "Liga", "1-0", "Victoria"],
				["6", "inter", "inter", "2024-06-21", "20:00", "Liga", "1-0", "Victoria"],
				["7", "atleti-madrid", "atleti-madrid", "2024-06-22", "20:00", "Liga", "1-0", "Victoria"],
				["8", "atleti-madrid", "atleti-madrid", "2024-06-21", "20:00", "Liga", "1-0", "Victoria"],
				["9", "inter", "inter", "2025-06-21", "20:00", "Liga", "1-0", "Victoria"]]

	for partido in partidos:

		conexion.insertarPartido(partido)

	assert conexion.ultimo_ano("atleti-madrid")==2024

def test_obtener_partidos_sin_estadio_tabla_vacia(conexion):

	assert not conexion.obtenerPartidosSinEstadio()

def test_obtener_partidos_sin_estadio_todos_existen(conexion):

	conexion.insertarEquipo("atleti-madrid")

	partidos=[[f"{numero}", "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga", "1-0", "Victoria"] for numero in range(1, 21)]

	for partido in partidos:

		conexion.insertarPartido(partido)

		estadio=[f"estadio-{partido[0]}", 1, "Calderon", "Paseo de los Melancolicos",
					40, -3, "Madrid", 55, 1957, 100, 50, "Telefono", "Cesped"]

		conexion.insertarEstadio(estadio)

		conexion.insertarPartidoEstadio((partido[0], f"estadio-{partido[0]}"))

	assert not conexion.obtenerPartidosSinEstadio()

@pytest.mark.parametrize(["numero_partidos"],
	[(3,),(5,),(77,),(3,),(99,),(6,),(10,),(90,),(150,),(200,)]
)
def test_obtener_partidos_sin_estadio_ninguno_existe(conexion, numero_partidos):

	conexion.insertarEquipo("atleti-madrid")

	partidos=[[f"{numero}", "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga", "1-0", "Victoria"] for numero in range(1, numero_partidos+1)]

	for partido in partidos:

		conexion.insertarPartido(partido)

		estadio=[f"estadio-{partido[0]}", 1, "Calderon", "Paseo de los Melancolicos",
					40, -3, "Madrid", 55, 1957, 100, 50, "Telefono", "Cesped"]

		conexion.insertarEstadio(estadio)

	assert len(conexion.obtenerPartidosSinEstadio())==numero_partidos

@pytest.mark.parametrize(["faltantes"],
	[(1,),(5,),(77,),(3,),(99,),(6,),(10,),(90,),(150,),(200,)]
)
def test_obtener_partidos_sin_estadio_faltantes(conexion, faltantes):

	conexion.insertarEquipo("atleti-madrid")

	partidos=[[f"{numero}", "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga", "1-0", "Victoria"] for numero in range(1, 201)]

	for partido in partidos:

		conexion.insertarPartido(partido)

	for partido in partidos[:-faltantes]:

		estadio=[f"estadio-{partido[0]}", 1, "Calderon", "Paseo de los Melancolicos",
					40, -3, "Madrid", 55, 1957, 100, 50, "Telefono", "Cesped"]

		conexion.insertarEstadio(estadio)

		conexion.insertarPartidoEstadio((partido[0], f"estadio-{partido[0]}"))

	assert len(conexion.obtenerPartidosSinEstadio())==faltantes

def test_obtener_partidos_sin_competicion_tabla_vacia(conexion):

	assert not conexion.obtenerPartidosSinCompeticion()

def test_obtener_partidos_sin_competicion_todos_existen(conexion):

	conexion.insertarEquipo("atleti-madrid")

	conexion.insertarCompeticion("competicion")

	partidos=[[f"{numero}", "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga", "1-0", "Victoria"] for numero in range(1, 21)]

	for partido in partidos:

		conexion.insertarPartido(partido)

		conexion.insertarPartidoCompeticion((partido[0], "competicion"))

	assert not conexion.obtenerPartidosSinCompeticion()

@pytest.mark.parametrize(["numero_partidos"],
	[(3,),(5,),(77,),(3,),(99,),(6,),(10,),(90,),(150,),(200,)]
)
def test_obtener_partidos_sin_competicion_ninguno_existe(conexion, numero_partidos):

	conexion.insertarEquipo("atleti-madrid")

	conexion.insertarCompeticion("competicion")

	partidos=[[f"{numero}", "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga", "1-0", "Victoria"] for numero in range(1, numero_partidos+1)]

	for partido in partidos:

		conexion.insertarPartido(partido)

	assert len(conexion.obtenerPartidosSinCompeticion())==numero_partidos

@pytest.mark.parametrize(["faltantes"],
	[(1,),(5,),(77,),(3,),(99,),(6,),(10,),(90,),(150,),(200,)]
)
def test_obtener_partidos_sin_competicion_faltantes(conexion, faltantes):

	conexion.insertarEquipo("atleti-madrid")

	conexion.insertarCompeticion("competicion")

	partidos=[[f"{numero}", "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga", "1-0", "Victoria"] for numero in range(1, 201)]

	for partido in partidos:

		conexion.insertarPartido(partido)

	for partido in partidos[:-faltantes]:

		conexion.insertarPartidoCompeticion((partido[0], "competicion"))

	assert len(conexion.obtenerPartidosSinCompeticion())==faltantes

def test_obtener_partidos_sin_goleadores_tabla_vacia(conexion):

	assert not conexion.obtenerPartidosSinGoleadores()

def test_obtener_partidos_sin_goleadores_todos_existen(conexion):

	conexion.insertarEquipo("atleti-madrid")

	conexion.insertarJugador("nacho")

	partidos=[[f"{numero}", "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga", "1-0", "Victoria"] for numero in range(1, 21)]

	for partido in partidos:

		conexion.insertarPartido(partido)

		conexion.insertarPartidoGoleador((partido[0], "nacho", 1, 0, True))

	assert not conexion.obtenerPartidosSinGoleadores()

@pytest.mark.parametrize(["numero_partidos"],
	[(3,),(5,),(77,),(3,),(99,),(6,),(10,),(90,),(150,),(200,)]
)
def test_obtener_partidos_sin_goleadores_ninguno_existe(conexion, numero_partidos):

	conexion.insertarEquipo("atleti-madrid")

	conexion.insertarJugador("nacho")

	partidos=[[f"{numero}", "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga", "1-0", "Victoria"] for numero in range(1, numero_partidos+1)]

	for partido in partidos:

		conexion.insertarPartido(partido)

	assert len(conexion.obtenerPartidosSinGoleadores())==numero_partidos

@pytest.mark.parametrize(["faltantes"],
	[(1,),(5,),(77,),(3,),(99,),(6,),(10,),(90,),(150,),(200,)]
)
def test_obtener_partidos_sin_goleadores_faltantes(conexion, faltantes):

	conexion.insertarEquipo("atleti-madrid")

	conexion.insertarJugador("nacho")

	partidos=[[f"{numero}", "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga", "1-0", "Victoria"] for numero in range(1, 201)]

	for partido in partidos:

		conexion.insertarPartido(partido)

	for partido in partidos[:-faltantes]:

		conexion.insertarPartidoGoleador((partido[0], "nacho", 1, 0, True))

	assert len(conexion.obtenerPartidosSinGoleadores())==faltantes

@pytest.mark.parametrize(["numero_partidos"],
	[(3,),(5,),(77,),(3,),(99,),(6,),(10,),(90,),(150,),(200,)]
)
def test_obtener_partidos_sin_goleadores_ninguno_existe_sin_goles(conexion, numero_partidos):

	conexion.insertarEquipo("atleti-madrid")

	conexion.insertarJugador("nacho")

	partidos=[[f"{numero}", "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga", "0-0", "Victoria"] for numero in range(1, numero_partidos+1)]

	for partido in partidos:

		conexion.insertarPartido(partido)

	assert not conexion.obtenerPartidosSinGoleadores()

def test_obtener_partidos_sin_alineaciones_tabla_vacia(conexion):

	assert not conexion.obtenerPartidosSinAlineaciones()

def test_obtener_partidos_sin_alineaciones_todos_existen(conexion):

	conexion.insertarEquipo("atleti-madrid")

	conexion.insertarJugador("nacho")

	partidos=[[f"{numero}", "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga", "1-0", "Victoria"] for numero in range(1, 21)]

	for partido in partidos:

		conexion.insertarPartido(partido)

		conexion.insertarPartidoJugador((partido[0], "nacho", 13, 6.8, True, True, 1))

	assert not conexion.obtenerPartidosSinAlineaciones()

@pytest.mark.parametrize(["numero_partidos"],
	[(3,),(5,),(77,),(3,),(99,),(6,),(10,),(90,),(150,),(200,)]
)
def test_obtener_partidos_sin_alineaciones_ninguno_existe(conexion, numero_partidos):

	conexion.insertarEquipo("atleti-madrid")

	conexion.insertarJugador("nacho")

	partidos=[[f"{numero}", "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga", "1-0", "Victoria"] for numero in range(1, numero_partidos+1)]

	for partido in partidos:

		conexion.insertarPartido(partido)

	assert len(conexion.obtenerPartidosSinAlineaciones())==numero_partidos

@pytest.mark.parametrize(["faltantes"],
	[(1,),(5,),(77,),(3,),(99,),(6,),(10,),(90,),(150,),(200,)]
)
def test_obtener_partidos_sin_alineaciones_faltantes(conexion, faltantes):

	conexion.insertarEquipo("atleti-madrid")

	conexion.insertarJugador("nacho")

	partidos=[[f"{numero}", "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga", "1-0", "Victoria"] for numero in range(1, 201)]

	for partido in partidos:

		conexion.insertarPartido(partido)

	for partido in partidos[:-faltantes]:

		conexion.insertarPartidoJugador((partido[0], "nacho", 13, 6.8, True, True, 1))

	assert len(conexion.obtenerPartidosSinAlineaciones())==faltantes