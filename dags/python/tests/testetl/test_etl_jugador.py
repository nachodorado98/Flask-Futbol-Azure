import pytest
import pandas as pd

from src.etl_jugador import extraerDataJugador
from src.scrapers.excepciones_scrapers import JugadorError

@pytest.mark.parametrize(["endpoint"],
	[("url",),("endpoint",),("en/players",),("bundeslig",),("primera-division",)]
)
def test_extraer_data_jugador_error_endpoint(endpoint):

	with pytest.raises(JugadorError):

		extraerDataJugador(endpoint)

@pytest.mark.parametrize(["jugador"],
	[("j-alvarez-772644",),("f-torres-29366",),("d-villa-23386",),("c-gallagher-367792",),
	("sorloth-232186",),("c-martin-776234",),("a-griezmann-32465",)]
)
def test_extraer_data_jugador(jugador):

	data=extraerDataJugador(jugador)

	assert isinstance(data, pd.DataFrame)
	assert not data.empty
	assert len(data)==1