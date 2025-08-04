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

    @task(task_id='transform_data')
    def transform_data():
        from src.execute_dbt import run_dbt_command
        run_dbt_command(dbt_command= 'run',
                        models_path = 'models/staging')
        
        run_dbt_command(dbt_command= 'test',
                        models_path = 'models/staging')

    t_transform_data = transform_data()
    
    @task(task_id='load_data')
    def load_data():
        from src.execute_dbt import run_dbt_command
        run_dbt_command(dbt_command= 'run',
                        models_path = 'models/prod')

    t_load_data = load_data()

    end = EmptyOperator(task_id="end")

    start >> t_extract_data >> t_transform_data >> t_load_data >> end

