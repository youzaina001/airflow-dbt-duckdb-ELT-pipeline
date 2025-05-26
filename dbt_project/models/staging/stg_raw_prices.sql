-- models/staging/stg_raw_prices.sql
SELECT
    CAST("timestamp" AS TIMESTAMP) AS price_timestamp, -- Assuming your raw column is named "timestamp"
    CAST(price AS DOUBLE) AS price_value,
    LOWER(TRIM(coin_id)) AS coin_id
FROM {{ source('raw_data_source', 'raw_crypto_prices') }}