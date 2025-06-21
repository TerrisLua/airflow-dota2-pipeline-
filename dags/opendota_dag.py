from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
from scripts.extract import fetch_pro_matches
from scripts.load import load_to_postgres
from scripts.email_report import send_report
from scripts.notify import task_success_alert, task_failure_alert


# Define default arguments for all tasks in the DAG
default_args = {
    "owner": "airflow",
    "start_date": datetime(2023, 1, 1),  # Required to initialize the DAG
}

# Define the DAG object with a daily schedule at 11:15 PM SGT (15:23 UTC)
with DAG(
    "opendota_etl",
    schedule_interval="15 23 * * *",  # runs every day at 11:15 PM SGT
    catchup=False,  # Don't run backfill for previous dates
    default_args=default_args
) as dag:

    # Task 1: Fetch data from OpenDota API and save to CSV
    extract = PythonOperator(
        task_id="extract",
        python_callable=fetch_pro_matches,
        on_failure_callback=task_failure_alert  # Notify on failure
    )

    # Task 2: Load the CSV data into PostgreSQL
    load = PythonOperator(
        task_id="load",
        python_callable=load_to_postgres,
        on_failure_callback=task_failure_alert
    )

    # Task 3: Run dbt transformations inside the container
    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command='cd /usr/app && dbt run',  # assumes dbt is installed in this path
        on_failure_callback=task_failure_alert
    )

    # Task 4: Send the report via email if all previous steps succeed
    email = PythonOperator(
        task_id="send_report",
        python_callable=send_report,
        on_success_callback=task_success_alert,  # Notify on success
        on_failure_callback=task_failure_alert
    )

# Define task execution order: extract → load → dbt → email
extract >> load >> dbt_run >> email
