

SELECT 
    generate_series('2023-01-01'::date, current_date, '1 day'::interval) AS date,
    EXTRACT(YEAR FROM generate_series) AS year,
    EXTRACT(MONTH FROM generate_series) AS month,
    EXTRACT(DAY FROM generate_series) AS day
FROM generate_series('2023-01-01'::date, current_date, '1 day'::interval)