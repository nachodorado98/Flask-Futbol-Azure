def test_tabla_competiciones_vacia(conexion):

	conexion.c.execute("SELECT * FROM competiciones")

	assert not conexion.c.fetchall()

def test_existe_competicion_no_existe(conexion):

	assert not conexion.existe_competicion("primera")

def test_existe_competicion_existe(conexion_entorno):

	assert conexion_entorno.existe_competicion("primera")

def test_obtener_competicion_no_existe(conexion):

	assert not conexion.obtenerDatosCompeticion("primera")

def test_obtener_competicion(conexion_entorno):

	assert conexion_entorno.obtenerDatosCompeticion("primera")

def test_obtener_competiciones_no_existen(conexion):

	assert not conexion.obtenerDatosCompeticiones()

def test_obtener_competiciones(conexion_entorno):

	assert conexion_entorno.obtenerDatosCompeticiones()

def test_obtener_competiciones_top_no_existe(conexion):

	assert not conexion.obtenerDatosCompeticionesTop(5)

def test_obtener_competiciones_top(conexion):

	conexion.c.execute("""INSERT INTO competiciones (Competicion_Id)
						VALUES('comp1'),('comp2'),('comp3'),('comp4'),('comp5'),('comp6'),('comp7')""")

	conexion.c.execute("""INSERT INTO equipos (Equipo_Id, Puntuacion, Codigo_Competicion)
									VALUES('equipo1', 10, 'comp1'),('equipo2', 100, 'comp2'),('equipo3', 22, 'comp1'),('equipo4', 101, 'comp4'),
											('equipo5', 5, 'comp1'),('equipo6', 15,'comp5'),('equipo7', 13,'comp2'),('equipo8', 1000,'comp5'),
											('equipo9', 11, 'comp6'),('equipo10', 10000,'comp7'),('equipo11', 100,'comp3'),('equipo12', 1,'comp5')""")


	conexion.confirmar()

	competiciones_top=conexion.obtenerDatosCompeticionesTop(5)

	assert competiciones_top[0][0]=="comp7"
	assert competiciones_top[-1][0]=="comp3"