import pytest
from bs4 import BeautifulSoup as bs4
import pandas as pd

from src.scrapers.scraper_partido_estadio import ScraperPartidoEstadio
from src.scrapers.excepciones_scrapers import PaginaError, PartidoEstadioError

def test_crear_objeto_scraper_partido_estadio():

	scraper=ScraperPartidoEstadio("equipo1", "equipo2", "partido_id")

def test_scraper_partido_estadio_realizar_peticion_error_redirecciona(scraper):

	scraper=ScraperPartidoEstadio("equipo1", "equipo2", "partido_id")

	with pytest.raises(PaginaError):

		scraper._Scraper__realizarPeticion()

def test_scraper_partido_estadio_realizar_peticion(scraper_partido_estadio):

	contenido=scraper_partido_estadio._Scraper__realizarPeticion()

	assert isinstance(contenido, bs4)

def test_scraper_partido_estadio_obtener_tabla_estadio_no_existe():

	scraper_partido_estadio=ScraperPartidoEstadio("ue-vic", "atletico-madrid", "2025208658")

	contenido=scraper_partido_estadio._Scraper__realizarPeticion()

	# with pytest.raises(PartidoEstadioError): # La web ha introducido la etiqueta del estadio del partido pero realmente no hay estadio

	# 	scraper_partido_estadio._ScraperPartidoEstadio__contenido_tabla_estadio(contenido)

def test_scraper_partido_estadio_obtener_tabla_estadio(scraper_partido_estadio):

	contenido=scraper_partido_estadio._Scraper__realizarPeticion()

	tabla_estadio=scraper_partido_estadio._ScraperPartidoEstadio__contenido_tabla_estadio(contenido)

	assert tabla_estadio is not None

def test_scraper_partido_estadio_obtener_imagen_estadio(scraper_partido_estadio):

	contenido=scraper_partido_estadio._Scraper__realizarPeticion()

	tabla_estadio=scraper_partido_estadio._ScraperPartidoEstadio__contenido_tabla_estadio(contenido)

	imagen_estadio=scraper_partido_estadio._ScraperPartidoEstadio__imagen_estadio(tabla_estadio)

	assert imagen_estadio.endswith(".png") or imagen_estadio.endswith(".jpg")
	assert "estadio_nofoto" not in imagen_estadio
	assert imagen_estadio.startswith("https://cdn.resfu.com/img_data/estadios/original_new")

def test_scraper_partido_estadio_obtener_informacion_datos_estadio(scraper_partido_estadio):

	contenido=scraper_partido_estadio._Scraper__realizarPeticion()

	tabla_estadio=scraper_partido_estadio._ScraperPartidoEstadio__contenido_tabla_estadio(contenido)

	tabla_info_datos=scraper_partido_estadio._ScraperPartidoEstadio__informacion_datos_estadio(tabla_estadio)

	assert tabla_info_datos is not None

def test_scraper_partido_estadio_obtener_tabla_nombre_ubicacion_datos_correctos(scraper_partido_estadio):

	contenido=scraper_partido_estadio._Scraper__realizarPeticion()

	tabla_estadio=scraper_partido_estadio._ScraperPartidoEstadio__contenido_tabla_estadio(contenido)

	tabla_info_datos=scraper_partido_estadio._ScraperPartidoEstadio__informacion_datos_estadio(tabla_estadio)

	nombre_ciudad_direccion=scraper_partido_estadio._ScraperPartidoEstadio__tabla_nombre_ubicacion(tabla_info_datos)

	assert len(nombre_ciudad_direccion)==3
	assert nombre_ciudad_direccion.count("")==1

def test_scraper_partido_estadio_obtener_informacion_nombre_ubicacion_datos_correctos(scraper_partido_estadio):

	contenido=scraper_partido_estadio._Scraper__realizarPeticion()

	tabla_estadio=scraper_partido_estadio._ScraperPartidoEstadio__contenido_tabla_estadio(contenido)

	nombre_ciudad_direccion=scraper_partido_estadio._ScraperPartidoEstadio__informacion_nombre_ubicacion(tabla_estadio)

	assert len(nombre_ciudad_direccion)==3

def test_scraper_partido_estadio_obtener_tabla_datos_tecnicos_datos_correctos(scraper_partido_estadio):

	contenido=scraper_partido_estadio._Scraper__realizarPeticion()

	tabla_estadio=scraper_partido_estadio._ScraperPartidoEstadio__contenido_tabla_estadio(contenido)

	tabla_info_datos=scraper_partido_estadio._ScraperPartidoEstadio__informacion_datos_estadio(tabla_estadio)

	estadio=scraper_partido_estadio._ScraperPartidoEstadio__tabla_datos_tecnicos(tabla_info_datos)

	assert len(estadio)==6
	#assert "" not in estadio # Antes no tenian datos faltantes pero ahora parece que los han eliminado en la web (ciudad, cesped, telefono)

def test_scraper_partido_estadio_obtener_informacion_datos_tecnicos_datos_correctos(scraper_partido_estadio):

	contenido=scraper_partido_estadio._Scraper__realizarPeticion()

	tabla_estadio=scraper_partido_estadio._ScraperPartidoEstadio__contenido_tabla_estadio(contenido)

	estadio=scraper_partido_estadio._ScraperPartidoEstadio__informacion_datos_tecnicos(tabla_estadio)

	assert len(estadio)==6
	#assert "" not in estadio # Antes no tenian datos faltantes pero ahora parece que los han eliminado en la web (ciudad, cesped, telefono)

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("valladolid", "atletico-madrid", "20256422"),
		("sparta-praha", "atletico-madrid", "2025162171"),
		("atletico-madrid", "sevilla", "20256430"),
		("internazionale", "atletico-madrid", "2024645008"),
		("seleccion-holanda", "seleccion-espanola", "201094287")
	]
)
def test_scraper_partido_estadio_obtener_data_limpia(local, visitante, partido_id):

	scraper_partido_estadio=ScraperPartidoEstadio(local, visitante, partido_id)

	contenido=scraper_partido_estadio._Scraper__realizarPeticion()

	tabla_estadio=scraper_partido_estadio._ScraperPartidoEstadio__contenido_tabla_estadio(contenido)

	data_limpia=scraper_partido_estadio._ScraperPartidoEstadio__obtenerDataLimpia(tabla_estadio)

	assert isinstance(data_limpia, pd.DataFrame)

def test_scraper_partido_estadio_obtener_partido_estadio_error():

	scraper=ScraperPartidoEstadio("equipo1", "equipo2", "partido_id")

	with pytest.raises(PartidoEstadioError):

		scraper.obtenerPartidoEstadio()

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("valladolid", "atletico-madrid", "20256422"),
		("sparta-praha", "atletico-madrid", "2025162171"),
		("atletico-madrid", "sevilla", "20256430"),
		("internazionale", "atletico-madrid", "2024645008"),
		("seleccion-holanda", "seleccion-espanola", "201094287")
	]
)
def test_scraper_partido_estadio_obtener_partido_estadio(local, visitante, partido_id):

	scraper=ScraperPartidoEstadio(local, visitante, partido_id)

	df_estadio=scraper.obtenerPartidoEstadio()

	assert isinstance(df_estadio, pd.DataFrame)