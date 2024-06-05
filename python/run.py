from src.etl_equipos_liga import extraerDataEquiposLiga, limpiarDataEquiposLiga
from src.etl_equipo import extraerDataEquipoDetalle, limpiarDataEquipoDetalle
from src.etl_equipo_estadio import extraerDataEquipoEstadio, limpiarDataEquipoEstadio
from src.etl_equipo_entrenador import extraerDataEquipoEntrenador, limpiarDataEquipoEntrenador
from src.etl_equipo_escudo import extraerDataEquipoEscudo

ligas=["primera", "segunda",
		"bundesliga", "premier",
		"ligue_1", "portugal"]

for liga in ligas:

	data_equipos=extraerDataEquiposLiga(liga)

	data_limpia_equipos=limpiarDataEquiposLiga(data_equipos)

	print(data_limpia_equipos)


equipos=["atletico-madrid", "liverpool", "barcelona",
		"fc-porto", "fulham", "paris-saint-germain-fc",
		"borussia-dortmund", "rayo-vallecano", "ca-boca-juniors"]

for equipo in equipos:

	data_equipo=extraerDataEquipoDetalle(equipo)

	data_limpia_equipo=limpiarDataEquipoDetalle(data_equipo)

	print(data_limpia_equipo)

	data_estadio=extraerDataEquipoEstadio(equipo)

	data_limpia_estadio=limpiarDataEquipoEstadio(data_estadio)

	print(data_limpia_estadio)

	data_entrenador=extraerDataEquipoEntrenador(equipo)

	data_limpia_entrenador=limpiarDataEquipoEntrenador(data_entrenador)

	print(data_limpia_entrenador)

	data_escudo=extraerDataEquipoEscudo(equipo)

	print(data_escudo)