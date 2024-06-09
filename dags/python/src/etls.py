from .etl_equipos_liga import extraerDataEquiposLiga, limpiarDataEquiposLiga, cargarDataEquiposLiga
from .etl_equipo import extraerDataEquipoDetalle, limpiarDataEquipoDetalle, cargarDataEquipoDetalle
from .etl_equipo_escudo import extraerDataEquipoEscudo, limpiarDataEquipoEscudo, cargarDataEquipoEscudo

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