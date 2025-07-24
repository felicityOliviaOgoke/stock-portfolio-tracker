{{ config(materialized='table') }}

WITH prices AS (
  SELECT * FROM {{ ref('fct_stock_prices') }}
),

returns AS (
  SELECT
    ticker,
    date,
    close,
    LAG(close) OVER (PARTITION BY ticker ORDER BY date) AS prev_close
  FROM prices
),

final AS (
  SELECT
    *,
    ROUND(
      ((close - prev_close) / NULLIF(prev_close, 0))::numeric,
      6
    ) AS daily_return
  FROM returns
  WHERE prev_close IS NOT NULL
)

SELECT * FROM final
