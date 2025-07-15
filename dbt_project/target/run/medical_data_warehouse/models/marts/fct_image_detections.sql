
  
    

  create  table "medical_data"."public"."fct_image_detections__dbt_tmp"
  
  
    as
  
  (
    

SELECT 
    id,
    message_id,
    detected_object_class,
    confidence_score
FROM "medical_data"."public"."image_detections"
  );
  