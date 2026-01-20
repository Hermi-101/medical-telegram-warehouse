from dagster import job, op, Definitions
import subprocess
import os

@op
def scrape_telegram():
    """Task 1: Run the Scraper"""
    subprocess.run(["python", "src/scraper.py"], check=True)

@op
def load_to_postgres(wait_for):
    """Task 2: Load raw JSON to Database"""
    subprocess.run(["python", "scripts/load_to_db.py"], check=True)

@op
def run_dbt_transformations(wait_for):
    """Task 2: Run dbt models and tests"""
    # Change to dbt directory
    os.chdir("medical_warehouse")
    subprocess.run(["dbt", "run"], check=True)
    subprocess.run(["dbt", "test"], check=True)
    os.chdir("..")

@op
def run_yolo_enrichment(wait_for):
    """Task 3: Run YOLO and update database"""
    subprocess.run(["python", "src/yolo_detect.py"], check=True)
    subprocess.run(["python", "scripts/load_yolo_to_db.py"], check=True)

@job
def medical_data_pipeline():
    # Sequence: Scrape -> Load -> dbt -> YOLO
    scraped = scrape_telegram()
    loaded = load_to_postgres(scraped)
    transformed = run_dbt_transformations(loaded)
    enriched = run_yolo_enrichment(transformed)

defs = Definitions(
    jobs=[medical_data_pipeline],
)