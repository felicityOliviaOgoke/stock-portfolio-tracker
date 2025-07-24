{{ config(materialized='table') }}

SELECT
    date,
    open,
    high,
    low,
    close,
    volume,
    ticker
FROM raw_stock_prices
WHERE ticker IS NOT NULL
