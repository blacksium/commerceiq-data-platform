WITH registered_batch AS (
    SELECT batch_id, row_count
    FROM {{ source('olist_raw', 'load_batches') }}
    WHERE source_name = 'olist_customers'
      AND batch_id = '{{ var("customers_batch_id") }}'::uuid
),

model_count AS (
    SELECT COUNT(*) AS actual_count
    FROM {{ ref('stg_customers') }}
)

SELECT
    'Selected customer batch is missing or its count does not match'
        AS failure_reason
FROM model_count AS m
LEFT JOIN registered_batch AS b ON TRUE
WHERE b.batch_id IS NULL
   OR b.row_count <= 0
   OR m.actual_count <> b.row_count
