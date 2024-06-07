from typing import List
import time

from src.etl_equipos_liga import extraerDataEquiposLiga, limpiarDataEquiposLiga, cargarDataEquiposLiga
from src.etl_equipo import extraerDataEquipoDetalle, limpiarDataEquipoDetalle
from src.etl_equipo_estadio import extraerDataEquipoEstadio, limpiarDataEquipoEstadio
from src.etl_equipo_entrenador import extraerDataEquipoEntrenador, limpiarDataEquipoEntrenador
from src.etl_equipo_escudo import extraerDataEquipoEscudo, limpiarDataEquipoEscudo

def pipeline(ligas:List[str], equipos:List[str])->None:

	try:

		for liga in ligas:

			data_equipos=extraerDataEquiposLiga(liga)

			data_limpia_equipos=limpiarDataEquiposLiga(data_equipos)

			cargarDataEquiposLiga(data_limpia_equipos)

			print(data_limpia_equipos)

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

			data_limpia_escudo=limpiarDataEquipoEscudo(data_escudo)

			print(data_limpia_escudo)

		print("Pipeline finalizado")

	except Exception as e:

		print("Reconectando con la BBDD Postgres en 5 segundos...")

		time.sleep(5)

		pipeline(ligas, equipos)

ligas=["primera", "segunda", "bundesliga", "premier", "ligue_1", "portugal"]

equipos=["atletico-madrid", "liverpool", "barcelona", "fc-porto", "fulham",
		"paris-saint-germain-fc", "borussia-dortmund", "rayo-vallecano", "ca-boca-juniors"]

pipeline(ligas, equipos)