WITH registered_batch AS (
    SELECT batch_id, row_count
    FROM {{ source('olist_raw', 'load_batches') }}
    WHERE source_name = 'olist_orders'
      AND batch_id = '{{ var("orders_batch_id") }}'::uuid
),

model_count AS (
    SELECT COUNT(*) AS actual_count
    FROM {{ ref('stg_orders') }}
)

SELECT
    'Selected batch is missing or its row count does not match'
        AS failure_reason
FROM model_count AS m
LEFT JOIN registered_batch AS b ON TRUE
WHERE b.batch_id IS NULL
   OR b.row_count <= 0
   OR m.actual_count <> b.row_count
