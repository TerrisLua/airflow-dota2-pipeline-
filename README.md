# Dota 2 ETL Pipeline

This is a personal data engineering project that automates the extraction, transformation, and reporting of professional Dota 2 match data.

The pipeline is fully containerized using **Docker** and uses **Apache Airflow**, **Python**, **dbt**, and **PostgreSQL** to manage daily ETL workflows. Slack notifications and email reports are also included for monitoring and output delivery.

---

## 💡 Purpose

To simulate a real-world ETL pipeline setup using modern tools and a reproducible Docker-based environment.

---

## 🛠️ Tools & Techniques

- **Docker + Docker Compose** – containerized setup for all services (Airflow, dbt, PostgreSQL)
- **Apache Airflow** – DAG orchestration and scheduling
- **Python** – for data extraction, loading, email sending, and Slack alerts
- **dbt** – for SQL-based data transformation and modeling
- **PostgreSQL** – data warehouse for match data
- **Slack Webhooks** – for real-time success/failure notifications
- **SMTP (Gmail)** – for sending reports via email
- **.env files** – for environment variable and secret management

---

## 🚀 Workflow Overview

1. **Extract**: Pull latest pro match data from [OpenDota API](https://docs.opendota.com/)
2. **Load**: Insert raw data into PostgreSQL
3. **Transform**: Use dbt to create summary models
4. **Report**: Send a summary report as a CSV via email
5. **Notify**: Send Slack alerts for each DAG task outcome

---
## 📦 Project Structure

dota2-etl-pipeline/
├── dags/
│ ├── opendota_dag.py # Airflow DAG definition
│ └── env_file.env # Environment variables (not tracked)
├── scripts/
│ ├── extract.py # Fetches match data from OpenDota API
│ ├── load.py # Loads data into PostgreSQL
│ ├── notify.py # Sends Slack alerts
│ └── email_report.py # Generates and emails summary reports
├── dbt/
│ ├── models/ mart # dbt models for transformations
│ └── dbt_project.yml # dbt configuration
│ └── profiles.yml #  dbt connection settings (used by Docker)
├── Dockerfile # Custom Airflow image
├── docker-compose.yml # Defines and runs the container stack
├── .gitignore # Excludes logs, env files, etc.
└── README.md # Project overview and documentation

## 🏗️ Tech Stack

| Tool            | Purpose                                 |
|-----------------|------------------------------------------|
| Docker          | Containerization of the entire project   |
| Airflow         | Workflow scheduling and task orchestration |
| Python          | Extraction, loading, email, Slack alerts |
| dbt             | SQL-based data modeling and transformation |
| PostgreSQL      | Central data warehouse                   |
| Slack Webhooks  | Real-time task notifications             |
| SMTP (Gmail)    | Send match summary report via email      |

---

