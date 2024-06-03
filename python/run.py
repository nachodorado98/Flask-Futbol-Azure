from src.extraer_equipos_liga import extraerDataEquiposLiga
from src.extraer_equipo import extraerDataEquipoDetalle
from src.extraer_equipo_estadio import extraerDataEquipoEstadio
from src.extraer_equipo_entrenador import extraerDataEquipoEntrenador

for liga in ["primera", "segunda", "bundesliga", "premier", "ligue_1", "portugal"]:

	data_equipos=extraerDataEquiposLiga(liga)

	print(data_equipos)

for equipo in ["atletico-madrid", "liverpool", "barcelona", "fc-porto", "fulham"]:

	data_equipo=extraerDataEquipoDetalle(equipo)

	print(data_equipo)

	data_estadio=extraerDataEquipoEstadio(equipo)

	print(data_estadio)

	data_entrenador=extraerDataEquipoEntrenador(equipo)

	print(data_entrenador)