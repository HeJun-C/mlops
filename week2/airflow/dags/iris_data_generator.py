from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import csv
import random

default_args = {
    "owner": "student",
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}

# Simple iris-like label buckets
IRIS_CLASSES = ["setosa", "versicolor", "virginica"]

def generate_iris_batch(**context):
    """
    Generate 100 random iris-like samples and append to a CSV file.
    Output columns:
      sepal_length, sepal_width, petal_length, petal_width, label, generated_at
    """
    # Airflow provides these in context
    logical_date = context["logical_date"]  # timezone-aware datetime
    ts = logical_date.isoformat()

    # Write under /opt/airflow (inside container). This is usually mounted with docker compose.
    out_dir = "/opt/airflow/generated_data"
    os.makedirs(out_dir, exist_ok=True)

    out_path = os.path.join(out_dir, "iris_training_data.csv")

    file_exists = os.path.exists(out_path)

    rows = []
    for _ in range(100):
        # Reasonable numeric ranges (not scientifically exact, but iris-like)
        sepal_length = round(random.uniform(4.0, 8.0), 2)
        sepal_width  = round(random.uniform(2.0, 4.5), 2)
        petal_length = round(random.uniform(1.0, 7.0), 2)
        petal_width  = round(random.uniform(0.1, 2.6), 2)
        label = random.choice(IRIS_CLASSES)

        rows.append([sepal_length, sepal_width, petal_length, petal_width, label, ts])

    with open(out_path, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["sepal_length", "sepal_width", "petal_length", "petal_width", "label", "generated_at"])
        writer.writerows(rows)

    print(f"Wrote 100 rows to {out_path} at {ts}")

with DAG(
    dag_id="iris_training_data_every_minute",
    default_args=default_args,
    description="Generate 100 iris training rows every minute via PythonOperator",
    start_date=datetime(2024, 12, 14),
    schedule_interval="* * * * *",   # every minute
    catchup=False,                   # don't backfill old runs
    max_active_runs=1,
) as dag:

    generate_data = PythonOperator(
        task_id="generate_iris_training_data",
        python_callable=generate_iris_batch,
        provide_context=True,   # safe even if newer Airflow ignores it
    )
