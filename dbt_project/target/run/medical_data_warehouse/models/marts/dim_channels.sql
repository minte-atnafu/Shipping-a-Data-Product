
  
    

  create  table "medical_data"."public_marts"."dim_channels__dbt_tmp"
  
  
    as
  
  (
    

SELECT DISTINCT
    channel_name,
    ROW_NUMBER() OVER () AS channel_id
FROM "medical_data"."public_staging"."stg_telegram_messages"
  );
  