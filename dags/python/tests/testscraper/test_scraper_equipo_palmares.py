import pytest
from bs4 import BeautifulSoup as bs4
import pandas as pd

from src.scrapers.scraper_equipo_palmares import ScraperEquipoPalmares
from src.scrapers.excepciones_scrapers import PaginaError, EquipoPalmaresError

def test_crear_objeto_scraper_equipo_palmares():

	scraper=ScraperEquipoPalmares("equipo")

def test_scraper_equipo_palmares_realizar_peticion_error_redirecciona(scraper):

	scraper=ScraperEquipoPalmares("redireccion_equipo")

	with pytest.raises(PaginaError):

		scraper._Scraper__realizarPeticion()

def test_scraper_equipo_palmares_realizar_peticion(scraper_equipo_palmares):

	contenido=scraper_equipo_palmares._Scraper__realizarPeticion()

	assert isinstance(contenido, bs4)

@pytest.mark.parametrize(["equipo"],
	[("cd-valdehornillo-a-senior",),("seleccion-santa-amalia",)]
)
def test_scraper_equipo_palmares_obtener_tabla_palmares_error_no_tiene(equipo):

	scraper_equipo_palmares=ScraperEquipoPalmares(equipo)

	with pytest.raises(PaginaError):

		scraper_equipo_palmares._Scraper__realizarPeticion()

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("sporting-gijon",)]
)
def test_scraper_equipo_palmares_obtener_tabla_palmares(equipo):

	scraper_equipo_palmares=ScraperEquipoPalmares(equipo)

	contenido=scraper_equipo_palmares._Scraper__realizarPeticion()

	tabla_palmares=scraper_equipo_palmares._ScraperEquipoPalmares__contenido_tabla_palmares(contenido)

	assert tabla_palmares is not None

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("sporting-gijon",)]
)
def test_scraper_equipo_palmares_obtener_tablas_titulos(equipo):

	scraper_equipo_palmares=ScraperEquipoPalmares(equipo)

	contenido=scraper_equipo_palmares._Scraper__realizarPeticion()

	tabla_palmares=scraper_equipo_palmares._ScraperEquipoPalmares__contenido_tabla_palmares(contenido)

	tablas_titulos=scraper_equipo_palmares._ScraperEquipoPalmares__obtener_tablas_titulos(tabla_palmares)

	assert tablas_titulos

	for tabla in tablas_titulos:

		assert len(tabla)==5
		assert tabla[2].endswith(".png") or tabla[2].endswith(".jpg")
		assert tabla[2].startswith("https://cdn.resfu.com/media/img/league_logos/")
		assert tabla[3].endswith(".png") or tabla[3].endswith(".jpg")
		assert tabla[3].startswith("https://cdn.resfu.com/img_data/competiciones/") or tabla[3].startswith("https://cdn.resfu.com/media/img/trophy_pic/")

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("barcelona",),("sporting-gijon",)]
)
def test_scraper_equipo_palmares_obtener_data_limpia(equipo):

	scraper_equipo_palmares=ScraperEquipoPalmares(equipo)

	contenido=scraper_equipo_palmares._Scraper__realizarPeticion()

	tabla_palmares=scraper_equipo_palmares._ScraperEquipoPalmares__contenido_tabla_palmares(contenido)

	data_limpia=scraper_equipo_palmares._ScraperEquipoPalmares__obtenerDataLimpia(tabla_palmares)

	assert isinstance(data_limpia, pd.DataFrame)

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",)]
)
def test_scraper_equipo_palmares_obtener_palmares_equipo_error(endpoint):

	scraper=ScraperEquipoPalmares(endpoint)

	with pytest.raises(EquipoPalmaresError):

		scraper.obtenerEstadioPalmares()

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("barcelona",),("sporting-gijon",)]
)
def test_scraper_equipo_palmares_obtener_palmares_equipo(equipo):

	scraper=ScraperEquipoPalmares(equipo)

	df_palmares=scraper.obtenerEstadioPalmares()

	assert isinstance(df_palmares, pd.DataFrame)