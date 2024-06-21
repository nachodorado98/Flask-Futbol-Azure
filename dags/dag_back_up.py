from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator

from utils import ejecutarDagBackUp

from datalake import subirBackUpTablasDataLake



with DAG("dag_back_up",
		start_date=datetime(2024,6,21),
		description="DAG para realizar un backup de las tablas de los datos de la web de futbol",
		schedule_interval="@monthly",
		catchup=False) as dag:

	tarea_ejecutar_dag_back_up=PythonOperator(task_id="ejecutar_dag_back_up", python_callable=ejecutarDagBackUp)

	tarea_subir_back_up_data_lake=PythonOperator(task_id="subir_back_up_data_lake", python_callable=subirBackUpTablasDataLake)


tarea_ejecutar_dag_back_up >> tarea_subir_back_up_data_lake