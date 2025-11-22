import pytest
from bs4 import BeautifulSoup as bs4
import pandas as pd

from src.scrapers.scraper_partido_alineaciones import ScraperPartidoAlineaciones
from src.scrapers.excepciones_scrapers import PaginaError, PartidoAlineacionesAlineacionError, PartidoAlineacionesSuplentesError, PartidoAlineacionesError

def test_crear_objeto_scraper_partido_alineaciones():

	scraper=ScraperPartidoAlineaciones("equipo1", "equipo2", "partido_id")

def test_scraper_partido_alineaciones_realizar_peticion_error_redirecciona(scraper):

	scraper=ScraperPartidoAlineaciones("equipo1", "equipo2", "partido_id")

	with pytest.raises(PaginaError):

		scraper._Scraper__realizarPeticion()

def test_scraper_partido_alineaciones_realizar_peticion(scraper_partido_alineaciones):

	contenido=scraper_partido_alineaciones._Scraper__realizarPeticion()

	assert isinstance(contenido, bs4)

def test_scraper_partido_alineaciones_obtener_tabla_alineaciones_no_existe():

	scraper_partido_alineaciones=ScraperPartidoAlineaciones("atletico-madrid", "liverpool", "198923660")

	contenido=scraper_partido_alineaciones._Scraper__realizarPeticion()

	with pytest.raises(PartidoAlineacionesAlineacionError):

		scraper_partido_alineaciones._ScraperPartidoAlineaciones__contenido_tabla_alineacion(contenido)

def test_scraper_partido_alineaciones_obtener_tabla_alineaciones(scraper_partido_alineaciones):

	contenido=scraper_partido_alineaciones._Scraper__realizarPeticion()

	tabla_alineacion=scraper_partido_alineaciones._ScraperPartidoAlineaciones__contenido_tabla_alineacion(contenido)

	assert tabla_alineacion is not None

def test_scraper_partido_alineaciones_obtener_tabla_suplentes_no_existe():

	scraper_partido_alineaciones=ScraperPartidoAlineaciones("atletico-madrid", "liverpool", "198923660")

	contenido=scraper_partido_alineaciones._Scraper__realizarPeticion()

	with pytest.raises(PartidoAlineacionesSuplentesError):

		scraper_partido_alineaciones._ScraperPartidoAlineaciones__contenido_tabla_suplentes(contenido)

def test_scraper_partido_alineaciones_obtener_tabla_suplentes(scraper_partido_alineaciones):

	contenido=scraper_partido_alineaciones._Scraper__realizarPeticion()

	tabla_suplentes=scraper_partido_alineaciones._ScraperPartidoAlineaciones__contenido_tabla_suplentes(contenido)

	assert tabla_suplentes is not None

def test_scraper_partido_alineaciones_obtener_entrenadores_faltante():

	scraper_partido_alineaciones=ScraperPartidoAlineaciones("cd-arcangel", "atletico-madrid", "201210617")

	contenido=scraper_partido_alineaciones._Scraper__realizarPeticion()

	tabla_alineacion=scraper_partido_alineaciones._ScraperPartidoAlineaciones__contenido_tabla_alineacion(contenido)

	entrenadores=scraper_partido_alineaciones._ScraperPartidoAlineaciones__obtener_entrenadores(tabla_alineacion)

	assert len(entrenadores)==2
	assert None in entrenadores

def test_scraper_partido_alineaciones_obtener_entrenadores(scraper_partido_alineaciones):

	contenido=scraper_partido_alineaciones._Scraper__realizarPeticion()

	tabla_alineacion=scraper_partido_alineaciones._ScraperPartidoAlineaciones__contenido_tabla_alineacion(contenido)

	entrenadores=scraper_partido_alineaciones._ScraperPartidoAlineaciones__obtener_entrenadores(tabla_alineacion)

	assert len(entrenadores)==2

def test_scraper_partido_alineaciones_obtener_alineaciones_alineacion_local():

	scraper_partido_alineaciones=ScraperPartidoAlineaciones("atletico-madrid", "almeria", "2021113990")

	contenido=scraper_partido_alineaciones._Scraper__realizarPeticion()

	tabla_alineacion=scraper_partido_alineaciones._ScraperPartidoAlineaciones__contenido_tabla_alineacion(contenido)

	alineaciones=scraper_partido_alineaciones._ScraperPartidoAlineaciones__obtener_alineaciones(tabla_alineacion)

	assert len(alineaciones)==2
	assert len(alineaciones[0])==11
	assert len(alineaciones[1])==0

	for alineacion in alineaciones[0]+alineaciones[1]:

		assert alineacion[-3]=="T"
		assert alineacion[-2]=="L"
		assert alineacion[-1]>0 and alineacion[-1]<12

def test_scraper_partido_alineaciones_obtener_alineaciones_alineacion_visitante():

	scraper_partido_alineaciones=ScraperPartidoAlineaciones("gimnastica-segoviana", "atletico-madrid", "201210634")

	contenido=scraper_partido_alineaciones._Scraper__realizarPeticion()

	tabla_alineacion=scraper_partido_alineaciones._ScraperPartidoAlineaciones__contenido_tabla_alineacion(contenido)

	alineaciones=scraper_partido_alineaciones._ScraperPartidoAlineaciones__obtener_alineaciones(tabla_alineacion)

	assert len(alineaciones)==2
	assert len(alineaciones[0])==0
	assert len(alineaciones[1])==11

	for alineacion in alineaciones[0]+alineaciones[1]:

		assert alineacion[-3]=="T"
		assert alineacion[-2]=="V"
		assert alineacion[-1]>0 and alineacion[-1]<12

def test_scraper_partido_alineaciones_obtener_alineaciones(scraper_partido_alineaciones):

	contenido=scraper_partido_alineaciones._Scraper__realizarPeticion()

	tabla_alineacion=scraper_partido_alineaciones._ScraperPartidoAlineaciones__contenido_tabla_alineacion(contenido)

	alineaciones=scraper_partido_alineaciones._ScraperPartidoAlineaciones__obtener_alineaciones(tabla_alineacion)

	assert len(alineaciones)==2
	assert len(alineaciones[0])==11
	assert len(alineaciones[1])==11

	for alineacion in alineaciones[0]+alineaciones[1]:

		assert alineacion[-3]=="T"
		assert alineacion[-2] in ("L", "V")
		assert alineacion[-1]>0 and alineacion[-1]<12

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("atletico-madrid", "almeria", "2021113990"),
		("cd-arcangel", "atletico-madrid", "201210617"),
		("valladolid", "atletico-madrid", "20256422"),
		("sparta-praha", "atletico-madrid", "2025162171"),
		("atletico-madrid", "sevilla", "20256430"),
		("internazionale", "atletico-madrid", "2024645008")
	]
)
def test_scraper_partido_alineaciones_obtener_tacticas(local, visitante, partido_id):

	scraper_partido_alineaciones=ScraperPartidoAlineaciones(local, visitante, partido_id)

	contenido=scraper_partido_alineaciones._Scraper__realizarPeticion()

	tabla_alineacion=scraper_partido_alineaciones._ScraperPartidoAlineaciones__contenido_tabla_alineacion(contenido)

	tacticas=scraper_partido_alineaciones._ScraperPartidoAlineaciones__obtener_tacticas(tabla_alineacion)

	assert len(tacticas)==2

def test_scraper_partido_alineaciones_informacion_entrenador_faltante():

	scraper_partido_alineaciones=ScraperPartidoAlineaciones("cd-arcangel", "atletico-madrid", "201210617")

	contenido=scraper_partido_alineaciones._Scraper__realizarPeticion()

	tabla_alineacion=scraper_partido_alineaciones._ScraperPartidoAlineaciones__contenido_tabla_alineacion(contenido)

	info_entrenador=scraper_partido_alineaciones._ScraperPartidoAlineaciones__informacion_entrenador(tabla_alineacion)

	assert len(info_entrenador)==2
	assert None in info_entrenador[0] or None in info_entrenador[1]

def test_scraper_partido_alineaciones_informacion_entrenador(scraper_partido_alineaciones):

	contenido=scraper_partido_alineaciones._Scraper__realizarPeticion()

	tabla_alineacion=scraper_partido_alineaciones._ScraperPartidoAlineaciones__contenido_tabla_alineacion(contenido)

	info_entrenador=scraper_partido_alineaciones._ScraperPartidoAlineaciones__informacion_entrenador(tabla_alineacion)

	assert len(info_entrenador)==2

def test_scraper_partido_alineaciones_obtener_suplentes(scraper_partido_alineaciones):

	contenido=scraper_partido_alineaciones._Scraper__realizarPeticion()

	tabla_suplentes=scraper_partido_alineaciones._ScraperPartidoAlineaciones__contenido_tabla_suplentes(contenido)

	suplentes=scraper_partido_alineaciones._ScraperPartidoAlineaciones__obtener_suplentes(tabla_suplentes)

	assert len(suplentes)==2
	assert len(suplentes[0])>0
	assert len(suplentes[1])>0

	for suplente in suplentes[0]+suplentes[1]:

		assert suplente[-3]=="S"
		assert suplente[-2] in ("L", "V")
		assert suplente[-1]==-1

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("atletico-madrid", "almeria", "2021113990")
	]
)
def test_scraper_partido_alineaciones_obtener_data_limpia_alineacion_local(local, visitante, partido_id):

	scraper_partido_alineaciones=ScraperPartidoAlineaciones(local, visitante, partido_id)

	contenido=scraper_partido_alineaciones._Scraper__realizarPeticion()

	tabla_alineacion=scraper_partido_alineaciones._ScraperPartidoAlineaciones__contenido_tabla_alineacion(contenido)

	data_limpia=scraper_partido_alineaciones._ScraperPartidoAlineaciones__obtenerDataLimpia(tabla_alineacion, None)

	assert isinstance(data_limpia, pd.DataFrame)
	assert not data_limpia[(data_limpia["Alineacion"]=="T") & (data_limpia["Tipo"]=="L")].empty
	assert data_limpia[(data_limpia["Alineacion"]=="T") & (data_limpia["Tipo"]=="V")].empty
	assert not data_limpia[(data_limpia["Posicion"]>0) & (data_limpia["Posicion"]<12)].empty

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("gimnastica-segoviana", "atletico-madrid", "201210634")
	]
)
def test_scraper_partido_alineaciones_obtener_data_limpia_alineacion_visitante(local, visitante, partido_id):

	scraper_partido_alineaciones=ScraperPartidoAlineaciones(local, visitante, partido_id)

	contenido=scraper_partido_alineaciones._Scraper__realizarPeticion()

	tabla_alineacion=scraper_partido_alineaciones._ScraperPartidoAlineaciones__contenido_tabla_alineacion(contenido)

	data_limpia=scraper_partido_alineaciones._ScraperPartidoAlineaciones__obtenerDataLimpia(tabla_alineacion, None)

	assert isinstance(data_limpia, pd.DataFrame)
	assert data_limpia[(data_limpia["Alineacion"]=="T") & (data_limpia["Tipo"]=="L")].empty
	assert not data_limpia[(data_limpia["Alineacion"]=="T") & (data_limpia["Tipo"]=="V")].empty
	assert not data_limpia[(data_limpia["Posicion"]>0) & (data_limpia["Posicion"]<12)].empty

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("atletico-madrid", "almeria", "2021113990"),
		("gimnastica-segoviana", "atletico-madrid", "201210634"),
		("cd-arcangel", "atletico-madrid", "201210617")
	]
)
def test_scraper_partido_alineaciones_obtener_data_limpia_sin_suplentes(local, visitante, partido_id):

	scraper_partido_alineaciones=ScraperPartidoAlineaciones(local, visitante, partido_id)

	contenido=scraper_partido_alineaciones._Scraper__realizarPeticion()

	tabla_alineacion=scraper_partido_alineaciones._ScraperPartidoAlineaciones__contenido_tabla_alineacion(contenido)

	data_limpia=scraper_partido_alineaciones._ScraperPartidoAlineaciones__obtenerDataLimpia(tabla_alineacion, None)

	assert isinstance(data_limpia, pd.DataFrame)
	assert data_limpia[(data_limpia["Alineacion"]=="S") & (data_limpia["Tipo"]=="L")].empty
	assert data_limpia[(data_limpia["Alineacion"]=="S") & (data_limpia["Tipo"]=="V")].empty
	assert data_limpia[data_limpia["Posicion"]==-1].empty

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("valladolid", "atletico-madrid", "20256422"),
		("sparta-praha", "atletico-madrid", "2025162171"),
		("atletico-madrid", "sevilla", "20256430"),
		("internazionale", "atletico-madrid", "2024645008"),
	]
)
def test_scraper_partido_alineaciones_obtener_data_limpia_completo(local, visitante, partido_id):

	scraper_partido_alineaciones=ScraperPartidoAlineaciones(local, visitante, partido_id)

	contenido=scraper_partido_alineaciones._Scraper__realizarPeticion()

	tabla_alineacion=scraper_partido_alineaciones._ScraperPartidoAlineaciones__contenido_tabla_alineacion(contenido)

	tabla_suplentes=scraper_partido_alineaciones._ScraperPartidoAlineaciones__contenido_tabla_suplentes(contenido)

	data_limpia=scraper_partido_alineaciones._ScraperPartidoAlineaciones__obtenerDataLimpia(tabla_alineacion, tabla_suplentes)

	assert isinstance(data_limpia, pd.DataFrame)
	assert not data_limpia[(data_limpia["Alineacion"]=="T") & (data_limpia["Tipo"]=="L")].empty
	assert not data_limpia[(data_limpia["Alineacion"]=="T") & (data_limpia["Tipo"]=="V")].empty
	assert not data_limpia[(data_limpia["Alineacion"]=="S") & (data_limpia["Tipo"]=="L")].empty
	assert not data_limpia[(data_limpia["Alineacion"]=="S") & (data_limpia["Tipo"]=="V")].empty
	assert not data_limpia[data_limpia["Posicion"]==-1].empty
	assert not data_limpia[(data_limpia["Posicion"]>0) & (data_limpia["Posicion"]<12)].empty

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("equipo1", "equipo2", "partido_id"),
		("atletico-madrid", "liverpool", "198923660")
	]
)
def test_scraper_partido_alineaciones_obtener_partido_alineaciones_error(local, visitante, partido_id):

	scraper=ScraperPartidoAlineaciones(local, visitante, partido_id)

	with pytest.raises(PartidoAlineacionesError):

		scraper.obtenerPartidoAlineaciones()

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("atletico-madrid", "almeria", "2021113990")
	]
)
def test_scraper_partido_alineaciones_obtener_partido_alineaciones_alineacion_local(local, visitante, partido_id):

	scraper=ScraperPartidoAlineaciones(local, visitante, partido_id)

	df_partido_alineaciones=scraper.obtenerPartidoAlineaciones()

	assert isinstance(df_partido_alineaciones, pd.DataFrame)
	assert not df_partido_alineaciones[(df_partido_alineaciones["Alineacion"]=="T") & (df_partido_alineaciones["Tipo"]=="L")].empty
	assert df_partido_alineaciones[(df_partido_alineaciones["Alineacion"]=="T") & (df_partido_alineaciones["Tipo"]=="V")].empty
	assert not df_partido_alineaciones[(df_partido_alineaciones["Posicion"]>0) & (df_partido_alineaciones["Posicion"]<12)].empty

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("gimnastica-segoviana", "atletico-madrid", "201210634")
	]
)
def test_scraper_partido_alineaciones_obtener_partido_alineaciones_alineacion_visitante(local, visitante, partido_id):

	scraper=ScraperPartidoAlineaciones(local, visitante, partido_id)

	df_partido_alineaciones=scraper.obtenerPartidoAlineaciones()

	assert isinstance(df_partido_alineaciones, pd.DataFrame)
	assert df_partido_alineaciones[(df_partido_alineaciones["Alineacion"]=="T") & (df_partido_alineaciones["Tipo"]=="L")].empty
	assert not df_partido_alineaciones[(df_partido_alineaciones["Alineacion"]=="T") & (df_partido_alineaciones["Tipo"]=="V")].empty
	assert not df_partido_alineaciones[(df_partido_alineaciones["Posicion"]>0) & (df_partido_alineaciones["Posicion"]<12)].empty

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("atletico-madrid", "almeria", "2021113990"),
		("gimnastica-segoviana", "atletico-madrid", "201210634"),
		("cd-arcangel", "atletico-madrid", "201210617")
	]
)
def test_scraper_partido_alineaciones_obtener_partido_alineaciones_sin_suplentes(local, visitante, partido_id):

	scraper=ScraperPartidoAlineaciones(local, visitante, partido_id)

	df_partido_alineaciones=scraper.obtenerPartidoAlineaciones()

	assert isinstance(df_partido_alineaciones, pd.DataFrame)
	assert df_partido_alineaciones[(df_partido_alineaciones["Alineacion"]=="S") & (df_partido_alineaciones["Tipo"]=="L")].empty
	assert df_partido_alineaciones[(df_partido_alineaciones["Alineacion"]=="S") & (df_partido_alineaciones["Tipo"]=="V")].empty
	assert df_partido_alineaciones[df_partido_alineaciones["Posicion"]==-1].empty

@pytest.mark.parametrize(["local", "visitante", "partido_id"],
	[
		("valladolid", "atletico-madrid", "20256422"),
		("sparta-praha", "atletico-madrid", "2025162171"),
		("atletico-madrid", "sevilla", "20256430"),
		("internazionale", "atletico-madrid", "2024645008")
	]
)
def test_scraper_partido_alineaciones_obtener_partido_alineaciones_completo(local, visitante, partido_id):

	scraper=ScraperPartidoAlineaciones(local, visitante, partido_id)

	df_partido_alineaciones=scraper.obtenerPartidoAlineaciones()

	assert isinstance(df_partido_alineaciones, pd.DataFrame)
	assert not df_partido_alineaciones[(df_partido_alineaciones["Alineacion"]=="T") & (df_partido_alineaciones["Tipo"]=="L")].empty
	assert not df_partido_alineaciones[(df_partido_alineaciones["Alineacion"]=="T") & (df_partido_alineaciones["Tipo"]=="V")].empty
	assert not df_partido_alineaciones[(df_partido_alineaciones["Alineacion"]=="S") & (df_partido_alineaciones["Tipo"]=="L")].empty
	assert not df_partido_alineaciones[(df_partido_alineaciones["Alineacion"]=="S") & (df_partido_alineaciones["Tipo"]=="V")].empty
	assert not df_partido_alineaciones[df_partido_alineaciones["Posicion"]==-1].empty
	assert not df_partido_alineaciones[(df_partido_alineaciones["Posicion"]>0) & (df_partido_alineaciones["Posicion"]<12)].empty