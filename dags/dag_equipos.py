from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.utils.task_group import TaskGroup
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago

from utils import existe_entorno, crearArchivoLog, actualizarVariable

from config import BASH_LOGS, BASH_ESCUDOS, BASH_ENTRENADORES, BASH_PRESIDENTES, BASH_ESTADIOS
from config import BASH_COMPETICIONES, BASH_PAISES, BASH_JUGADORES, BASH_SELECCIONES

from pipelines import Pipeline_Equipos_Ligas
from pipelines import Pipeline_Detalle_Equipos, Pipeline_Escudo_Equipos, Pipeline_Entrenador_Equipos, Pipeline_Estadio_Equipos

from datalake import data_lake_disponible, entorno_data_lake_creado, creacion_entorno_data_lake
from datalake import subirEscudosDataLake, subirEntrenadoresDataLake, subirPresidentesDataLake, subirEstadiosDataLake, subirPaisesEquiposDataLake



with DAG("dag_equipos",
		start_date=days_ago(1),
		description="DAG para obtener datos de los equipos de la web de futbol",
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


	with TaskGroup("pipelines_equipos") as tareas_pipelines_equipos:

		tarea_pipeline_detalle_equipos=PythonOperator(task_id="pipeline_detalle_equipos", python_callable=Pipeline_Detalle_Equipos)

		tarea_pipeline_escudo_equipos=PythonOperator(task_id="pipeline_escudo_equipos", python_callable=Pipeline_Escudo_Equipos)

		tarea_pipeline_entrenador_equipos=PythonOperator(task_id="pipeline_entrenador_equipos", python_callable=Pipeline_Entrenador_Equipos)

		tarea_pipeline_estadio_equipos=PythonOperator(task_id="pipeline_estadio_equipos", python_callable=Pipeline_Estadio_Equipos)


		# Si tu maquina no tiene buenos recursos es preferible ejecutar en serie en vez de en paralelo

		tarea_pipeline_detalle_equipos >> tarea_pipeline_escudo_equipos >> tarea_pipeline_entrenador_equipos >> tarea_pipeline_estadio_equipos



	with TaskGroup("datalake") as tareas_datalake:

		tarea_entorno_data_lake_creado=BranchPythonOperator(task_id="entorno_data_lake_creado", python_callable=entorno_data_lake_creado)

		tarea_crear_entorno_data_lake=PythonOperator(task_id="crear_entorno_data_lake", python_callable=creacion_entorno_data_lake)

		tarea_no_crear_entorno_data_lake=DummyOperator(task_id="no_crear_entorno_data_lake")


		tarea_entorno_data_lake_creado >> [tarea_crear_entorno_data_lake, tarea_no_crear_entorno_data_lake]



	with TaskGroup("subir_data_lake") as tareas_subir_data_lake:

		tarea_subir_escudos_data_lake=PythonOperator(task_id="subir_escudos_data_lake", python_callable=subirEscudosDataLake, trigger_rule="none_failed_min_one_success")

		tarea_subir_entrenadores_data_lake=PythonOperator(task_id="subir_entrenadores_data_lake", python_callable=subirEntrenadoresDataLake, trigger_rule="none_failed_min_one_success")

		tarea_subir_presidentes_data_lake=PythonOperator(task_id="subir_presidentes_data_lake", python_callable=subirPresidentesDataLake, trigger_rule="none_failed_min_one_success")

		tarea_subir_estadios_data_lake=PythonOperator(task_id="subir_estadios_data_lake", python_callable=subirEstadiosDataLake, trigger_rule="none_failed_min_one_success")

		tarea_subir_paises_equipos_data_lake=PythonOperator(task_id="subir_paises_equipos_data_lake", python_callable=subirPaisesEquiposDataLake, trigger_rule="none_failed_min_one_success")


		# Si tu maquina no tiene buenos recursos es preferible ejecutar en serie en vez de en paralelo

		tarea_subir_escudos_data_lake >> tarea_subir_entrenadores_data_lake >> tarea_subir_presidentes_data_lake >> tarea_subir_estadios_data_lake >> tarea_subir_paises_equipos_data_lake



	tarea_pipeline_equipos_ligas=PythonOperator(task_id="pipeline_equipos_ligas", python_callable=Pipeline_Equipos_Ligas, trigger_rule="none_failed_min_one_success")

	tarea_data_lake_disponible=BranchPythonOperator(task_id="data_lake_disponible", python_callable=data_lake_disponible)

	tarea_log_data_lake=PythonOperator(task_id="log_data_lake", python_callable=crearArchivoLog, op_kwargs={"motivo": "Error en la conexion con el Data Lake"})

	tarea_dag_equipos_completado=PythonOperator(task_id="dag_equipos_completado", python_callable=lambda: actualizarVariable("DAG_EQUIPOS_EJECUTADO", "True"))
	


tareas_entorno >> tarea_pipeline_equipos_ligas >> tareas_pipelines_equipos >> tarea_data_lake_disponible >> [tareas_datalake, tarea_log_data_lake]

tareas_datalake >> tareas_subir_data_lake >> tarea_dag_equipos_completado