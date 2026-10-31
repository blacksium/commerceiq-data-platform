SELECT
    o.order_id,
    o.customer_id
FROM {{ ref('stg_orders') }} AS o
WHERE NOT EXISTS (
    SELECT 1
    FROM {{ ref('stg_customers') }} AS c
    WHERE c.customer_id = o.customer_id
)
