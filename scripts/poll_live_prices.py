import yfinance as yf
import pandas as pd
import os
import time
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.dialects.postgresql import insert
from dotenv import load_dotenv
from logging_setup import log

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

# Config
TICKERS = ["AAPL", "MSFT", "GOOG"]
POLL_INTERVAL = 60  # seconds


def insert_ignore_conflicts(df, table_name):
    if df.empty:
        return

    metadata = MetaData()
    metadata.reflect(bind=engine)
    table = metadata.tables[table_name]

    rows = df.to_dict(orient="records")
    stmt = insert(table).values(rows)
    stmt = stmt.on_conflict_do_nothing(index_elements=["ticker", "timestamp"])

    with engine.begin() as conn:
        conn.execute(stmt)


def poll_and_insert():
    for ticker in TICKERS:
        try:
            df = yf.download(ticker, period="1d", interval="1m")
            if df.empty:
                print(f"No data for {ticker}")
                continue

            df = df.reset_index()

            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            if "Datetime" not in df.columns or "Close" not in df.columns:
                print(f"Missing required columns for {ticker}, skipping.")
                continue

            df = df[["Datetime", "Close"]].rename(columns={
                "Datetime": "timestamp",
                "Close": "price"
            })
            df["ticker"] = ticker
            df = df[["ticker", "timestamp", "price"]]

            # REMOVE already-inserted timestamps
            query = f"""
                SELECT timestamp FROM live_stock_prices 
                WHERE ticker = '{ticker}'
            """
            existing = pd.read_sql(query, engine)
            df = df[~df["timestamp"].isin(existing["timestamp"])]

            if df.empty:
                print(f"No new data for {ticker}")
                continue

            df.to_sql("live_stock_prices", engine, if_exists="append", index=False, method="multi")
            print(f"{ticker}: {len(df)} new rows inserted")

        except Exception as e:
            print(f"Error processing {ticker}: {e}")

    log(f"Polling completed at {pd.Timestamp.now()}")


if __name__ == "__main__":
    while True:
        poll_and_insert()
        time.sleep(POLL_INTERVAL)
