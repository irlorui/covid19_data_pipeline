from datetime import datetime

from airflow import DAG
from airflow.decorators import task
from airflow.operators.empty import EmptyOperator

default_args = {
    'owner': 'irene.lopez',
    'retries': 1,
}

with DAG(dag_id='clinical_trial_etl',
         start_date=datetime(2025, 8, 1), 
         schedule_interval=None,
         tags=['etl', 'clinical_trial'],
         catchup=False,
         default_args=default_args) as dag:

    start = EmptyOperator(task_id="start")

    @task(task_id='extract_data')
    def extract_data():
        from src.extract import extract_source_data 
        extract_source_data()

    t_extract_data = extract_data()

    end = EmptyOperator(task_id="end")

    start >> t_extract_data >> end

