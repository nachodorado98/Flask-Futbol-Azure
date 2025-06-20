import pytest

from src.database.conexion import Conexion

@pytest.mark.parametrize(["entorno_error"],
	[("PRE",),("entorno",),("develop",),("pr",),("clona",)]
)
def test_conexion_error_entorno(entorno_error):

	with pytest.raises(Exception):

		Conexion(entorno_error)

def test_conexion_pro():

	conexion=Conexion("PRO")

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

def test_conexion_dev(conexion):

	conexion.c.execute("SELECT current_database();")

	assert conexion.c.fetchone()["current_database"]=="bbdd_futbol_data_dev"

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

def test_conexion_postgres():

	conexion=Conexion("CLONAR")

	conexion.c.execute("SELECT current_database();")

	assert conexion.c.fetchone()["current_database"]=="postgres"

	conexion.c.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")

	tablas=[tabla["relname"] for tabla in conexion.c.fetchall()]

	assert "ligas_scrapear" not in tablas
	assert "equipos" not in tablas
	assert "estadios" not in tablas
	assert "equipo_estadio" not in tablas
	assert "partidos" not in tablas
	assert "proximos_partidos" not in tablas
	assert "partido_estadio" not in tablas
	assert "partido_competicion" not in tablas
	assert "competiciones" not in tablas
	assert "competiciones_campeones" not in tablas
	assert "jugadores" not in tablas
	assert "jugadores_equipo" not in tablas
	assert "jugadores_seleccion" not in tablas
	assert "partido_goleador" not in tablas
	assert "entrenadores" not in tablas
	assert "temporada_jugadores" not in tablas
	assert "variables" not in tablas
	assert "paises" not in tablas
	assert "ciudades" not in tablas

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