import pytest

def test_conexion(conexion):

	conexion.c.execute("SELECT current_database();")

	assert conexion.c.fetchone()["current_database"]=="bbdd_futbol_data"

	conexion.c.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")

	tablas=[tabla["relname"] for tabla in conexion.c.fetchall()]

	assert "ligas_scrapear" in tablas
	assert "equipos" in tablas
	assert "estadios" in tablas
	assert "equipo_estadio" in tablas
	assert "partidos" in tablas
	assert "proximos_partidos" in tablas
	assert "partido_estadio" in tablas
	assert "partido_competicion" in tablas
	assert "competiciones" in tablas
	assert "competiciones_campeones" in tablas
	assert "jugadores" in tablas
	assert "jugadores_equipo" in tablas
	assert "jugadores_seleccion" in tablas
	assert "partido_goleador" in tablas
	assert "entrenadores" in tablas
	assert "temporada_jugadores" in tablas
	assert "variables" in tablas
	assert "paises" in tablas
	assert "ciudades" in tablas

def test_cerrar_conexion(conexion):

	assert not conexion.bbdd.closed

	conexion.cerrarConexion()

	assert conexion.bbdd.closed

def test_tabla_vacia_no_existe(conexion):

	with pytest.raises(Exception):

		conexion.tabla_vacia("hola")

def test_tabla_vacia_llena(conexion):

	assert not conexion.tabla_vacia("ligas_scrapear")

@pytest.mark.parametrize(["tabla"],
	[("equipos",),("estadios",),("equipo_estadio",),("partidos",),("proximos_partidos",),
	("partido_estadio",),("competiciones",),("competiciones_campeones",),("partido_competicion",),
	("jugadores",),("jugadores_equipo",),("jugadores_seleccion",),("partido_goleador",),("entrenadores",),
	("temporada_jugadores",)]
)
def test_tabla_vacia(conexion, tabla):

	assert conexion.tabla_vacia(tabla)