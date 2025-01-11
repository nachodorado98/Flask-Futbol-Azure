from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.utils.task_group import TaskGroup
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago

from utils import existe_entorno, ejecutarDagEntrenadores, actualizarVariable, crearArchivoLog

from config import BASH_LOGS, BASH_ESCUDOS, BASH_ENTRENADORES, BASH_PRESIDENTES, BASH_ESTADIOS
from config import BASH_COMPETICIONES, BASH_PAISES, BASH_JUGADORES, BASH_SELECCIONES

from pipelines import Pipeline_Entrenadores_Equipos, Pipeline_Entrenadores

from datalake import data_lake_disponible_creado, subirPaisesEntrenadoresDataLake


with DAG("dag_entrenadores",
		start_date=days_ago(1),
		description="DAG para obtener datos de los entrenadores de la web de futbol",
		schedule_interval="@monthly",
		catchup=False) as dag:



	with TaskGroup("entorno") as tareas_entorno:

		tarea_existe_entorno=BranchPythonOperator(task_id="existe_entorno", python_callable=existe_entorno)

		tarea_carpeta_logs=BashOperator(task_id="carpeta_logs", bash_command=BASH_LOGS)

		tarea_carpeta_escudos=BashOperator(task_id="carpeta_escudos", bash_command=BASH_ESCUDOS)

		tarea_carpeta_entrenadores=BashOperator(task_id="carpeta_entrenadores", bash_command=BASH_ENTRENADORES)

		tarea_carpeta_presidentes=BashOperator(task_id="carpeta_presidentes", bash_command=BASH_PRESIDENTES)

		tarea_carpeta_estadios=BashOperator(task_id="carpeta_estadios", bash_command=BASH_ESTADIOS)

		tarea_carpeta_competiciones=BashOperator(task_id="carpeta_competiciones", bash_command=BASH_COMPETICIONES)

		tarea_carpeta_paises=BashOperator(task_id="carpeta_paises", bash_command=BASH_PAISES)

		tarea_carpeta_jugadores=BashOperator(task_id="carpeta_jugadores", bash_command=BASH_JUGADORES)

		tarea_carpeta_selecciones=BashOperator(task_id="carpeta_selecciones", bash_command=BASH_SELECCIONES)

		tarea_entorno_creado=DummyOperator(task_id="entorno_creado")


		tarea_existe_entorno >> [tarea_carpeta_logs, tarea_entorno_creado]

		tarea_carpeta_logs >> tarea_carpeta_escudos >> tarea_carpeta_entrenadores >> tarea_carpeta_presidentes >> tarea_carpeta_estadios

		tarea_carpeta_estadios >> tarea_carpeta_competiciones >> tarea_carpeta_paises >> tarea_carpeta_jugadores >> tarea_carpeta_selecciones


	with TaskGroup("pipelines_entrenadores") as tareas_pipelines_entrenadores:

		tarea_pipeline_entrenadores_equipos=PythonOperator(task_id="pipeline_entrenadores_equipos", python_callable=Pipeline_Entrenadores_Equipos, trigger_rule="none_failed_min_one_success")

		tareas_pipeline_entrenadores_detalle=PythonOperator(task_id="pipeline_entrenadores", python_callable=Pipeline_Entrenadores)


		tarea_pipeline_entrenadores_equipos >> tareas_pipeline_entrenadores_detalle


	with TaskGroup("subir_data_lake") as tareas_subir_data_lake:

		tarea_subir_paises_entrenadores_data_lake=PythonOperator(task_id="subir_paises_entrenadores_data_lake", python_callable=subirPaisesEntrenadoresDataLake, trigger_rule="none_failed_min_one_success")
		

		tarea_subir_paises_entrenadores_data_lake


	tarea_ejecutar_dag_entrenadores=PythonOperator(task_id="ejecutar_dag_entrenadores", python_callable=ejecutarDagEntrenadores)

	tarea_data_lake_disponible=BranchPythonOperator(task_id="data_lake_disponible", python_callable=lambda: data_lake_disponible_creado("subir_data_lake.subir_paises_entrenadores_data_lake"))

	tarea_log_data_lake=PythonOperator(task_id="log_data_lake", python_callable=crearArchivoLog, op_kwargs={"motivo": "Error en la conexion con el Data Lake"})

	tarea_dag_entrenadores_completado=PythonOperator(task_id="dag_entrenadores_completado", python_callable=lambda: actualizarVariable("DAG_ENTRENADORES_EJECUTADO", "True"))


tarea_ejecutar_dag_entrenadores >> tareas_entorno >> tareas_pipelines_entrenadores >> tarea_data_lake_disponible >> [tareas_subir_data_lake, tarea_log_data_lake]

tareas_subir_data_lake >> tarea_dag_entrenadores_completado