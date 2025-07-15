-- models/marts/dimensions/dim_dates.sql
{{ config(materialized='table') }}

WITH dates AS (
    SELECT generate_series(
        (SELECT MIN(message_date)::date FROM {{ ref('stg_telegram_messages') }}),
        (SELECT MAX(message_date)::date FROM {{ ref('stg_telegram_messages') }}),
        INTERVAL '1 day'
    ) AS date
)
SELECT
    date,
    EXTRACT(dow FROM date) AS day_of_week,
    TO_CHAR(date, 'Day') AS day_name,
    EXTRACT(week FROM date) AS week_num,
    EXTRACT(month FROM date) AS month_num,
    TO_CHAR(date, 'Month') AS month_name,
    EXTRACT(year FROM date) AS year
FROM dates
