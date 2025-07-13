
  
    

  create  table "medical_data"."public"."dim_channels__dbt_tmp"
  
  
    as
  
  (
    

SELECT DISTINCT
    channel_name,
    ROW_NUMBER() OVER () AS channel_id
FROM "medical_data"."public"."stg_telegram_messages"
  );
  