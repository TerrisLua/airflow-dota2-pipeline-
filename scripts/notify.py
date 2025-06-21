from airflow.utils.email import send_email
import os
import requests
from dotenv import load_dotenv
import logging

# Load environment variables early
load_dotenv(dotenv_path='/opt/airflow/dags/env_file.env')

def task_success_alert(context):
    logging.info("✅ task_success_alert called")  # Log that this callback was triggered

    # Extract relevant metadata from the Airflow context
    task_instance = context["task_instance"]
    dag = context["dag"]
    dag_id = dag.dag_id  # The name of the DAG/pipeline
    task_id = task_instance.task_id  # The name of the specific task
    run_id = context.get("run_id", "N/A")  # Unique identifier for this DAG run
    execution_date = str(context.get("execution_date", "N/A"))  # When this task was scheduled to run
    log_url = task_instance.log_url  # Direct link to the Airflow UI log for this task instance

    # Format a Slack-friendly message with all the key metadata and explanation
    message = (
        f":white_check_mark: *Task Succeeded*\n"
        f"**What happened:** Task *`{task_id}`* in pipeline *`{dag_id}`* ran successfully.\n\n"
        f"📦 *Pipeline Run ID:* `{run_id}`\n"
        f"🕒 *Execution Time:* `{execution_date}`\n"
        f"🔗 <{log_url}|View Task Logs>\n\n"
        f"✅ This means the task completed as expected without any errors. No further action is needed."
    )

    # Get the Slack webhook URL from environment variable
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    # Send the message to Slack, and log the result
    if webhook_url:
        try:
            response = requests.post(webhook_url, json={"text": message})
            logging.info(f"📤 Slack response status: {response.status_code}")
        except Exception as e:
            logging.error(f"Slack notification failed: {str(e)}")
    else:
        logging.warning("⚠️ SLACK_WEBHOOK_URL is not set in environment.")


def task_failure_alert(context):
    logging.info("🚨 task_failure_alert called")  # Log that this callback was triggered

    # Extract relevant metadata from the Airflow context
    task_instance = context["task_instance"]
    dag = context["dag"]
    dag_id = dag.dag_id  # The name of the DAG/pipeline
    task_id = task_instance.task_id  # The specific task that failed
    run_id = context.get("run_id", "N/A")  # The specific DAG run instance
    execution_date = str(context.get("execution_date", "N/A"))  # When this task was meant to execute
    log_url = task_instance.log_url  # URL to Airflow log page for this task instance
    exception = str(context.get("exception", "No exception info"))  # Error thrown by the task

    # Construct a Slack-friendly alert message with helpful info and next steps
    message = (
        f":x: *Task Failed*\n"
        f"**What happened:** Task *`{task_id}`* in pipeline *`{dag_id}`* has failed to complete.\n\n"
        f"📦 *Pipeline Run ID:* `{run_id}`\n"
        f"🕒 *Execution Time:* `{execution_date}`\n"
        f"🔗 <{log_url}|View Task Logs>\n"
        f"🧨 *Error:* `{exception}`\n\n"
        f"⚠️ This means the task encountered an error and did not finish. "
        f"Please check the logs and resolve the issue before re-running the DAG."
    )

    # Get the Slack webhook URL from the environment
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    # Send message to Slack, if the webhook URL is available
    if webhook_url:
        try:
            response = requests.post(webhook_url, json={"text": message})
            logging.info(f"📤 Slack response status: {response.status_code}")
        except Exception as e:
            logging.error(f"Slack notification failed: {str(e)}")
    else:
        logging.warning("⚠️ SLACK_WEBHOOK_URL is not set in environment.")