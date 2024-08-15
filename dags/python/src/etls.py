from .etl_equipos_liga import extraerDataEquiposLiga, limpiarDataEquiposLiga, cargarDataEquiposLiga
from .etl_equipo import extraerDataEquipoDetalle, limpiarDataEquipoDetalle, cargarDataEquipoDetalle
from .etl_equipo_escudo import extraerDataEquipoEscudo, limpiarDataEquipoEscudo, cargarDataEquipoEscudo
from .etl_equipo_entrenador import extraerDataEquipoEntrenador, limpiarDataEquipoEntrenador, cargarDataEquipoEntrenador
from .etl_equipo_estadio import extraerDataEquipoEstadio, limpiarDataEquipoEstadio, cargarDataEquipoEstadio
from .etl_partidos import extraerDataPartidosEquipo, limpiarDataPartidosEquipo, cargarDataPartidosEquipo
from .etl_partido_estadio import extraerDataPartidoEstadio, limpiarDataPartidoEstadio, cargarDataPartidoEstadio
from .etl_competicion import extraerDataCompeticion, limpiarDataCompeticion, cargarDataCompeticion
from .etl_competicion_campeones import extraerDataCampeonesCompeticion, limpiarDataCampeonesCompeticion, cargarDataCampeonesCompeticion
from .etl_partido_competicion import extraerDataPartidoCompeticion, limpiarDataPartidoCompeticion, cargarDataPartidoCompeticion

def ETL_Equipos_Liga(liga:str)->None:

	print(f"ETL Equipos Liga {liga}")

	data=extraerDataEquiposLiga(liga)

	data_limpia=limpiarDataEquiposLiga(data)

	cargarDataEquiposLiga(data_limpia)

def ETL_Detalle_Equipo(equipo_id:str)->None:

	print(f"ETL Equipo {equipo_id}")

	data=extraerDataEquipoDetalle(equipo_id)

	data_limpia=limpiarDataEquipoDetalle(data)

	cargarDataEquipoDetalle(data_limpia, equipo_id)

def ETL_Escudo_Equipo(equipo_id:str)->None:

	print(f"ETL Escudo Equipo {equipo_id}")

	data=extraerDataEquipoEscudo(equipo_id)

	data_limpia=limpiarDataEquipoEscudo(data)

	cargarDataEquipoEscudo(data_limpia, equipo_id)

def ETL_Entrenador_Equipo(equipo_id:str)->None:

	print(f"ETL Entrenador Equipo {equipo_id}")

	data=extraerDataEquipoEntrenador(equipo_id)

	data_limpia=limpiarDataEquipoEntrenador(data)

	cargarDataEquipoEntrenador(data_limpia, equipo_id)

def ETL_Estadio_Equipo(equipo_id:str)->None:

	print(f"ETL Estadio Equipo {equipo_id}")

	data=extraerDataEquipoEstadio(equipo_id)

	data_limpia=limpiarDataEquipoEstadio(data)

	cargarDataEquipoEstadio(data_limpia, equipo_id)

def ETL_Partidos_Equipo(equipo_id:int, temporada:int)->None:

	print(f"ETL Partidos Equipo {equipo_id} Temporada {temporada}")

	data=extraerDataPartidosEquipo(equipo_id, temporada)

	data_limpia=limpiarDataPartidosEquipo(data)

	cargarDataPartidosEquipo(data_limpia)

def ETL_Partido_Estadio(equipo_local:str, equipo_visitante:str, partido_id:str)->None:

	print(f"ETL Partido Estadio {equipo_local} vs {equipo_visitante} - {partido_id}")

	data=extraerDataPartidoEstadio(equipo_local, equipo_visitante, partido_id)

	data_limpia=limpiarDataPartidoEstadio(data)

	cargarDataPartidoEstadio(data_limpia, partido_id)

def ETL_Competicion(competicion_id:str)->None:

	print(f"ETL Competicion {competicion_id}")

	data=extraerDataCompeticion(competicion_id)

	data_limpia=limpiarDataCompeticion(data)

	cargarDataCompeticion(data_limpia, competicion_id)

def ETL_Campeones_Competicion(competicion_id:str)->None:

	print(f"ETL Campeones Competicion {competicion_id}")

	data=extraerDataCampeonesCompeticion(competicion_id)

	data_limpia=limpiarDataCampeonesCompeticion(data)

	cargarDataCampeonesCompeticion(data_limpia, competicion_id)

def ETL_Partido_Competicion(equipo_local:str, equipo_visitante:str, partido_id:str)->None:

	print(f"ETL Partido Competicion {equipo_local} vs {equipo_visitante} - {partido_id}")

	data=extraerDataPartidoCompeticion(equipo_local, equipo_visitante, partido_id)

	data_limpia=limpiarDataPartidoCompeticion(data)

	cargarDataPartidoCompeticion(data_limpia, partido_id)