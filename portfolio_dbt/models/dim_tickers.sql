--models/dim_tickers.sql
select distinct
ticker 
from {{ref('stg_stock_prices')}}