-- models/marts/daily_candlestick.sql
WITH source_data AS (
    SELECT
        price_timestamp,
        price_value,
        coin_id
    FROM {{ ref('stg_raw_prices') }} -- This refers to the staging model above
),

aggregated_by_day AS (
    SELECT
        DATE_TRUNC('day', price_timestamp) AS trade_date,
        coin_id,
        price_value,
        -- Get the first price of the day for opening price
        ROW_NUMBER() OVER (PARTITION BY coin_id, DATE_TRUNC('day', price_timestamp) ORDER BY price_timestamp ASC) as rn_asc,
        -- Get the last price of the day for closing price
        ROW_NUMBER() OVER (PARTITION BY coin_id, DATE_TRUNC('day', price_timestamp) ORDER BY price_timestamp DESC) as rn_desc
    FROM source_data
)

SELECT
    trade_date,
    coin_id,
    MAX(CASE WHEN rn_asc = 1 THEN price_value END) AS opening_price,
    MAX(CASE WHEN rn_desc = 1 THEN price_value END) AS closing_price,
    MIN(price_value) AS minimum_price,
    MAX(price_value) AS maximum_price
FROM aggregated_by_day
GROUP BY 1, 2 -- Group by trade_date and coin_id
ORDER BY trade_date DESC, coin_id