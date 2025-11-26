from .etl_equipos_liga import extraerDataEquiposLiga, limpiarDataEquiposLiga, cargarDataEquiposLiga
from .etl_equipo import extraerDataEquipoDetalle, limpiarDataEquipoDetalle, cargarDataEquipoDetalle
from .etl_equipo_escudo import extraerDataEquipoEscudo, limpiarDataEquipoEscudo, cargarDataEquipoEscudo
from .etl_equipo_entrenador import extraerDataEquipoEntrenador, limpiarDataEquipoEntrenador, cargarDataEquipoEntrenador
from .etl_equipo_estadio import extraerDataEquipoEstadio, limpiarDataEquipoEstadio, cargarDataEquipoEstadio
from .etl_equipo_palmares import extraerDataEquipoPalmares, limpiarDataEquipoPalmares, cargarDataEquipoPalmares
from .etl_partidos import extraerDataPartidosEquipo, limpiarDataPartidosEquipo, cargarDataPartidosEquipo
from .etl_partido_estadio import extraerDataPartidoEstadio, limpiarDataPartidoEstadio, cargarDataPartidoEstadio
from .etl_competicion import extraerDataCompeticion, limpiarDataCompeticion, cargarDataCompeticion
from .etl_competicion_campeones import extraerDataCampeonesCompeticion, limpiarDataCampeonesCompeticion, cargarDataCampeonesCompeticion
from .etl_partido_competicion import extraerDataPartidoCompeticion, limpiarDataPartidoCompeticion, cargarDataPartidoCompeticion
from .etl_jugadores import extraerDataJugadoresEquipo, limpiarDataJugadoresEquipo, cargarDataJugadoresEquipo
from .etl_jugador import extraerDataJugador, limpiarDataJugador, cargarDataJugador
from .etl_partido_goleadores import extraerDataPartidoGoleadores, limpiarDataPartidoGoleadores, cargarDataPartidoGoleadores
from .etl_estadio import extraerDataEstadio, limpiarDataEstadio, cargarDataEstadio
from .etl_proximos_partidos import extraerDataProximosPartidosEquipo, limpiarDataProximosPartidosEquipo, cargarDataProximosPartidosEquipo
from .etl_entrenador import extraerDataEntrenador, limpiarDataEntrenador, cargarDataEntrenador
from .etl_jugador_equipos import extraerDataJugadorEquipos, limpiarDataJugadorEquipos, cargarDataJugadorEquipos
from .etl_jugador_seleccion import extraerDataJugadorSeleccion, limpiarDataJugadorSeleccion, cargarDataJugadorSeleccion
from .etl_entrenador_equipos import extraerDataEntrenadorEquipos, limpiarDataEntrenadorEquipos, cargarDataEntrenadorEquipos
from .etl_entrenador_palmares import extraerDataEntrenadorPalmares, limpiarDataEntrenadorPalmares, cargarDataEntrenadorPalmares
from .etl_partido_alineaciones import extraerDataPartidoAlineaciones, limpiarDataPartidoAlineaciones, cargarDataPartidoAlineaciones

def ETL_Equipos_Liga(liga:str, entorno:str)->None:

	print(f"ETL Equipos Liga {liga}")

	data=extraerDataEquiposLiga(liga)

	data_limpia=limpiarDataEquiposLiga(data)

	cargarDataEquiposLiga(data_limpia, entorno)

def ETL_Detalle_Equipo(equipo_id:str, entorno:str)->None:

	print(f"ETL Equipo {equipo_id}")

	data=extraerDataEquipoDetalle(equipo_id)

	data_limpia=limpiarDataEquipoDetalle(data)

	cargarDataEquipoDetalle(data_limpia, equipo_id, entorno)

def ETL_Escudo_Equipo(equipo_id:str, entorno:str)->None:

	print(f"ETL Escudo Equipo {equipo_id}")

	data=extraerDataEquipoEscudo(equipo_id)

	data_limpia=limpiarDataEquipoEscudo(data)

	cargarDataEquipoEscudo(data_limpia, equipo_id, entorno)

def ETL_Entrenador_Equipo(equipo_id:str, entorno:str)->None:

	print(f"ETL Entrenador Equipo {equipo_id}")

	data=extraerDataEquipoEntrenador(equipo_id)

	data_limpia=limpiarDataEquipoEntrenador(data)

	cargarDataEquipoEntrenador(data_limpia, equipo_id, entorno)

def ETL_Estadio_Equipo(equipo_id:str, entorno:str)->None:

	print(f"ETL Estadio Equipo {equipo_id}")

	data=extraerDataEquipoEstadio(equipo_id)

	data_limpia=limpiarDataEquipoEstadio(data)

	cargarDataEquipoEstadio(data_limpia, equipo_id, entorno)

def ETL_Palmares_Equipo(equipo_id:str, entorno:str)->None:

	print(f"ETL Palmares Equipo {equipo_id}")

	data=extraerDataEquipoPalmares(equipo_id)

	data_limpia=limpiarDataEquipoPalmares(data)

	cargarDataEquipoPalmares(data_limpia, equipo_id, entorno)

def ETL_Partidos_Equipo(equipo_id:int, temporada:int, entorno:str)->None:

	print(f"ETL Partidos Equipo {equipo_id} Temporada {temporada}")

	data=extraerDataPartidosEquipo(equipo_id, temporada)

	data_limpia=limpiarDataPartidosEquipo(data)

	cargarDataPartidosEquipo(data_limpia, entorno)

def ETL_Partido_Estadio(equipo_local:str, equipo_visitante:str, partido_id:str, entorno:str)->None:

	print(f"ETL Partido Estadio {equipo_local} vs {equipo_visitante} - {partido_id}")

	data=extraerDataPartidoEstadio(equipo_local, equipo_visitante, partido_id)

	data_limpia=limpiarDataPartidoEstadio(data)

	cargarDataPartidoEstadio(data_limpia, partido_id, entorno)

def ETL_Competicion(competicion_id:str, entorno:str)->None:

	print(f"ETL Competicion {competicion_id}")

	data=extraerDataCompeticion(competicion_id)

	data_limpia=limpiarDataCompeticion(data)

	cargarDataCompeticion(data_limpia, competicion_id, entorno)

def ETL_Campeones_Competicion(competicion_id:str, entorno:str)->None:

	print(f"ETL Campeones Competicion {competicion_id}")

	data=extraerDataCampeonesCompeticion(competicion_id)

	data_limpia=limpiarDataCampeonesCompeticion(data)

	cargarDataCampeonesCompeticion(data_limpia, competicion_id, entorno)

def ETL_Partido_Competicion(equipo_local:str, equipo_visitante:str, partido_id:str, entorno:str)->None:

	print(f"ETL Partido Competicion {equipo_local} vs {equipo_visitante} - {partido_id}")

	data=extraerDataPartidoCompeticion(equipo_local, equipo_visitante, partido_id)

	data_limpia=limpiarDataPartidoCompeticion(data)

	cargarDataPartidoCompeticion(data_limpia, partido_id, entorno)

def ETL_Partido_Goleadores(equipo_local:str, equipo_visitante:str, partido_id:str, entorno:str)->None:

	print(f"ETL Partido Goleadores {equipo_local} vs {equipo_visitante} - {partido_id}")

	data=extraerDataPartidoGoleadores(equipo_local, equipo_visitante, partido_id)

	data_limpia=limpiarDataPartidoGoleadores(data)

	cargarDataPartidoGoleadores(data_limpia, partido_id, entorno)

def ETL_Partido_Alineaciones(equipo_local:str, equipo_visitante:str, partido_id:str, entorno:str)->None:

	print(f"ETL Partido Alineaciones {equipo_local} vs {equipo_visitante} - {partido_id}")

	data=extraerDataPartidoAlineaciones(equipo_local, equipo_visitante, partido_id)

	data_limpia=limpiarDataPartidoAlineaciones(data)

	cargarDataPartidoAlineaciones(data_limpia, partido_id, entorno)

def ETL_Jugadores_Equipo(equipo_id:int, temporada:int, entorno:str)->None:

	print(f"ETL Jugadores Equipo {equipo_id} Temporada {temporada}")

	data=extraerDataJugadoresEquipo(equipo_id, temporada)

	data_limpia=limpiarDataJugadoresEquipo(data)

	cargarDataJugadoresEquipo(data_limpia, entorno)

def ETL_Jugador(jugador_id:str, entorno:str)->None:

	print(f"ETL Jugador {jugador_id}")

	data=extraerDataJugador(jugador_id)

	data_limpia=limpiarDataJugador(data)

	cargarDataJugador(data_limpia, jugador_id, entorno)

def ETL_Jugador_Equipos(jugador_id:str, entorno:str)->None:

	print(f"ETL Jugador Equipos {jugador_id}")

	data=extraerDataJugadorEquipos(jugador_id)

	data_limpia=limpiarDataJugadorEquipos(data)

	cargarDataJugadorEquipos(data_limpia, jugador_id, entorno)

def ETL_Jugador_Seleccion(jugador_id:str, entorno:str)->None:

	print(f"ETL Jugador Seleccion {jugador_id}")

	data=extraerDataJugadorSeleccion(jugador_id)

	data_limpia=limpiarDataJugadorSeleccion(data)

	cargarDataJugadorSeleccion(data_limpia, jugador_id, entorno)

def ETL_Estadio(estadio_id:str, entorno:str)->None:

	print(f"ETL Estadio {estadio_id}")

	data=extraerDataEstadio(estadio_id)

	data_limpia=limpiarDataEstadio(data)

	cargarDataEstadio(data_limpia, estadio_id, entorno)

def ETL_Proximos_Partidos_Equipo(equipo_id:int, temporada:int, entorno:str)->None:

	print(f"ETL Proximos Partidos Equipo {equipo_id} Temporada {temporada}")

	data=extraerDataProximosPartidosEquipo(equipo_id, temporada)

	data_limpia=limpiarDataProximosPartidosEquipo(data)

	cargarDataProximosPartidosEquipo(data_limpia, entorno)

def ETL_Entrenador(entrenador_id:str, entorno:str)->None:

	print(f"ETL Entrenador {entrenador_id}")

	data=extraerDataEntrenador(entrenador_id)

	data_limpia=limpiarDataEntrenador(data)

	cargarDataEntrenador(data_limpia, entrenador_id, entorno)

def ETL_Entrenador_Equipos(entrenador_id:str, entorno:str)->None:

	print(f"ETL Entrenador Equipos {entrenador_id}")

	data=extraerDataEntrenadorEquipos(entrenador_id)

	data_limpia=limpiarDataEntrenadorEquipos(data)

	cargarDataEntrenadorEquipos(data_limpia, entrenador_id, entorno)

def ETL_Palmares_Entrenador(entrenador_id:str, entorno:str)->None:

	print(f"ETL Palmares Entrenador {entrenador_id}")

	data=extraerDataEntrenadorPalmares(entrenador_id)

	data_limpia=limpiarDataEntrenadorPalmares(data)

	cargarDataEntrenadorPalmares(data_limpia, entrenador_id, entorno)