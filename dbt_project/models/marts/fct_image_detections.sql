{{ config(materialized='table') }}

SELECT 
    id,
    message_id,
    detected_object_class,
    confidence_score
FROM {{ source('public', 'image_detections') }}