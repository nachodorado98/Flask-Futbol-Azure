def test_tabla_estadios_vacia(conexion):

	conexion.c.execute("SELECT * FROM estadios")

	assert not conexion.c.fetchall()

def test_existe_estadio_no_existe(conexion):

	assert not conexion.existe_estadio("estadio")

def test_existe_estadio(conexion_entorno):

	assert conexion_entorno.existe_estadio("metropolitano")

def test_obtener_estadio_no_existe(conexion):

	assert not conexion.obtenerEstadio("metropolitano")

def test_obtener_estadio(conexion_entorno):

	assert conexion_entorno.obtenerEstadio("metropolitano")

def test_obtener_equipo_estadio_no_existe(conexion):

	assert not conexion.obtenerEquipoEstadio("metropolitano")

def test_obtener_equipo_estadio(conexion_entorno):

	equipo=conexion_entorno.obtenerEquipoEstadio("metropolitano")

	assert len(equipo)==1

def test_obtener_equipo_estadio_compartido(conexion_entorno):

	conexion_entorno.c.execute("""INSERT INTO equipos (Equipo_Id) VALUES('atletico-madrid-b')""")

	conexion_entorno.c.execute("""INSERT INTO equipo_estadio
								VALUES('atletico-madrid-b', 'metropolitano')""")

	conexion_entorno.confirmar()

	equipos=conexion_entorno.obtenerEquipoEstadio("metropolitano")

	assert len(equipos)==2