{{ config(materialized='table') }}

SELECT
    date,
    ticker,
    open,
    high,
    low,
    close,
    volume
FROM {{ ref('stg_stock_prices') }}
WHERE date IS NOT NULL
  AND ticker IS NOT NULL
