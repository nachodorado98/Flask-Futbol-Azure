import pytest
from bs4 import BeautifulSoup as bs4
import pandas as pd

from src.scrapers.scraper_entrenador_equipos import ScraperEntrenadorEquipos
from src.scrapers.excepciones_scrapers import PaginaError, EntrenadorEquiposError

def test_crear_objeto_scraper_entrenador_equipos():

	scraper=ScraperEntrenadorEquipos("entrenador")

# def test_scraper_entrenador_equipos_realizar_peticion_error_redirecciona(scraper):

# 	scraper=ScraperEntrenadorEquipos("redireccion_entrenador")

# 	with pytest.raises(PaginaError):

# 		scraper._Scraper__realizarPeticion()

def test_scraper_entrenador_equipos_realizar_peticion(scraper_entrenador_equipos):

	contenido=scraper_entrenador_equipos._Scraper__realizarPeticion()

	assert isinstance(contenido, bs4)

def test_scraper_entrenador_equipos_obtener_contenedor_entrenados(scraper_entrenador_equipos):

	contenido=scraper_entrenador_equipos._Scraper__realizarPeticion()

	contenedor_entrenados=scraper_entrenador_equipos._ScraperEntrenadorEquipos__contenido_contenedor_entrenados(contenido)

	assert contenedor_entrenados is not None

@pytest.mark.parametrize(["entrenador"],
	[("diego-simeone-13",),("hansi-flick-8143",),("thiago-motta-21853",),("fernando-torres-47437",)]
)
def test_scraper_entrenador_equipos_obtener_informacion_equipos(entrenador):

	scraper_entrenador_equipos=ScraperEntrenadorEquipos(entrenador)

	contenido=scraper_entrenador_equipos._Scraper__realizarPeticion()

	contenedor_entrenados=scraper_entrenador_equipos._ScraperEntrenadorEquipos__contenido_contenedor_entrenados(contenido)

	info_equipos=scraper_entrenador_equipos._ScraperEntrenadorEquipos__informacion_equipos(contenedor_entrenados)

	for info in info_equipos:

		assert len(info)==8
		assert info[0].startswith("https://es.besoccer.com/equipo/")

@pytest.mark.parametrize(["entrenador"],
	[("diego-simeone-13",),("hansi-flick-8143",),("thiago-motta-21853",),("fernando-torres-47437",)]
)
def test_scraper_entrenador_equipos_obtener_data_limpia(entrenador):

	scraper_entrenador_equipos=ScraperEntrenadorEquipos(entrenador)

	contenido=scraper_entrenador_equipos._Scraper__realizarPeticion()

	contenedor_entrenados=scraper_entrenador_equipos._ScraperEntrenadorEquipos__contenido_contenedor_entrenados(contenido)

	data_limpia=scraper_entrenador_equipos._ScraperEntrenadorEquipos__obtenerDataLimpia(contenedor_entrenados)

	assert isinstance(data_limpia, pd.DataFrame)

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",)]
)
def test_scraper_entrenador_equipos_obtener_entrenador_equipos_error(endpoint):

	scraper=ScraperEntrenadorEquipos(endpoint)

	with pytest.raises(EntrenadorEquiposError):

		scraper.obtenerEntrenadorEquipos()

@pytest.mark.parametrize(["entrenador"],
	[("diego-simeone-13",),("hansi-flick-8143",),("thiago-motta-21853",),("fernando-torres-47437",)]
)
def test_scraper_entrenador_equipos_obtener_entrenador_equipos(entrenador):

	scraper=ScraperEntrenadorEquipos(entrenador)

	df_entrenador_equipos=scraper.obtenerEntrenadorEquipos()

	assert isinstance(df_entrenador_equipos, pd.DataFrame)