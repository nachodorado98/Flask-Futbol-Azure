def test_tabla_partidos_vacia(conexion):

	conexion.c.execute("SELECT * FROM partidos")

	assert not conexion.c.fetchall()

def test_insertar_partido(conexion):

	conexion.insertarEquipo("atleti-madrid")

	partido=[1, "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	conexion.c.execute("SELECT * FROM partidos")

	assert len(conexion.c.fetchall())==1

def test_existe_partido_no_existe(conexion):

	assert not conexion.existe_partido(1)

def test_existe_partido_existe(conexion):

	conexion.insertarEquipo("atleti-madrid")

	partido=[1, "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga", "1-0", "Victoria"]

	conexion.insertarPartido(partido)

	assert conexion.existe_partido(1)

def test_fecha_mas_reciente_tabla_vacia(conexion):

	assert conexion.fecha_mas_reciente() is None

def test_fecha_mas_reciente(conexion):

	conexion.insertarEquipo("atleti-madrid")

	partidos=[[1, "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga", "1-0", "Victoria"],
				[2, "atleti-madrid", "atleti-madrid", "2018-06-22", "20:00", "Liga", "1-0", "Victoria"],
				[3, "atleti-madrid", "atleti-madrid", "2010-05-22", "20:00", "Liga", "1-0", "Victoria"],
				[4, "atleti-madrid", "atleti-madrid", "2019-07-11", "20:00", "Liga", "1-0", "Victoria"],
				[5, "atleti-madrid", "atleti-madrid", "2024-06-22", "20:00", "Liga", "1-0", "Victoria"],
				[6, "atleti-madrid", "atleti-madrid", "2024-06-21", "20:00", "Liga", "1-0", "Victoria"]]

	for partido in partidos:

		conexion.insertarPartido(partido)

	assert conexion.fecha_mas_reciente().strftime("%Y-%m-%d")=="2024-06-22"

def test_ultimo_ano_tabla_vacia(conexion):

	assert conexion.ultimo_ano() is None

def test_ultimo_ano(conexion):

	conexion.insertarEquipo("atleti-madrid")

	partidos=[[1, "atleti-madrid", "atleti-madrid", "2019-06-22", "20:00", "Liga", "1-0", "Victoria"],
				[2, "atleti-madrid", "atleti-madrid", "2018-06-22", "20:00", "Liga", "1-0", "Victoria"],
				[3, "atleti-madrid", "atleti-madrid", "2010-05-22", "20:00", "Liga", "1-0", "Victoria"],
				[4, "atleti-madrid", "atleti-madrid", "2019-07-11", "20:00", "Liga", "1-0", "Victoria"],
				[5, "atleti-madrid", "atleti-madrid", "2024-06-22", "20:00", "Liga", "1-0", "Victoria"],
				[6, "atleti-madrid", "atleti-madrid", "2024-06-21", "20:00", "Liga", "1-0", "Victoria"]]

	for partido in partidos:

		conexion.insertarPartido(partido)

	assert conexion.ultimo_ano()==2024