from dagster import job
from dagster_pipeline.ops import (
    scrape_telegram_data,
    load_raw_to_postgres,
    run_dbt_transformations
    # run_yolo_enrichment  # not yet implemented
)

@job
def telegram_pipeline_job():
    scrape_telegram_data()
    load_raw_to_postgres()
    run_dbt_transformations()
    # run_yolo_enrichment()
