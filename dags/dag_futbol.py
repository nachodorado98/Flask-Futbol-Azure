from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
import os
import time

from python.src.etls import ETL_Equipos_Liga, ETL_Detalle_Equipo, ETL_Escudo_Equipo
from python.src.etls import ETL_Entrenador_Equipo, ETL_Estadio_Equipo
from python.src.database.conexion import Conexion
from python.src.utils import descargarImagen, entorno_creado, crearEntornoDataLake
from python.src.datalake.conexion_data_lake import ConexionDataLake

def existe_entorno()->str:

	return "pipeline_equipos_ligas" if os.path.exists(os.path.join(os.getcwd(), "dags", "entorno")) else "carpeta_logs"

def crearArchivoLog(motivo:str)->None:

	archivo_log=f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

	ruta_log=os.path.join(os.getcwd(), "dags", "entorno", "logs", archivo_log)

	with open(ruta_log, "w") as archivo:

		archivo.write(f"Error!!! {motivo}")

def Pipeline_Equipos_Ligas()->None:

	con=Conexion()

	ligas=con.obtenerLigas()

	for liga in ligas:

		try:
			
			ETL_Equipos_Liga(liga)

		except Exception as e:

			mensaje=f"Liga: {liga} - Motivo: {e}"
		
			print(f"Error en liga {liga}")

			crearArchivoLog(mensaje)

	con.cerrarConexion()

def Pipeline(funcion):

	def wrapper():

		con=Conexion()

		equipos=con.obtenerEquipos()

		for equipo in equipos:

			try:

				funcion(equipo)

			except Exception as e:

				mensaje=f"Equipo: {equipo} - Motivo: {e}"

				print(f"Error en equipo {equipo}")

				crearArchivoLog(mensaje)

			time.sleep(0.5)

		con.cerrarConexion()

	return wrapper

@Pipeline
def Pipeline_Detalle_Equipos(equipo):
	ETL_Detalle_Equipo(equipo)

@Pipeline
def Pipeline_Escudo_Equipos(equipo):
	ETL_Escudo_Equipo(equipo)

@Pipeline
def Pipeline_Entrenador_Equipos(equipo):
	ETL_Entrenador_Equipo(equipo)

@Pipeline
def Pipeline_Estadio_Equipos(equipo):
	ETL_Estadio_Equipo(equipo)

def descargarEscudos()->None:

	con=Conexion()

	codigo_escudos=con.obtenerCodigoEscudos()

	con.cerrarConexion()

	ruta_imagenes=os.path.join(os.getcwd(), "dags", "entorno", "imagenes", "escudos")

	for codigo in codigo_escudos:

		print(f"Descargando imagen {codigo}...")

		try:

			descargarImagen("https://cdn.resfu.com/img_data/equipos/", codigo, ruta_imagenes)

		except Exception as e:

			mensaje=f"Imagen: {codigo} - Motivo: {e}"

			print(f"Error en imagen con codigo {codigo}")

			crearArchivoLog(mensaje)

	print("Descarga de escudos finalizada")

def data_lake_disponible()->str:

	try:

		con=ConexionDataLake()

		con.cerrarConexion()

		return "entorno_data_lake_creado"

	except Exception:

		return "log_data_lake"

def entorno_data_lake_creado():

	if not entorno_creado("contenedorequipos"):

		return "crear_entorno_data_lake"

	return "entorno_creado"

def creacion_entorno_data_lake()->None:

	crearEntornoDataLake("contenedorequipos", "escudos")

	print("Entorno Data Lake creado")




with DAG("dag_futbol",
		start_date=datetime(2024,6,8),
		description="DAG para obtener datos de la web de futbol",
		schedule_interval=None,
		catchup=False) as dag:

	tarea_existe_entorno=BranchPythonOperator(task_id="existe_entorno", python_callable=existe_entorno)

	comando_bash_logs="cd ../../opt/airflow/dags && mkdir -p entorno/logs"

	comando_bash_imagenes="cd ../../opt/airflow/dags && mkdir -p entorno/imagenes/escudos"

	tarea_carpeta_logs=BashOperator(task_id="carpeta_logs", bash_command=comando_bash_logs)

	tarea_carpeta_imagenes=BashOperator(task_id="carpeta_imagenes", bash_command=comando_bash_imagenes)

	tarea_pipeline_equipos_ligas=PythonOperator(task_id="pipeline_equipos_ligas", python_callable=Pipeline_Equipos_Ligas, trigger_rule="none_failed_min_one_success")

	tarea_pipeline_detalle_equipos=PythonOperator(task_id="pipeline_detalle_equipos", python_callable=Pipeline_Detalle_Equipos)

	tarea_pipeline_escudo_equipos=PythonOperator(task_id="pipeline_escudo_equipos", python_callable=Pipeline_Escudo_Equipos)

	tarea_pipeline_entrenador_equipos=PythonOperator(task_id="pipeline_entrenador_equipos", python_callable=Pipeline_Entrenador_Equipos)

	tarea_pipeline_estadio_equipos=PythonOperator(task_id="pipeline_estadio_equipos", python_callable=Pipeline_Estadio_Equipos)

	tarea_descargar_escudos=PythonOperator(task_id="descargar_escudos", python_callable=descargarEscudos)

	tarea_data_lake_disponible=BranchPythonOperator(task_id="data_lake_disponible", python_callable=data_lake_disponible)

	tarea_log_data_lake=PythonOperator(task_id="log_data_lake", python_callable=crearArchivoLog, op_kwargs={"motivo": "Error en la conexion con el Data Lake"})

	tarea_entorno_data_lake_creado=BranchPythonOperator(task_id="entorno_data_lake_creado", python_callable=entorno_data_lake_creado)

	tarea_crear_entorno_data_lake=PythonOperator(task_id="crear_entorno_data_lake", python_callable=creacion_entorno_data_lake)

	tarea_entorno_creado=DummyOperator(task_id="entorno_creado", trigger_rule="none_failed_min_one_success")

tarea_existe_entorno >> [tarea_carpeta_logs, tarea_pipeline_equipos_ligas]

tarea_carpeta_logs >> tarea_carpeta_imagenes >> tarea_pipeline_equipos_ligas

tarea_pipeline_equipos_ligas >> tarea_pipeline_detalle_equipos >> tarea_pipeline_escudo_equipos >> tarea_pipeline_entrenador_equipos >> tarea_pipeline_estadio_equipos

tarea_pipeline_estadio_equipos >> tarea_descargar_escudos >> tarea_data_lake_disponible >> [tarea_entorno_data_lake_creado, tarea_log_data_lake]

tarea_entorno_data_lake_creado >> [tarea_crear_entorno_data_lake, tarea_entorno_creado]

tarea_crear_entorno_data_lake >> tarea_entorno_creado