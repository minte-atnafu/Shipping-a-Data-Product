
  create view "medical_data"."public"."fct_messages__dbt_tmp"
    
    
  as (
    


SELECT 
    s.message_id,
    c.channel_id,
    d.date AS message_date,
    s.message_text,
    s.has_image,
    LENGTH(s.message_text) AS message_length
FROM "medical_data"."public"."stg_telegram_messages" s
JOIN "medical_data"."public"."dim_channels" c ON s.channel_name = c.channel_name
JOIN "medical_data"."public"."dim_dates" d ON DATE(s.message_date) = d.date
  );