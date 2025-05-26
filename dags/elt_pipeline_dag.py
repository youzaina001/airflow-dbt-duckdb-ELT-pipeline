from __future__ import annotations
import pendulum
from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
import os

# Define where our project lives inside the Airflow environment.
PROJECT_DIR = '/usr/local/airflow/dags/lydia-data-engineer-ELT-pipeline'

# Define paths to our scripts and dbt project
EXTRACT_SCRIPT = '/usr/local/airflow/include/extract.py'
LOAD_SCRIPT = '/usr/local/airflow/include/load.py'
DBT_DIR = '/usr/local/airflow/dbt_project'
VISUALIZE_SCRIPT = '/usr/local/airflow/include/visualize.py'

with DAG(
    dag_id='simple_crypto_elt_pipeline',
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    schedule='@daily',
    catchup=False,
    tags=['crypto', 'elt', 'simple'],
    doc_md="""
    ### Simple Crypto ELT Pipeline
    1.  **Extract**: Runs `extract.py` to get data.
    2.  **Load**: Runs `load.py` to store data.
    3.  **Transform**: Runs `dbt run` to process data.
    """
) as dag:

    # Task 1: Run the extract script using Bash
    extract_task = BashOperator(
        task_id='run_extract_script',
        bash_command=f"echo 'Running Extract Script...' && python {EXTRACT_SCRIPT}",
    )

    # Task 2: Run the load script using Bash
    load_task = BashOperator(
        task_id='run_load_script',
        bash_command=f"echo 'Running Load Script...' && python {LOAD_SCRIPT}",
    )

    # Task 3: Run dbt (assuming dbt is installed and configured)
    # We change directory (cd) into the dbt folder first.
    dbt_run_task = BashOperator(
        task_id='run_dbt_transformations',
        bash_command=(
            f"echo 'Running dbt transformations...' && "
            f"cd {DBT_DIR} && "
            f"dbt run --profiles-dir ." # Tells dbt where to find profiles.yml
        ),
    )

    # Task 4: Run dbt tests
    dbt_test_task = BashOperator(
        task_id='run_dbt_tests',
        bash_command=(
            f"echo 'Running dbt tests...' && "
            f"cd {DBT_DIR} && "
            f"dbt test --profiles-dir ."
        ),
    )

    # Task 5: Generate data visualization
    generate_viz_task = BashOperator(
        task_id='generate_candlestick_visualization', # Renamed for clarity
        bash_command=f"echo 'Generating candlestick visualization...' && python {VISUALIZE_SCRIPT}",
    )

    # Define the order: Extract -> Load -> Transform -> Test -> Visualize
    extract_task >> load_task >> dbt_run_task >> dbt_test_task >> generate_viz_task
    print("DAG defined successfully with tasks: Extract, Load, Transform, Test, and Visualization.")