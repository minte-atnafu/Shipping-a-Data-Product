{{ config(materialized='table') }}

SELECT DISTINCT
    channel_name,
    ROW_NUMBER() OVER () AS channel_id
FROM {{ ref('stg_telegram_messages') }}