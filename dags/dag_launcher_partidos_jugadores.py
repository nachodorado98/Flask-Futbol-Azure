from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.utils.dates import days_ago

from utils import obtenerEquiposProximosPartidos

equipos=obtenerEquiposProximosPartidos()

with DAG("dag_launcher_partidos_jugadores",
            start_date=days_ago(1),
            schedule_interval=None,
            catchup=False) as dag:

    previous_task=None

    for equipo in equipos:

        trigger=TriggerDagRunOperator(task_id=f"trigger_{equipo['equipo_id_real']}",
                                        trigger_dag_id="dag_partidos_jugadores",
                                        conf={"equipo_id":equipo["equipo_id"], "equipo_id_real":equipo["equipo_id_real"]},
                                        wait_for_completion=True)

        if previous_task:

            previous_task >> trigger

        previous_task=trigger