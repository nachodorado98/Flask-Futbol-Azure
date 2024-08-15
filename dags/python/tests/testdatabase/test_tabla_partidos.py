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

	assert conexion.fecha_mas_reciente() is None

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

	assert conexion.fecha_mas_reciente().strftime("%Y-%m-%d")=="2024-06-22"

def test_ultimo_ano_tabla_vacia(conexion):

	assert conexion.ultimo_ano() is None

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

	assert conexion.ultimo_ano()==2024

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