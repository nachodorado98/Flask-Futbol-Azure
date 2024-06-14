import pytest
import pandas as pd

from src.etl_partidos import extraerDataPartidosEquipo
from src.scrapers.excepciones_scrapers import PartidosEquipoError

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(-1, -1), (0, 0), (0, 2019), (1, 2024), ("equipo", 2023)]
)
def test_extraer_data_partidos_equipo_error_endpoint(equipo_id, temporada):

	with pytest.raises(PartidosEquipoError):

		extraerDataPartidosEquipo(equipo_id, temporada)

@pytest.mark.parametrize(["equipo_id", "temporada"],
	[(369, 2021),(369, 2014),(4, 2020),(449, 2017),(429, 1990),(369, 2000),(369, 1940),(449, 1971)]
)
def test_extraer_data_partidos_equipo(equipo_id, temporada):

	data=extraerDataPartidosEquipo(equipo_id, temporada)

	assert isinstance(data, pd.DataFrame)
	assert not data.empty