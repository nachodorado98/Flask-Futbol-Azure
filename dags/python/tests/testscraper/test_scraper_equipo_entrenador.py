import pytest
from bs4 import BeautifulSoup as bs4
import pandas as pd

from src.scrapers.scraper_equipo_entrenador import ScraperEquipoEntrenador
from src.scrapers.excepciones_scrapers import PaginaError, EquipoEntrenadorError

def test_crear_objeto_scraper_equipo_entrenador():

	scraper=ScraperEquipoEntrenador("equipo")

def test_scraper_equipo_entrenador_realizar_peticion_error_redirecciona(scraper):

	scraper=ScraperEquipoEntrenador("redireccion_equipo")

	with pytest.raises(PaginaError):

		scraper._Scraper__realizarPeticion()

def test_scraper_equipo_entrenador_realizar_peticion(scraper_equipo_entrenador):

	contenido=scraper_equipo_entrenador._Scraper__realizarPeticion()

	assert isinstance(contenido, bs4)

@pytest.mark.parametrize(["equipo"],
	[("kakamega-homeboyz",),("cd-valdehornillo-a-senior",),("seleccion-santa-amalia",)]
)
def test_scraper_equipo_entrenador_obtener_tabla_entrenador_no_existe(equipo):

	scraper_equipo_entrenador=ScraperEquipoEntrenador(equipo)

	contenido=scraper_equipo_entrenador._Scraper__realizarPeticion()

	with pytest.raises(EquipoEntrenadorError):

		scraper_equipo_entrenador._ScraperEquipoEntrenador__contenido_tabla_entrenador(contenido)

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("sporting-gijon",)]
)
def test_scraper_equipo_entrenador_obtener_tabla_entrenador(equipo):

	scraper_equipo_entrenador=ScraperEquipoEntrenador(equipo)

	contenido=scraper_equipo_entrenador._Scraper__realizarPeticion()

	tabla_entrenador=scraper_equipo_entrenador._ScraperEquipoEntrenador__contenido_tabla_entrenador(contenido)

	assert tabla_entrenador is not None

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("sporting-gijon",)]
)
def test_scraper_equipo_entrenador_obtener_entrenador(equipo):

	scraper_equipo_entrenador=ScraperEquipoEntrenador(equipo)

	contenido=scraper_equipo_entrenador._Scraper__realizarPeticion()

	tabla_entrenador=scraper_equipo_entrenador._ScraperEquipoEntrenador__contenido_tabla_entrenador(contenido)

	entrenador=scraper_equipo_entrenador._ScraperEquipoEntrenador__obtener_entrenador(tabla_entrenador)

	assert len(entrenador)==5

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("sporting-gijon",)]
)
def test_scraper_equipo_entrenador_obtener_estadisticas(equipo):

	scraper_equipo_entrenador=ScraperEquipoEntrenador(equipo)

	contenido=scraper_equipo_entrenador._Scraper__realizarPeticion()

	tabla_entrenador=scraper_equipo_entrenador._ScraperEquipoEntrenador__contenido_tabla_entrenador(contenido)

	estadisticas=scraper_equipo_entrenador._ScraperEquipoEntrenador__obtener_estadisticas(tabla_entrenador)

	assert len(estadisticas)==12
	assert "" in estadisticas
	assert "G" in estadisticas
	assert "E" in estadisticas
	assert "P" in estadisticas

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("sporting-gijon",)]
)
def test_scraper_equipo_entrenador_obtener_data_limpia(equipo):

	scraper_equipo_entrenador=ScraperEquipoEntrenador(equipo)

	contenido=scraper_equipo_entrenador._Scraper__realizarPeticion()

	tabla_entrenador=scraper_equipo_entrenador._ScraperEquipoEntrenador__contenido_tabla_entrenador(contenido)

	data_limpia=scraper_equipo_entrenador._ScraperEquipoEntrenador__obtenerDataLimpia(tabla_entrenador)

	assert isinstance(data_limpia, pd.DataFrame)

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",)]
)
def test_scraper_equipo_entrenador_obtener_entrenador_equipo_error(endpoint):

	scraper=ScraperEquipoEntrenador(endpoint)

	with pytest.raises(EquipoEntrenadorError):

		scraper.obtenerEntrenadorEquipo()

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("barcelona",),("sporting-gijon",)]
)
def test_scraper_equipo_entrenador_obtener_entrenador_equipo(equipo):

	scraper=ScraperEquipoEntrenador(equipo)

	df_entrenador=scraper.obtenerEntrenadorEquipo()

	assert isinstance(df_entrenador, pd.DataFrame)