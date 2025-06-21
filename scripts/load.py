import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

def load_to_postgres():
    # Set the path to the CSV file that was previously downloaded
    csv_path = os.path.join("/opt/airflow/dags/data", "pro_matches.csv")  # ✅ absolute path inside container

    # Load the CSV into a pandas DataFrame
    df = pd.read_csv(csv_path)

    # Load environment variables from your .env file (database credentials, etc.)
    load_dotenv(dotenv_path='/opt/airflow/dags/env_file.env')

    # Define a list of required environment variables
    required_env = ["PG_DB", "PG_USER", "PG_PASSWORD", "PG_HOST", "PG_PORT"]

    # Print all the required environment variable values for debugging
    for var in required_env:
        print(f"{var}: {os.getenv(var)}")

    # Check if any required variables are missing and stop the script if they are
    missing_vars = [var for var in required_env if not os.getenv(var)]
    if missing_vars:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

    # Connect to PostgreSQL using credentials from the .env file
    conn = psycopg2.connect(
        dbname=os.getenv("PG_DB"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD"),
        host=os.getenv("PG_HOST"),
        port=os.getenv("PG_PORT")
    )
    print("PostgreSQL connection established.")

    # Create a cursor to execute SQL queries
    cur = conn.cursor()

    # Create the pro_matches table if it doesn't already exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS pro_matches (
            match_id BIGINT PRIMARY KEY,
            start_time BIGINT,
            duration INT,
            radiant_name TEXT,
            dire_name TEXT,
            league_name TEXT,
            radiant_win BOOLEAN
        );
    """)
    print("Creating Table")

    # Insert each row from the CSV into the database
    # If the match_id already exists, skip that row (no duplication)
    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO pro_matches (match_id, start_time, duration, radiant_name, dire_name, league_name, radiant_win)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (match_id) DO NOTHING;
        """, tuple(row[col] for col in ['match_id', 'start_time', 'duration', 'radiant_name', 'dire_name', 'league_name', 'radiant_win']))

    # Save changes and clean up
    conn.commit()
    cur.close()
    conn.close()


