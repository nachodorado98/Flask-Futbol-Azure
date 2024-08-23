import pytest

def test_tabla_temporada_jugadores_vacia(conexion):

	conexion.c.execute("SELECT * FROM temporada_jugadores")

	assert not conexion.c.fetchall()

def test_insertar_temporada_jugadores(conexion):

	conexion.insertarTemporadaJugadores(2024)

	conexion.c.execute("SELECT * FROM temporada_jugadores")

	assert len(conexion.c.fetchall())==1

def test_ultimo_ano_jugadores_tabla_vacia(conexion):

	assert conexion.ultimo_ano_jugadores() is None

@pytest.mark.parametrize(["temporada"],
	[(3,),(5,),(77,),(3,),(99,),(6,),(10,),(90,),(150,),(200,)]
)
def test_ultimo_ano_jugadores(conexion, temporada):

	conexion.insertarTemporadaJugadores(temporada)

	assert conexion.ultimo_ano_jugadores()==temporada

@pytest.mark.parametrize(["temporada_antigua", "temporada_nueva"],
	[
		(None, 1),
		(5, 6),
		(77, 22),
		(3, 0),
		(99, None),
		(6, 13),
		(10, 90),
		(90, 1)
	]
)
def test_actualizar_temporada_jugadores(conexion, temporada_antigua, temporada_nueva):

	conexion.insertarTemporadaJugadores(temporada_antigua)

	assert conexion.ultimo_ano_jugadores()==temporada_antigua

	conexion.actualizarTemporadaJugadores(temporada_nueva)

	assert conexion.ultimo_ano_jugadores()==temporada_nueva