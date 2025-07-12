{{ config(materialized='view') }}

SELECT 
    message->>'id' AS message_id,
    (message->>'date')::timestamp AS message_date,
    message->>'text' AS message_text,
    (message->>'has_image')::boolean AS has_image,
    channel_name
FROM {{ source('raw', 'telegram_messages') }}