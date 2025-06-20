import pytest

from src.database.conexion import Conexion

@pytest.mark.parametrize(["entorno_error"],
	[("DEV",),("PRO",)]
)
def test_ejecutar_backup_conexion_entorno_error(entorno_error):

	conexion=Conexion(entorno_error)

	with pytest.raises(Exception):

		conexion.ejecutarBackUp("DEV")

@pytest.mark.parametrize(["entorno_error"],
	[("PRE",),("entorno",),("develop",),("pr",),("clona",)]
)
def test_ejecutar_backup_entorno_error(entorno_error):

	conexion=Conexion("CLONAR")

	with pytest.raises(Exception):

		conexion.ejecutarBackUp(entorno_error)

def test_ejecutar_backup():

	conexion=Conexion("CLONAR")

	conexion.ejecutarBackUp("DEV")

	conexion.c.execute("SELECT 1 FROM pg_database WHERE datname='bbdd_futbol_data_backup'")

	assert conexion.c.fetchone()

def test_ejecutar_backup_existente():

	conexion=Conexion("CLONAR")

	with pytest.raises(Exception):

		conexion.ejecutarBackUp("DEV")

	conexion.c.execute("SELECT 1 FROM pg_database WHERE datname='bbdd_futbol_data_backup'")

	assert conexion.c.fetchone()

@pytest.mark.parametrize(["entorno_error"],
	[("DEV",),("PRO",)]
)
def test_eliminar_bbdd_conexion_entorno_error(entorno_error):

	conexion=Conexion(entorno_error)

	with pytest.raises(Exception):

		conexion.eliminarBBDD("bbdd_futbol_data_backup")

def test_eliminar_bbdd_bbdd_error():

	conexion=Conexion("CLONAR")

	with pytest.raises(Exception):

		conexion.eliminarBBDD("postgres")

def test_eliminar_bbdd():

	conexion=Conexion("CLONAR")

	conexion.c.execute("SELECT 1 FROM pg_database WHERE datname='bbdd_futbol_data_backup'")

	assert conexion.c.fetchone()

	conexion.eliminarBBDD("bbdd_futbol_data_backup")

	conexion.c.execute("SELECT 1 FROM pg_database WHERE datname='bbdd_futbol_data_backup'")

	assert not conexion.c.fetchone()

def test_eliminar_bbdd_no_existe():

	conexion=Conexion("CLONAR")

	conexion.c.execute("SELECT 1 FROM pg_database WHERE datname='bbdd_futbol_data_backup'")

	assert not conexion.c.fetchone()

	conexion.eliminarBBDD("bbdd_futbol_data_backup")

	conexion.c.execute("SELECT 1 FROM pg_database WHERE datname='bbdd_futbol_data_backup'")

	assert not conexion.c.fetchone()

@pytest.mark.parametrize(["entorno_error", "bbdd"],
	[("DEV", "bbdd_futbol_data_dev"),("PRO", "bbdd_futbol_data")]
)
def test_matar_conexiones_bbdd_conexion_entorno_error(entorno_error, bbdd):

	conexion=Conexion(entorno_error)

	with pytest.raises(Exception):

		conexion.matar_conexiones_bbdd(bbdd)

def test_matar_conexiones_bbdd_bbdd_error():

	conexion=Conexion("CLONAR")

	with pytest.raises(Exception):

		conexion.matar_conexiones_bbdd("postgres")

def test_matar_conexiones_bbdd(conexion):

	conexion_postgres=Conexion("CLONAR")

	conexion_postgres.matar_conexiones_bbdd("bbdd_futbol_data_dev")

	with pytest.raises(Exception):

		conexion.c.execute("SELECT 1")