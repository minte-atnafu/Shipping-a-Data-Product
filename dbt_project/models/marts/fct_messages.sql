{{ config(materialized='view') }}

SELECT 
    s.message_id,
    c.channel_id,
    d.date AS message_date,
    s.message_text,
    s.has_image,
    LENGTH(s.message_text) AS message_length
FROM {{ ref('stg_telegram_messages') }} s
JOIN {{ ref('dim_channels') }} c ON s.channel_name = c.channel_name
JOIN {{ ref('dim_dates') }} d ON DATE(s.message_date) = d.date