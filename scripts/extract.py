import requests
import pandas as pd
import os

def fetch_pro_matches():
    # Define where to store the data
    DATA_DIR = "/opt/airflow/dags/data"

    # Create the directory if it doesn't already exist
    os.makedirs(DATA_DIR, exist_ok=True)

    # Define the API URL to fetch professional match data
    url = "https://api.opendota.com/api/proMatches"

    # Make a GET request to the API
    res = requests.get(url)

    # Check if the request was successful (HTTP 200 OK)
    if res.status_code == 200:
        # Convert the JSON response to a pandas DataFrame
        df = pd.DataFrame(res.json())
        # Save the DataFrame to a CSV file
        df.to_csv(os.path.join(DATA_DIR, 'pro_matches.csv'), index=False)
    else:
        # Raise an error if the API request fails
        raise Exception(f"Failed to fetch: {res.status_code}")

    
