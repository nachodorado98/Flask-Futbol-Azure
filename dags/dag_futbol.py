from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash_operator import BashOperator
import os

from python.src.etls import ETL_Equipos_Liga
from python.src.database.conexion import Conexion

def existe_carpeta()->str:

	return "pipeline_equipos_ligas" if os.path.exists(os.path.join(os.getcwd(), "dags", "logs")) else "carpeta_logs"

def crearArchivoLog(motivo:str)->None:

	archivo_log=f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

	ruta_log=os.path.join(os.getcwd(), "dags", "logs", archivo_log)

	with open(ruta_log, "w") as archivo:

		archivo.write(f"Error en ejecucion: {motivo}")

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


with DAG("dag_futbol",
		start_date=datetime(2024,6,8),
		description="DAG para obtener datos de la web de futbol",
		schedule_interval=None,
		catchup=False) as dag:

	tarea_existe_carpeta=BranchPythonOperator(task_id="existe_carpeta", python_callable=existe_carpeta)

	comando_bash="cd ../../opt/airflow/dags && mkdir logs"

	tarea_carpeta_logs=BashOperator(task_id="carpeta_logs", bash_command=comando_bash)

	tarea_pipeline_equipos_ligas=PythonOperator(task_id="pipeline_equipos_ligas", python_callable=Pipeline_Equipos_Ligas, trigger_rule="none_failed_min_one_success")

tarea_existe_carpeta >> [tarea_carpeta_logs, tarea_pipeline_equipos_ligas]

tarea_carpeta_logs >> tarea_pipeline_equipos_ligas