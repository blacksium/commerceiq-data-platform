CREATE TABLE IF NOT EXISTS raw."order_items" (
    batch_id UUID NOT NULL,
    source_row_number BIGINT NOT NULL,
    source_file TEXT NOT NULL,
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    "order_id" TEXT,
    "order_item_id" TEXT,
    "product_id" TEXT,
    "seller_id" TEXT,
    "shipping_limit_date" TEXT,
    "price" TEXT,
    "freight_value" TEXT,

    PRIMARY KEY (batch_id, source_row_number),
    FOREIGN KEY (batch_id)
        REFERENCES raw.load_batches (batch_id),
    CHECK (source_row_number > 0)
);

CREATE TABLE IF NOT EXISTS raw."order_payments" (
    batch_id UUID NOT NULL,
    source_row_number BIGINT NOT NULL,
    source_file TEXT NOT NULL,
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    "order_id" TEXT,
    "payment_sequential" TEXT,
    "payment_type" TEXT,
    "payment_installments" TEXT,
    "payment_value" TEXT,

    PRIMARY KEY (batch_id, source_row_number),
    FOREIGN KEY (batch_id)
        REFERENCES raw.load_batches (batch_id),
    CHECK (source_row_number > 0)
);

CREATE TABLE IF NOT EXISTS raw."order_reviews" (
    batch_id UUID NOT NULL,
    source_row_number BIGINT NOT NULL,
    source_file TEXT NOT NULL,
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    "review_id" TEXT,
    "order_id" TEXT,
    "review_score" TEXT,
    "review_comment_title" TEXT,
    "review_comment_message" TEXT,
    "review_creation_date" TEXT,
    "review_answer_timestamp" TEXT,

    PRIMARY KEY (batch_id, source_row_number),
    FOREIGN KEY (batch_id)
        REFERENCES raw.load_batches (batch_id),
    CHECK (source_row_number > 0)
);

CREATE TABLE IF NOT EXISTS raw."products" (
    batch_id UUID NOT NULL,
    source_row_number BIGINT NOT NULL,
    source_file TEXT NOT NULL,
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    "product_id" TEXT,
    "product_category_name" TEXT,
    "product_name_lenght" TEXT,
    "product_description_lenght" TEXT,
    "product_photos_qty" TEXT,
    "product_weight_g" TEXT,
    "product_length_cm" TEXT,
    "product_height_cm" TEXT,
    "product_width_cm" TEXT,

    PRIMARY KEY (batch_id, source_row_number),
    FOREIGN KEY (batch_id)
        REFERENCES raw.load_batches (batch_id),
    CHECK (source_row_number > 0)
);

CREATE TABLE IF NOT EXISTS raw."sellers" (
    batch_id UUID NOT NULL,
    source_row_number BIGINT NOT NULL,
    source_file TEXT NOT NULL,
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    "seller_id" TEXT,
    "seller_zip_code_prefix" TEXT,
    "seller_city" TEXT,
    "seller_state" TEXT,

    PRIMARY KEY (batch_id, source_row_number),
    FOREIGN KEY (batch_id)
        REFERENCES raw.load_batches (batch_id),
    CHECK (source_row_number > 0)
);

CREATE TABLE IF NOT EXISTS raw."geolocation" (
    batch_id UUID NOT NULL,
    source_row_number BIGINT NOT NULL,
    source_file TEXT NOT NULL,
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    "geolocation_zip_code_prefix" TEXT,
    "geolocation_lat" TEXT,
    "geolocation_lng" TEXT,
    "geolocation_city" TEXT,
    "geolocation_state" TEXT,

    PRIMARY KEY (batch_id, source_row_number),
    FOREIGN KEY (batch_id)
        REFERENCES raw.load_batches (batch_id),
    CHECK (source_row_number > 0)
);

CREATE TABLE IF NOT EXISTS raw."category_translation" (
    batch_id UUID NOT NULL,
    source_row_number BIGINT NOT NULL,
    source_file TEXT NOT NULL,
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    "product_category_name" TEXT,
    "product_category_name_english" TEXT,

    PRIMARY KEY (batch_id, source_row_number),
    FOREIGN KEY (batch_id)
        REFERENCES raw.load_batches (batch_id),
    CHECK (source_row_number > 0)
);
