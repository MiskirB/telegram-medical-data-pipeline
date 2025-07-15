Final Report: End-to-End Telegram Data Pipeline for Medical Analytics

Project: Shipping a Data Product – Kara Solutions

Cohort: Nova July Week 7

Participant: Miskir Besir

Date: July 15, 2025

# Table of Contents

1. Project Overview

2. Task 1 – Telegram Scraper Implementation

3. Task 2 – Data Storage and Processing

4. Task 3 – DBT Modeling & Testing

5. Task 4 – Analytical API Development

6. Task 5 – Orchestration with Dagster

7. Challenges and Resolutions

8. Learnings and Takeaways

9. Future Work

10. Appendix: Tech Stack & Setup

# Project Overview

Kara Solutions aims to extract real-time analytics from public Telegram channels related to Ethiopian pharmaceutical and health-related commerce. This pipeline delivers insights like product trends, channel activity, and keyword searches through a fully orchestrated, testable, and scalable architecture using FastAPI, DBT, PostgreSQL, and Dagster.

# Task 1 – Telegram Scraper Implementation

Tools: telethon, json, dotenv

Scope:

- Scraped messages from ~20 curated Telegram channels.
- Saved JSON output structured as: message ID, timestamp, text, channel name, has_media, image_path.

Output: Files stored in data/raw/telegram_messages/YYYY-MM-DD/

Key Highlights:

- Handled pagination and duplicate messages.
- Resilient scraping with retry mechanisms and daily scheduling in mind.

# Task 2 – Data Storage and Processing

Storage: PostgreSQL table raw_telegram_messages

Loader Script: loader/load_json_to_postgres.py

Schema Fields:

- id, message_date, text, has_media, channel, image_path

Error Handling:

- Ensured ON CONFLICT DO NOTHING for safe upserts.
- Used .env for secure DB credentials.

# Task 3 – DBT Modeling & Testing

Staging Model: stg_telegram_messages.sql
Data Marts:

- dim_channels.sql
- dim_dates.sql
- fct_messages.sql

Enhancements:

- Message length, channel dimension join, date parsing

Tests: uniqueness, not-null, referential integrity

DBT CLI Output: 6 models built, 12 data tests, 11 passed

# Task 4 – Analytical API Development

Framework: FastAPI + SQLAlchemy

Endpoints:

- /api/reports/top-products?limit=10
- /api/channels/{channel_name}/activity
- /api/search/messages?query=paracetamol

Schemas: TopProduct, Message, ChannelActivity

Validations: Used Pydantic to define all outputs

Testing: Swagger UI at http://127.0.0.1:8001/docs

# Task 5 – Orchestration with Dagster

Ops Created:

- scrape_telegram_data()
- load_raw_to_postgres()
- run_dbt_transformations()
- run_yolo_enrichment() (placeholder)

Job: telegram_pipeline_job defined full execution graph

Repository: Exposed telegram_pipeline_repo() with schedule

UI: Dagster Webserver on http://127.0.0.1:3000

Schedule: Daily run configured in schedules.py

# Challenges and Resolutions

| Challenge                    | Solution                              |
| ---------------------------- | ------------------------------------- |
| PostgreSQL permission denied | Adjusted role privileges              |
| FastAPI path errors          | Cleaned imports and app instantiation |
| Dagster import issues        | Switched to absolute imports          |
| DBT model column mismatch    | Normalized field names                |

# Learnings and Takeaways

- Mastered FastAPI + Pydantic for data validation and endpoint structuring.
- Gained real-world experience in data modeling with DBT and semantic joins.
- Integrated Dagster orchestration, handling scheduling and job dependency graphs.
- Practiced debugging across PostgreSQL, Docker, subprocess, and FastAPI systems.

# Future Work

- Add tokenization + named entity recognition (NER) for deeper text insights.
- Store media content (images/videos) in S3 or equivalent.
- Build real-time dashboards with Superset or Streamlit.
- Extend Dagster to include alerting on scrape failures or data anomalies.

# Appendix: Tech Stack & Setup

| Component      | Stack                      |
| -------------- | -------------------------- |
| Scraper        | Python, Telethon           |
| Storage        | PostgreSQL (raw + modeled) |
| Transformation | DBT                        |
| API            | FastAPI, SQLAlchemy        |
| Orchestration  | Dagster                    |
| Deployment     | Local Dev, CLI             |
