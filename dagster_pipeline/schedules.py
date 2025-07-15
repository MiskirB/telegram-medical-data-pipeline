# dagster_pipeline/schedules.py

from dagster import schedule
from dagster_pipeline.jobs import telegram_pipeline_job

@schedule(cron_schedule="0 9 * * *", job=telegram_pipeline_job, execution_timezone="Africa/Nairobi")
def daily_scrape_schedule():
    return {}
