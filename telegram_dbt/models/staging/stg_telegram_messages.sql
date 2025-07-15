-- models/staging/stg_telegram_messages.sql

with source as (
    select * from {{ source('public', 'raw_telegram_messages') }}
),

renamed as (
    select
        id as message_id,
        message_date,
        text,
        has_media,
        channel,
        image_path
    from source
)

select * from renamed
