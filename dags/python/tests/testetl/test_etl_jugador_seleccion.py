import pytest
import pandas as pd

from src.etl_jugador_seleccion import extraerDataJugadorSeleccion
from src.scrapers.excepciones_scrapers import JugadorSeleccionError

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",)]
)
def test_extraer_data_jugador_seleccion_error_endpoint(endpoint):

	with pytest.raises(JugadorSeleccionError):

		extraerDataJugadorSeleccion(endpoint)

@pytest.mark.parametrize(["jugador"],
	[("j-dorado-3363152",),("m-garcia-348428",),("gonzalez-375633",),
	("carlinos-189054",),("sergio-cordero-parral",)]
)
def test_extraer_data_jugador_seleccion_no_tiene(jugador):

	with pytest.raises(JugadorSeleccionError):

		extraerDataJugadorSeleccion(jugador)

@pytest.mark.parametrize(["jugador"],
	[("j-alvarez-772644",),("f-torres-29366",),("d-villa-23386",),("c-gallagher-367792",),
	("sorloth-232186",),("c-martin-776234",),("a-griezmann-32465",)]
)
def test_extraer_data_jugador_seleccion(jugador):

	data=extraerDataJugadorSeleccion(jugador)

	assert isinstance(data, pd.DataFrame)
	assert not data.empty
	assert len(data.columns)==7