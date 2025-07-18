

SELECT DISTINCT
    channel_name,
    ROW_NUMBER() OVER () AS channel_id
FROM "medical_data"."public_staging"."stg_telegram_messages"