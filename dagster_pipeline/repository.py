# dagster_pipeline/repository.py

from dagster import repository
from dagster_pipeline.jobs import telegram_pipeline_job
from dagster_pipeline.schedules import daily_scrape_schedule

@repository
def telegram_pipeline_repo():
    return [telegram_pipeline_job, daily_scrape_schedule]
