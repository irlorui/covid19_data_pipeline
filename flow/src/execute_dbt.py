import subprocess
import sys
import logging


def run_dbt_command(dbt_command: str,
                    profiles_dir: str = './dbt_project/profiles/',
                    project_dir: str = './dbt_project',
                    target: str = 'clinical_trial',
                    models_path: str = 'models/staging'):
    
    command_args = [
        "dbt", 
        dbt_command,
        f"--profiles-dir={profiles_dir}",
        f"--project-dir={project_dir}",
        f"--target={target}",
        f"--models={models_path}"
    ]

    print(f'{dbt_command}ing {models_path} models with DBT...')
    print(f'Executing dbt command: \n {command_args}')

    try:
        result = subprocess.run(command_args, 
                                cwd = '/opt/airflow/src',
                                capture_output=False)
        print(f"Process {dbt_command} on {models_path} models completed successfully.\n")
    except subprocess.CalledProcessError:
        print(f"Process {dbt_command} on {models_path} models failed.")
        sys.exit(1)
