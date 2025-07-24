# scripts/load_to_postgres.py
import os
import pandas as pd
from sqlalchemy import create_engine, text, MetaData, Table
from dotenv import load_dotenv
from sqlalchemy.dialects.postgresql import insert as pg_insert
import psycopg2
# Load environment variables
load_dotenv()

DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")

# SQLAlchemy connection string
engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Folder where your CSVs live
RAW_DIR = os.path.join("..", "data", "raw")

# Create table once with PRIMARY KEY
def create_table_if_not_exists():
    create_sql = """
    CREATE TABLE IF NOT EXISTS raw_stock_prices (
        date DATE NOT NULL,
        open FLOAT,
        high FLOAT,
        low FLOAT,
        close FLOAT,
        volume BIGINT,
        ticker TEXT NOT NULL,
        PRIMARY KEY (ticker, date)
    );
    """
    with engine.begin() as conn:
        conn.execute(text(create_sql))

# Insert with upsert (do nothing on conflict)
def upsert_data(df):
    df.columns = [c.lower().replace(" ", "_") for c in df.columns]

    # Select only columns that match the table schema
    expected_cols = [
        "date", "open", "high", "low", "close",
        "volume", "ticker"
    ]

    missing = [col for col in expected_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    df = df[[col for col in expected_cols if col in df.columns]]

    metadata = MetaData()
    metadata.reflect(bind=engine)
    stock_prices = Table("raw_stock_prices", metadata, autoload_with=engine)

    records = df.to_dict(orient="records")

    with engine.begin() as conn:
        stmt = pg_insert(stock_prices).values(records)
        stmt = stmt.on_conflict_do_nothing(index_elements=["ticker", "date"])
        conn.execute(stmt)


# Load CSVs into PostgreSQL
def load_csv():
    for file in os.listdir(RAW_DIR):
        if file.endswith(".csv"):
            ticker = file.replace(".csv", "")
            print(f"loading {ticker}...")
            df = pd.read_csv(os.path.join(RAW_DIR, file))
            df["ticker"] = ticker
            upsert_data(df)
            print(f"{ticker} done")
def main():
    create_table_if_not_exists()
    load_csv()
    print("data loaded with deduplication.")


if __name__ == "__main__":
    main()