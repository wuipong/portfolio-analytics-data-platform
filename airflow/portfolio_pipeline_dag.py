from airflow import DAG
from airflow.ops.python_operator import PythonOperator
from datetime import datetime
from main import run_pipeline  # 直接從根目錄匯入你的 Orchestrator

default_args = {
    'owner': 'analytics_engineer',
    'start_date': datetime(2024, 1, 1),
    'retries': 2
}

with DAG('portfolio_analytics_etl', default_args=default_args, schedule_interval='@daily') as dag:
    
    # execute main.py
    run_etl = PythonOperator(
        task_id='run_portfolio_etl',
        python_callable=run_pipeline
    )

    # If using dbt，change to
    # run_dbt = BashOperator(task_id='dbt_run', bash_command='dbt run')
    # run_etl >> run_dbt
