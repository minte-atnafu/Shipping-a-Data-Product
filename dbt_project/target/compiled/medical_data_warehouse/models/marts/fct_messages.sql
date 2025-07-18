

-- Joining staging data with dimensions to create fact table
SELECT
    s.message_id,  -- Unique message identifier
    c.channel_id,  -- Foreign key to dim_channels
    d.date AS message_date,  -- Foreign key to dim_dates
    s.message_text,  -- Message content
    s.has_image,  -- Image presence indicator
    COALESCE(LENGTH(s.message_text), 0) AS message_length,  -- Length of message text
    CASE
        WHEN s.message_text IS NULL THEN FALSE
        ELSE TRUE
    END AS has_text,  -- Indicator for non-empty text
    COALESCE(
        NULLIF(
            REGEXP_REPLACE(
                s.message_text,
                '^\s*(?:[\*\s]*)(.*?)(?:\s*(?:Price|\n|$)).*',
                '\1',
                'i'
            ),
            ''
        ),
        'Unknown'
    ) AS product_name  -- Extracted product name
FROM "medical_data"."public_staging"."stg_telegram_messages" s
JOIN "medical_data"."public_marts"."dim_channels" c
    ON s.channel_name = c.channel_name
JOIN "medical_data"."public_marts"."dim_dates" d
    ON DATE(s.message_date) = d.date
WHERE s.message_date IS NOT NULL  -- Ensure valid dates