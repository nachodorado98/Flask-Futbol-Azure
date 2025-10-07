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

def test_obtener_estadios_no_existen(conexion):

	assert not conexion.obtenerDatosEstadios()

def test_obtener_estadios(conexion_entorno):

	assert conexion_entorno.obtenerDatosEstadios()

def test_obtener_estadios_dos_equipos(conexion_entorno):

	conexion_entorno.c.execute("""INSERT INTO equipos (Equipo_Id, Escudo, Codigo_Pais)
						VALUES('atletico-madrid-b', 1000, 'es')""")

	conexion_entorno.c.execute("""INSERT INTO equipo_estadio
						VALUES('atletico-madrid-b', 'metropolitano')""")

	conexion_entorno.confirmar()

	estadios=conexion_entorno.obtenerDatosEstadios()

	assert len(estadios)==1

def test_obtener_estadios_top_no_existe(conexion):

	assert not conexion.obtenerDatosEstadiosTop(5)

def test_obtener_estadios_top(conexion):

	conexion.c.execute("""INSERT INTO estadios
						VALUES('estadio1', '1', 'Est', 'Dir', '4.1', '-3.5', 'Madrid', 13647, 2017, 105, 68, 'Tel', 'Ces'),
								('estadio2', '1', 'Est', 'Dir', '4.1', '-3.5', 'Madrid', 100000, 2017, 105, 68, 'Tel', 'Ces'),
								('estadio3', '1', 'Est', 'Dir', '4.1', '-3.5', 'Madrid', 20001, 2017, 105, 68, 'Tel', 'Ces'),
								('estadio4', '1', 'Est', 'Dir', '4.1', '-3.5', 'Madrid', 35000, 2017, 105, 68, 'Tel', 'Ces'),
								('estadio5', '1', 'Est', 'Dir', '4.1', '-3.5', 'Madrid', 66000, 2017, 105, 68, 'Tel', 'Ces'),
								('estadio6', '1', 'Est', 'Dir', '4.1', '-3.5', 'Madrid', 10, 2017, 105, 68, 'Tel', 'Ces'),
								('estadio7', '1', 'Est', 'Dir', '4.1', '-3.5', 'Madrid', 22500, 2017, 105, 68, 'Tel', 'Ces'),
								('estadio8', '1', 'Est', 'Dir', '4.1', '-3.5', 'Madrid', 75677, 2017, 105, 68, 'Tel', 'Ces')""")

	conexion.confirmar()

	estadios_top=conexion.obtenerDatosEstadiosTop(5)

	assert estadios_top[0][0]=="estadio2"
	assert estadios_top[-1][0]=="estadio7"

def test_estadio_asistido_usuario_no_existe_estadio(conexion):

	assert not conexion.estadio_asistido_usuario("nacho", "estadio")

def test_estadio_asistido_usuario_no_existe_usuario(conexion_entorno):

	assert not conexion_entorno.estadio_asistido_usuario("nacho", "metropolitano")

def test_estadio_asistido_usuario_no_asistido(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	assert not conexion_entorno.estadio_asistido_usuario("nacho", "metropolitano")

def test_estadio_asistido_usuario(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

	assert conexion_entorno.estadio_asistido_usuario("nacho", "metropolitano")

def test_ultimo_partido_estadio_no_existe_estadio(conexion):

	assert not conexion.obtenerUltimoPartidoEstadio("metropolitano")

def test_ultimo_partido_estadio_no_existen_partidos(conexion_entorno):

	conexion_entorno.c.execute("DELETE FROM partidos")

	conexion_entorno.confirmar()	

	assert not conexion_entorno.obtenerUltimoPartidoEstadio("metropolitano")

def test_ultimo_partido_estadio(conexion_entorno):

	assert conexion_entorno.obtenerUltimoPartidoEstadio("metropolitano")

def test_ultimo_partido_estadio_existen_varios(conexion_entorno):

	for numero in range(8):

		conexion_entorno.c.execute(f"""INSERT INTO partidos
									VALUES('{numero}', 'atletico-madrid', 'atletico-madrid', '201{numero}-06-22', '20:00', 'Liga', '1-0', 'Victoria')""")

		conexion_entorno.c.execute(f"""INSERT INTO partido_estadio
									VALUES('{numero}', 'metropolitano')""")

	conexion_entorno.confirmar()

	ultimo_partido_estadio=conexion_entorno.obtenerUltimoPartidoEstadio("metropolitano")

	assert ultimo_partido_estadio[2]=="22/06/2019"

def test_ultimo_partido_estadio_asistido_no_existe_estadio(conexion):

	assert not conexion.obtenerUltimoPartidoAsistidoEstadio("metropolitano", "nacho")

def test_ultimo_partido_estadio_asistido_no_existen_partidos(conexion_entorno):

	conexion_entorno.c.execute("DELETE FROM partidos")

	conexion_entorno.confirmar()	

	assert not conexion_entorno.obtenerUltimoPartidoAsistidoEstadio("metropolitano", "nacho")

def test_ultimo_partido_estadio_asistido_no_existe_usuario(conexion_entorno):

	assert not conexion_entorno.obtenerUltimoPartidoAsistidoEstadio("metropolitano", "nacho")

def test_ultimo_partido_estadio_asistido_no_asistido(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	assert not conexion_entorno.obtenerUltimoPartidoAsistidoEstadio("metropolitano", "nacho")

def test_ultimo_partido_estadio_asistido(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

	assert conexion_entorno.obtenerUltimoPartidoAsistidoEstadio("metropolitano", "nacho")

def test_ultimo_partido_estadio_asistido_existen_varios(conexion_entorno):

	conexion_entorno.insertarUsuario("nacho", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103, "atletico-madrid")

	conexion_entorno.insertarPartidoAsistido("20190622", "nacho", "comentario")

	for numero in range(8):

		conexion_entorno.c.execute(f"""INSERT INTO partidos
									VALUES('{numero}', 'atletico-madrid', 'atletico-madrid', '201{numero}-06-22', '20:00', 'Liga', '1-0', 'Victoria')""")

		conexion_entorno.c.execute(f"""INSERT INTO partido_estadio
									VALUES('{numero}', 'metropolitano')""")

		conexion_entorno.insertarPartidoAsistido(numero, "nacho", "comentario")

	conexion_entorno.confirmar()

	ultimo_partido_asistido_estadio=conexion_entorno.obtenerUltimoPartidoAsistidoEstadio("metropolitano", "nacho")

	assert ultimo_partido_asistido_estadio[2]=="22/06/2019"