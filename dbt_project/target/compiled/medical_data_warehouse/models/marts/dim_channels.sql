

SELECT DISTINCT
    channel_name,
    ROW_NUMBER() OVER () AS channel_id
FROM "medical_data"."public"."stg_telegram_messages"