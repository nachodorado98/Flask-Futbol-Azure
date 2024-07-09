from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.utils.task_group import TaskGroup
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago

from utils import existe_entorno, ejecutarDagPartidos, actualizarVariable

from config import BASH_LOGS, BASH_ESCUDOS, BASH_ENTRENADORES, BASH_PRESIDENTES, BASH_ESTADIOS

from pipelines import Pipeline_Partidos_Equipo, Pipeline_Partidos_Estadio



with DAG("dag_partidos",
		start_date=days_ago(1),
		description="DAG para obtener datos de los partidos de la web de futbol",
		schedule_interval="@weekly",
		catchup=False) as dag:



	with TaskGroup("entorno") as tareas_entorno:

		tarea_existe_entorno=BranchPythonOperator(task_id="existe_entorno", python_callable=existe_entorno)

		tarea_carpeta_logs=BashOperator(task_id="carpeta_logs", bash_command=BASH_LOGS)

		tarea_carpeta_escudos=BashOperator(task_id="carpeta_escudos", bash_command=BASH_ESCUDOS)

		tarea_carpeta_entrenadores=BashOperator(task_id="carpeta_entrenadores", bash_command=BASH_ENTRENADORES)

		tarea_carpeta_presidentes=BashOperator(task_id="carpeta_presidentes", bash_command=BASH_PRESIDENTES)

		tarea_carpeta_estadios=BashOperator(task_id="carpeta_estadios", bash_command=BASH_ESTADIOS)

		tarea_entorno_creado=DummyOperator(task_id="entorno_creado")


		tarea_existe_entorno >> [tarea_carpeta_logs, tarea_entorno_creado]

		tarea_carpeta_logs >> tarea_carpeta_escudos >> tarea_carpeta_entrenadores >> tarea_carpeta_presidentes >> tarea_carpeta_estadios


	tarea_ejecutar_dag_partidos=PythonOperator(task_id="ejecutar_dag_partidos", python_callable=ejecutarDagPartidos)

	tarea_pipeline_partidos_equipo=PythonOperator(task_id="pipeline_partidos_equipo", python_callable=Pipeline_Partidos_Equipo, trigger_rule="none_failed_min_one_success")

	tarea_pipeline_partidos_estadio=PythonOperator(task_id="pipeline_partidos_estadio", python_callable=Pipeline_Partidos_Estadio)

	tarea_dag_partidos_completado=PythonOperator(task_id="dag_partidos_completado", python_callable=lambda: actualizarVariable("DAG_PARTIDOS_EJECUTADO", "True"))


tarea_ejecutar_dag_partidos >> tareas_entorno >>  tarea_pipeline_partidos_equipo >> tarea_pipeline_partidos_estadio >> tarea_dag_partidos_completado