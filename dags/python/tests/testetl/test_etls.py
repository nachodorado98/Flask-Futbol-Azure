import pytest
import pandas as pd

from src.etls import ETL_Equipos_Liga
from src.scrapers.excepciones_scrapers import EquiposLigaError

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",),("usa",)]
)
def test_etl_equipos_liga_error(endpoint):

	with pytest.raises(EquiposLigaError):

		ETL_Equipos_Liga(endpoint)

@pytest.mark.parametrize(["endpoint"],
	[("primera",),("segunda",),("/primera/2019",), ("bundesliga",),
	("premier",),("/primera/1996",),("/segunda/1990",)]
)
def test_etl_equipos_liga(conexion, endpoint):

	ETL_Equipos_Liga(endpoint)

	conexion.c.execute("SELECT * FROM equipos")

	assert conexion.c.fetchall()

@pytest.mark.parametrize(["endpoint"],
	[("primera",),("segunda",),("/primera/2019",), ("bundesliga",),("premier",),
	("/primera/1996",),("/segunda/1990",)]
)
def test_etl_equipos_liga_equipos_existentes(conexion, endpoint):

	ETL_Equipos_Liga(endpoint)

	conexion.c.execute("SELECT * FROM equipos")

	numero_registros=len(conexion.c.fetchall())

	ETL_Equipos_Liga(endpoint)

	conexion.c.execute("SELECT * FROM equipos")

	numero_registros_nuevos=len(conexion.c.fetchall())

	assert numero_registros==numero_registros_nuevos

@pytest.mark.parametrize(["endpoint", "nuevos_equipos"],
	[
		("primera",12),
		("segunda",4),
		("/primera/2019",2),
		("bundesliga",5),
		("premier",3),
		("/primera/1996",7),
		("/segunda/1990",1)
	]
)
def test_etl_equipos_liga_equipos_nuevos_equipos(conexion, endpoint, nuevos_equipos):

	ETL_Equipos_Liga(endpoint)

	conexion.c.execute(f"""DELETE FROM equipos
							WHERE Equipo_Id IN (SELECT Equipo_Id
											    FROM equipos
											    ORDER BY RANDOM()
											    LIMIT {nuevos_equipos})""")

	conexion.confirmar()

	conexion.c.execute("SELECT * FROM equipos")

	numero_registros=len(conexion.c.fetchall())

	ETL_Equipos_Liga(endpoint)

	conexion.c.execute("SELECT * FROM equipos")

	numero_registros_nuevos=len(conexion.c.fetchall())

	assert numero_registros+nuevos_equipos==numero_registros_nuevos

@pytest.mark.parametrize(["temporada1", "temporada2"],
	[
		("primera/2019","primera/2020"),
		("primera/2024","primera/2023"),
		("premier/2014","premier/2015")
	]
)
def test_etl_equipos_liga_equipos_nueva_temporada(conexion, temporada1, temporada2):

	ETL_Equipos_Liga(temporada1)

	conexion.c.execute("SELECT * FROM equipos")

	numero_registros=len(conexion.c.fetchall())

	ETL_Equipos_Liga(temporada2)

	conexion.c.execute("SELECT * FROM equipos")

	numero_registros_nuevos=len(conexion.c.fetchall())

	assert numero_registros+3==numero_registros_nuevos