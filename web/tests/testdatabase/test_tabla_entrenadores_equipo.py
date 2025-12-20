import pytest

def test_tabla_entrenadores_equipo_vacia(conexion):

	conexion.c.execute("SELECT * FROM entrenadores_equipo")

	assert not conexion.c.fetchall()

def test_obtener_equipos_entrenador_no_existe_entrenador(conexion):

	assert not conexion.obtenerEquiposEntrenador("diego-pablo")

def test_obtener_equipos_entrenador_no_tiene(conexion_entorno):

	conexion_entorno.c.execute("""INSERT INTO entrenadores
						VALUES('nacho', 'Nacho', 'atletico-madrid', 'ar', '13', 100)""")

	conexion_entorno.confirmar()

	assert not conexion_entorno.obtenerEquiposEntrenador("nacho")

def test_obtener_equipos_entrenador(conexion_entorno):

	equipos=conexion_entorno.obtenerEquiposEntrenador("diego-pablo")

	assert len(equipos)==1

@pytest.mark.parametrize(["numero_equipos"],
	[(2,),(10,),(13,),(7,)]
)
def test_obtener_equipos_entrenador_varios(conexion_entorno, numero_equipos):

	for numero in range(numero_equipos):

		conexion_entorno.c.execute(f"""INSERT INTO equipos (Equipo_Id)
							VALUES('equipo{numero}')""")

		conexion_entorno.c.execute(f"""INSERT INTO entrenadores_equipo
							VALUES('diego-pablo', 'equipo{numero}', 1000, '2013-', 1000, 0, 0, '4-4-2')""")

		conexion_entorno.confirmar()

	equipos=conexion_entorno.obtenerEquiposEntrenador("diego-pablo")

	assert len(equipos)==numero_equipos+1