WITH selected_batch AS (
    SELECT *
    FROM {{ source('olist_raw', 'customers') }}
    WHERE batch_id = '{{ var("customers_batch_id") }}'::uuid
)

SELECT
    batch_id,
    source_row_number,
    source_file,
    loaded_at,

    NULLIF(BTRIM(customer_id), '') AS customer_id,
    NULLIF(BTRIM(customer_unique_id), '') AS customer_unique_id,
    NULLIF(BTRIM(customer_zip_code_prefix), '')
        AS customer_zip_code_prefix,
    NULLIF(BTRIM(customer_city), '') AS customer_city,
    NULLIF(BTRIM(customer_state), '') AS customer_state

FROM selected_batch
