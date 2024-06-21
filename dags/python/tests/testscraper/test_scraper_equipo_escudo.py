import pytest
from bs4 import BeautifulSoup as bs4
import pandas as pd

from src.scrapers.scraper_equipo_escudo import ScraperEquipoEscudo
from src.scrapers.excepciones_scrapers import PaginaError, EquipoEscudoError

def test_crear_objeto_scraper_equipo_escudo():

	scraper=ScraperEquipoEscudo("equipo")

def test_scraper_equipo_escudo_realizar_peticion_error_redirecciona(scraper):

	scraper=ScraperEquipoEscudo("redireccion_equipo")

	with pytest.raises(PaginaError):

		scraper._Scraper__realizarPeticion()

def test_scraper_equipo_escudo_realizar_peticion(scraper_equipo_escudo):

	contenido=scraper_equipo_escudo._Scraper__realizarPeticion()

	assert isinstance(contenido, bs4)

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("sporting-gijon",)]
)
def test_scraper_equipo_escudo_obtener_tabla_cabecera(equipo):

	scraper_equipo_escudo=ScraperEquipoEscudo(equipo)

	contenido=scraper_equipo_escudo._Scraper__realizarPeticion()

	tabla_cabecera=scraper_equipo_escudo._ScraperEquipoEscudo__contenido_tabla_cabecera(contenido)

	assert tabla_cabecera is not None

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("sporting-gijon",),("merida-cp",),("cf-extremadura",)]
)
def test_scraper_equipo_escudo_obtener_escudo(equipo):

	scraper_equipo_escudo=ScraperEquipoEscudo(equipo)

	contenido=scraper_equipo_escudo._Scraper__realizarPeticion()

	tabla_cabecera=scraper_equipo_escudo._ScraperEquipoEscudo__contenido_tabla_cabecera(contenido)

	imagen_escudo=scraper_equipo_escudo._ScraperEquipoEscudo__obtener_escudo(tabla_cabecera)

	assert imagen_escudo.endswith(".png") or imagen_escudo.endswith(".jpg")
	assert imagen_escudo.startswith("https://cdn.resfu.com/img_data/equipos") or imagen_escudo.startswith("https://cdn.resfu.com/img_data/escudos/medium")

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("sporting-gijon",),("merida-cp",),("cf-extremadura",)]
)
def test_scraper_equipo_escudo_obtener_puntuacion(equipo):

	scraper_equipo_escudo=ScraperEquipoEscudo(equipo)

	contenido=scraper_equipo_escudo._Scraper__realizarPeticion()

	tabla_cabecera=scraper_equipo_escudo._ScraperEquipoEscudo__contenido_tabla_cabecera(contenido)

	puntuacion=scraper_equipo_escudo._ScraperEquipoEscudo__obtener_puntuacion(tabla_cabecera)

	assert isinstance(int(puntuacion), int)

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("sporting-gijon",)]
)
def test_scraper_equipo_escudo_obtener_data_limpia(equipo):

	scraper_equipo_escudo=ScraperEquipoEscudo(equipo)

	contenido=scraper_equipo_escudo._Scraper__realizarPeticion()

	tabla_cabecera=scraper_equipo_escudo._ScraperEquipoEscudo__contenido_tabla_cabecera(contenido)

	data_limpia=scraper_equipo_escudo._ScraperEquipoEscudo__obtenerDataLimpia(tabla_cabecera)

	assert isinstance(data_limpia, pd.DataFrame)

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",)]
)
def test_scraper_equipo_escudo_obtener_escudo_equipo_error(endpoint):

	scraper=ScraperEquipoEscudo(endpoint)

	with pytest.raises(EquipoEscudoError):

		scraper.obtenerEscudoEquipo()

@pytest.mark.parametrize(["equipo"],
	[("atletico-madrid",),("liverpool",),("barcelona",),("sporting-gijon",)]
)
def test_scraper_equipo_escudo_obtener_escudo_equipo(equipo):

	scraper=ScraperEquipoEscudo(equipo)

	df_escudo=scraper.obtenerEscudoEquipo()

	assert isinstance(df_escudo, pd.DataFrame)