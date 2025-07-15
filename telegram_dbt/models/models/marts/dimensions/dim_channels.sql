-- models/marts/dimensions/dim_channels.sql
{{ config(materialized='table') }}

SELECT DISTINCT
    channel AS channel_name
FROM {{ ref('stg_telegram_messages') }}
