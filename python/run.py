from src.etl_equipos_liga import extraerDataEquiposLiga, limpiarDataEquiposLiga
from src.etl_equipo import extraerDataEquipoDetalle, limpiarDataEquipoDetalle
from src.etl_equipo_estadio import extraerDataEquipoEstadio, limpiarDataEquipoEstadio
from src.extraer_equipo_entrenador import extraerDataEquipoEntrenador

for liga in ["primera", "segunda", "bundesliga", "premier", "ligue_1", "portugal"]:

	data_equipos=extraerDataEquiposLiga(liga)

	data_limpia_equipos=limpiarDataEquiposLiga(data_equipos)

	print(data_limpia_equipos)

for equipo in ["atletico-madrid", "liverpool", "barcelona", "fc-porto", "fulham"]:

	data_equipo=extraerDataEquipoDetalle(equipo)

	data_limpia_equipo=limpiarDataEquipoDetalle(data_equipo)

	print(data_limpia_equipo)

	data_estadio=extraerDataEquipoEstadio(equipo)

	data_limpia_estadio=limpiarDataEquipoEstadio(data_estadio)

	print(data_limpia_estadio)

	data_entrenador=extraerDataEquipoEntrenador(equipo)

	print(data_entrenador)