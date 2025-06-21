# Start from official Airflow image
FROM apache/airflow:2.8.1-python3.10

# Set working directory inside the container
WORKDIR /opt/airflow

# Copy your requirements.txt into the image
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Optional: Copy your entire project (if needed for scripts)
# COPY . .

# Airflow will still use entrypoint and DAGs as defined in docker-compose