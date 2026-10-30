WITH selected_batch AS (
    SELECT *
    FROM {{ source('olist_raw', 'orders') }}
    WHERE batch_id = '{{ var("orders_batch_id") }}'::uuid
)

SELECT
    batch_id,
    source_row_number,
    source_file,
    loaded_at,

    NULLIF(BTRIM(order_id), '') AS order_id,
    NULLIF(BTRIM(customer_id), '') AS customer_id,
    NULLIF(BTRIM(order_status), '') AS order_status,

    CAST(
        NULLIF(BTRIM(order_purchase_timestamp), '')
        AS timestamp without time zone
    ) AS purchased_at,

    CAST(
        NULLIF(BTRIM(order_approved_at), '')
        AS timestamp without time zone
    ) AS approved_at,

    CAST(
        NULLIF(BTRIM(order_delivered_carrier_date), '')
        AS timestamp without time zone
    ) AS handed_to_carrier_at,

    CAST(
        NULLIF(BTRIM(order_delivered_customer_date), '')
        AS timestamp without time zone
    ) AS delivered_at,

    CAST(
        NULLIF(BTRIM(order_estimated_delivery_date), '')
        AS timestamp without time zone
    ) AS estimated_delivery_at

FROM selected_batch
