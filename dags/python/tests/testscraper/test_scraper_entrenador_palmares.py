import pytest
from bs4 import BeautifulSoup as bs4
import pandas as pd

from src.scrapers.scraper_entrenador_palmares import ScraperEntrenadorPalmares
from src.scrapers.excepciones_scrapers import PaginaError, EntrenadorPalmaresError

def test_crear_objeto_scraper_entrenador_palmares():

	scraper=ScraperEntrenadorPalmares("entrenador")

# def test_scraper_entrenador_palmares_realizar_peticion_error_redirecciona(scraper):

# 	scraper=ScraperEntrenadorPalmares("redireccion_entrenador")

# 	with pytest.raises(PaginaError):

# 		scraper._Scraper__realizarPeticion()

def test_scraper_entrenador_palmares_realizar_peticion(scraper_entrenador_palmares):

	contenido=scraper_entrenador_palmares._Scraper__realizarPeticion()

	assert isinstance(contenido, bs4)

@pytest.mark.parametrize(["entrenador"],
	[("jakob-poulsen-63406",),("ricardo-fajardo-19230",),("alejandro-alvarez-43905",)]
)
def test_scraper_entrenador_palmares_obtener_tabla_palmares_error_no_tiene(entrenador):

	scraper_entrenador_palmares=ScraperEntrenadorPalmares(entrenador)

	contenido=scraper_entrenador_palmares._Scraper__realizarPeticion()

	with pytest.raises(EntrenadorPalmaresError):

		scraper_entrenador_palmares._ScraperEntrenadorPalmares__contenido_tabla_palmares(contenido)

@pytest.mark.parametrize(["entrenador"],
	[("diego-simeone-13",),("hansi-flick-8143",),("thiago-motta-21853",),("fernando-torres-47437",)]
)
def test_scraper_entrenador_palmares_obtener_tabla_palmares(entrenador):

	scraper_entrenador_palmares=ScraperEntrenadorPalmares(entrenador)

	contenido=scraper_entrenador_palmares._Scraper__realizarPeticion()

	tabla_palmares=scraper_entrenador_palmares._ScraperEntrenadorPalmares__contenido_tabla_palmares(contenido)

	assert tabla_palmares is not None

@pytest.mark.parametrize(["entrenador"],
	[("diego-simeone-13",),("hansi-flick-8143",),("thiago-motta-21853",),("fernando-torres-47437",)]
)
def test_scraper_entrenador_palmares_obtener_tablas_titulos(entrenador):

	scraper_entrenador_palmares=ScraperEntrenadorPalmares(entrenador)

	contenido=scraper_entrenador_palmares._Scraper__realizarPeticion()

	tabla_palmares=scraper_entrenador_palmares._ScraperEntrenadorPalmares__contenido_tabla_palmares(contenido)

	tablas_titulos=scraper_entrenador_palmares._ScraperEntrenadorPalmares__obtener_tablas_titulos(tabla_palmares)

	assert tablas_titulos

	for tabla in tablas_titulos:

		assert len(tabla)==4
		assert tabla[2].endswith(".png") or tabla[2].endswith(".jpg")
		assert tabla[2].startswith("https://cdn.resfu.com/img_data/competiciones/") or tabla[2].startswith("https://cdn.resfu.com/media/img/")

@pytest.mark.parametrize(["entrenador"],
	[("diego-simeone-13",),("hansi-flick-8143",),("thiago-motta-21853",),("fernando-torres-47437",)]
)
def test_scraper_entrenador_palmares_obtener_data_limpia(entrenador):

	scraper_entrenador_palmares=ScraperEntrenadorPalmares(entrenador)

	contenido=scraper_entrenador_palmares._Scraper__realizarPeticion()

	tabla_palmares=scraper_entrenador_palmares._ScraperEntrenadorPalmares__contenido_tabla_palmares(contenido)

	data_limpia=scraper_entrenador_palmares._ScraperEntrenadorPalmares__obtenerDataLimpia(tabla_palmares)

	assert isinstance(data_limpia, pd.DataFrame)

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",)]
)
def test_scraper_entrenador_palmares_obtener_palmares_equipo_error(endpoint):

	scraper=ScraperEntrenadorPalmares(endpoint)

	with pytest.raises(EntrenadorPalmaresError):

		scraper.obtenerEntrenadorPalmares()

@pytest.mark.parametrize(["entrenador"],
	[("diego-simeone-13",),("hansi-flick-8143",),("thiago-motta-21853",),("fernando-torres-47437",)]
)
def test_scraper_entrenador_palmares_obtener_palmares_equipo(entrenador):

	scraper=ScraperEntrenadorPalmares(entrenador)

	df_palmares=scraper.obtenerEntrenadorPalmares()

	assert isinstance(df_palmares, pd.DataFrame)