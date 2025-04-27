import pytest
from bs4 import BeautifulSoup as bs4
import pandas as pd

from src.scrapers.scraper_entrenador import ScraperEntrenador
from src.scrapers.excepciones_scrapers import PaginaError, EntrenadorError

def test_crear_objeto_scraper_entrenador():

	scraper=ScraperEntrenador("entrenador")

# def test_scraper_entrenador_realizar_peticion_error_redirecciona(scraper):

# 	scraper=ScraperEntrenador("redireccion_entrenador")

# 	with pytest.raises(PaginaError):

# 		scraper._Scraper__realizarPeticion()

def test_scraper_entrenador_realizar_peticion(scraper_entrenador):

	contenido=scraper_entrenador._Scraper__realizarPeticion()

	assert isinstance(contenido, bs4)

def test_scraper_entrenador_obtener_cabecera(scraper_entrenador):

	contenido=scraper_entrenador._Scraper__realizarPeticion()

	cabecera=scraper_entrenador._ScraperEntrenador__contenido_cabecera(contenido)

	assert cabecera is not None

@pytest.mark.parametrize(["entrenador"],
	[("diego-simeone-13",),("hansi-flick-8143",),("thiago-motta-21853",),("fernando-torres-47437",)]
)
def test_scraper_entrenador_obtener_informacion_nombre(entrenador):

	scraper_entrenador=ScraperEntrenador(entrenador)

	contenido=scraper_entrenador._Scraper__realizarPeticion()

	cabecera=scraper_entrenador._ScraperEntrenador__contenido_cabecera(contenido)

	nombre=scraper_entrenador._ScraperEntrenador__informacion_nombre(cabecera)

	assert nombre is not ""

@pytest.mark.parametrize(["entrenador"],
	[("luis-aragones-1918",),("radomir-antic-2601",)]
)
def test_scraper_entrenador_obtener_informacion_general_sin_equipo(entrenador):

	scraper_entrenador=ScraperEntrenador(entrenador)

	contenido=scraper_entrenador._Scraper__realizarPeticion()

	cabecera=scraper_entrenador._ScraperEntrenador__contenido_cabecera(contenido)

	datos=scraper_entrenador._ScraperEntrenador__informacion_general(contenido)

	assert len(datos)==4

	assert datos[0]==""

	assert datos[1].endswith(".png") or datos[1].endswith(".jpg")
	assert datos[1].startswith("https://cdn.resfu.com/media/img/flags")

	assert datos[2].endswith(".png") or datos[2].endswith(".jpg")
	assert datos[2].startswith("https://cdn.resfu.com/img_data/people/original")

@pytest.mark.parametrize(["entrenador"],
	[("diego-simeone-13",),("hansi-flick-8143",),("pep-guardiola-114",),("fernando-torres-47437",)]
)
def test_scraper_entrenador_obtener_informacion_general_con_equipo(entrenador):

	scraper_entrenador=ScraperEntrenador(entrenador)

	contenido=scraper_entrenador._Scraper__realizarPeticion()

	cabecera=scraper_entrenador._ScraperEntrenador__contenido_cabecera(contenido)

	datos=scraper_entrenador._ScraperEntrenador__informacion_general(contenido)

	assert len(datos)==4

	assert datos[0].startswith("https://es.besoccer.com/equipo/")

	assert datos[1].endswith(".png") or datos[1].endswith(".jpg")
	assert datos[1].startswith("https://cdn.resfu.com/media/img/flags")

	assert datos[2].endswith(".png") or datos[2].endswith(".jpg")
	assert datos[2].startswith("https://cdn.resfu.com/img_data/people/original")

@pytest.mark.parametrize(["entrenador"],
	[("diego-simeone-13",),("hansi-flick-8143",),("thiago-motta-21853",),
	("fernando-torres-47437",),("luis-aragones-1918",),("radomir-antic-2601",)]
)
def test_scraper_entrenador_obtener_data_limpia(entrenador):

	scraper_entrenador=ScraperEntrenador(entrenador)

	contenido=scraper_entrenador._Scraper__realizarPeticion()

	cabecera=scraper_entrenador._ScraperEntrenador__contenido_cabecera(contenido)

	data_limpia=scraper_entrenador._ScraperEntrenador__obtenerDataLimpia(cabecera)

	assert isinstance(data_limpia, pd.DataFrame)

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",)]
)
def test_scraper_entrenador_obtener_entrenador_error(endpoint):

	scraper=ScraperEntrenador(endpoint)

	with pytest.raises(EntrenadorError):

		scraper.obtenerEntrenador()

@pytest.mark.parametrize(["entrenador"],
	[("diego-simeone-13",),("hansi-flick-8143",),("thiago-motta-21853",),
	("fernando-torres-47437",),("luis-aragones-1918",),("radomir-antic-2601",)]
)
def test_scraper_entrenador_obtener_entrenador(entrenador):

	scraper=ScraperEntrenador(entrenador)

	df_entrenador=scraper.obtenerEntrenador()

	assert isinstance(df_entrenador, pd.DataFrame)