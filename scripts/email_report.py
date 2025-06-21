import smtplib
import pandas as pd
import psycopg2
from email.message import EmailMessage
import os
from dotenv import load_dotenv
from datetime import datetime
from zoneinfo import ZoneInfo

# Load environment variables from a specific .env file
load_dotenv(dotenv_path='/opt/airflow/dags/env_file.env')

def send_report():
    # Connect to PostgreSQL using credentials from environment variables
    conn = psycopg2.connect(
        dbname=os.getenv("PG_DB"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD"),
        host=os.getenv("PG_HOST"),
        port=os.getenv("PG_PORT")
    )

    # Run a SQL query and load the results into a pandas DataFrame
    df = pd.read_sql("SELECT * FROM mart_matches_summary", conn)

    # Define the path to save the CSV report
    csv_path = "/opt/airflow/dags/data/report.csv"

    # Save the DataFrame as a CSV file
    df.to_csv(csv_path, index=False)

    # Get current time in Singapore timezone
    sg_time = datetime.now(ZoneInfo("Asia/Singapore"))

    # Format the time nicely for the email
    sg_time_trimmed = sg_time.strftime("%Y-%m-%d %H:%M")

    # Set up the email message
    msg = EmailMessage()
    msg['Subject'] = 'Dota 2 Match Summary Report'  # Email subject
    msg['From'] = os.getenv("EMAIL_SENDER")         # Sender's email
    msg['To'] = os.getenv("EMAIL_RECIPIENT")        # Recipient's email

    # Email body with the report timestamp
    body = (f"Hi,\n\n"
            f"Attached is the Dota 2 Match Summary Report for {sg_time_trimmed}.\n\n"
            "Cheers,\n")
    msg.set_content(body)

    # Attach the CSV report to the email
    with open(csv_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="csv", filename="summary_report.csv")

    # Send the email using Gmail's SMTP server over SSL
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_PASSWORD"))  # Log in
        smtp.send_message(msg)  # Send the email
        print("sent")  # Print confirmation