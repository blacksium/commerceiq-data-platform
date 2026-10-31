SELECT
    customer_id,
    customer_zip_code_prefix,
    customer_state
FROM {{ ref('stg_customers') }}
WHERE customer_zip_code_prefix IS NULL
   OR customer_zip_code_prefix !~ '^[0-9]{5}$'
   OR customer_state IS NULL
   OR customer_state !~ '^[A-Z]{2}$'
