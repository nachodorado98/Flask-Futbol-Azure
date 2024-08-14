import pytest

def test_tabla_competiciones_campeones_vacia(conexion):

	conexion.c.execute("SELECT * FROM competiciones_campeones")

	assert not conexion.c.fetchall()

def test_insertar_competicion_campeon(conexion):

	conexion.insertarCompeticion("competicion")

	datos=["competicion", 2025, "atleti"]

	conexion.insertarCampeonCompeticion(datos)

	conexion.c.execute("SELECT * FROM competiciones_campeones")

	assert len(conexion.c.fetchall())==1

def test_existe_campeon_competicion_no_existe_nada(conexion):

	assert not conexion.existe_campeon_competicion("competicion", 2025, "atleti")

def test_existe_campeon_competicion_existe_competicion(conexion):

	conexion.insertarCompeticion("competicion")

	datos=["competicion", 2024, "atleti-madrid"]

	conexion.insertarCampeonCompeticion(datos)

	assert not conexion.existe_campeon_competicion("competicion", 2025, "atleti")

def test_existe_campeon_competicion_existe_temporada(conexion):

	conexion.insertarCompeticion("competicion")

	datos=["competicion", 2025, "atleti-madrid"]

	conexion.insertarCampeonCompeticion(datos)

	assert not conexion.existe_campeon_competicion("competicion", 2025, "atleti")

def test_existe_campeon_competicion_existe(conexion):

	conexion.insertarCompeticion("competicion")

	datos=["competicion", 2025, "atleti"]

	conexion.insertarCampeonCompeticion(datos)

	assert conexion.existe_campeon_competicion("competicion", 2025, "atleti")