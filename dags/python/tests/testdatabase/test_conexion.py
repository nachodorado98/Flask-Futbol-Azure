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
	assert "partido_estadio" in tablas
	assert "competiciones" in tablas
	assert "variables" in tablas

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
	[("equipos",),("estadios",),("equipo_estadio",),("partidos",),("partido_estadio",), ("competiciones",)]
)
def test_tabla_vacia(conexion, tabla):

	assert conexion.tabla_vacia(tabla)