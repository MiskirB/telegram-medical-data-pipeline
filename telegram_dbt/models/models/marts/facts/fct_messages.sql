-- models/marts/facts/fct_messages.sql
{{ config(materialized='table') }}

SELECT
    m.message_id AS id,
    m.message_date,
    m.text,
    LENGTH(m.text) AS message_length,
    m.has_media,
    m.channel AS channel_name,
    d.date AS message_day,
    d.month_name,
    d.year
FROM {{ ref('stg_telegram_messages') }} m
LEFT JOIN {{ ref('dim_channels') }} c
    ON m.channel = c.channel_name
LEFT JOIN {{ ref('dim_dates') }} d
    ON m.message_date::date = d.date
