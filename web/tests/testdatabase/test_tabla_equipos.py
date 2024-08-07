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