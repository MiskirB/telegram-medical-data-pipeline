from dagster import op
import subprocess

@op
def scrape_telegram_data():
    subprocess.run(["python", "scraper/telegram_scraper.py"], check=True)
    return "scraped"

@op
def load_raw_to_postgres():
    subprocess.run(["python", "loader/load_json_to_postgres.py"], check=True)
    return "loaded"

@op
def run_dbt_transformations():
    subprocess.run(["dbt", "run", "--project-dir", "telegram_dbt"], check=True)
    return "dbt_done"

# Comment this out until you implement YOLO logic
# @op
# def run_yolo_enrichment():
#     subprocess.run(["python", "scripts/run_yolo.py"], check=True)
#     return "yolo_done"
