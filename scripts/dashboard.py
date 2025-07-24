import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import plotly.express as px
import time
# Load environment variables
load_dotenv()

# DB connection
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)






st.set_page_config(
    page_title="Stock Monitor",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Real-Time Stock Monitoring Dashboard")

TICKERS = ["AAPL", "MSFT", "GOOG"]
selected_ticker = st.sidebar.selectbox("Select Ticker", TICKERS)

@st.cache_data(ttl=60)
def load_data(ticker):
    query = """
        SELECT ticker, timestamp, price
        FROM live_stock_prices
        WHERE ticker = %s
        ORDER BY timestamp DESC
        LIMIT 1000
    """
    df = pd.read_sql_query(query, engine, params=(ticker,))
    return df.sort_values("timestamp")

df = load_data(selected_ticker)

if df.empty:
    st.warning("No data available for this ticker.")
    st.stop()

# Show current price and stats
latest_price = df["price"].iloc[-1]
previous_price = df["price"].iloc[-2] if len(df) > 1 else latest_price
change = latest_price - previous_price
pct_change = (change / previous_price) * 100 if previous_price else 0

col1, col2, col3 = st.columns(3)
col1.metric("Latest Price", f"${latest_price:.2f}")
col2.metric("Change", f"${change:.2f}", delta_color="inverse")
col3.metric("Change %", f"{pct_change:.2f}%", delta_color="inverse")

# Price Line Chart
st.subheader(f"{selected_ticker} Intraday Price (1m Interval)")
fig = px.line(df, x="timestamp", y="price", title=f"{selected_ticker} Price", labels={"timestamp": "Time", "price": "Price ($)"})
fig.update_layout(height=400, margin=dict(l=20, r=20, t=30, b=20))
st.plotly_chart(fig, use_container_width=True)

# Data Table
st.subheader("Recent Data")
st.dataframe(df.tail(20), use_container_width=True)


time.sleep(60)
st.rerun()