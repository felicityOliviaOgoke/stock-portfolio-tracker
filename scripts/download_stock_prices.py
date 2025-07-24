import yfinance as yf
import pandas as pd
import os
from datetime import datetime, timedelta

# Output path
RAW_DATA_DIR = os.path.join("..", "data", "raw")
os.makedirs(RAW_DATA_DIR, exist_ok=True)

# Tickers to fetch
TICKERS = ["AAPL", "GOOG", "MSFT", "AMZN", "TSLA"]

# Date range
END_DATE = datetime.today()
START_DATE = END_DATE - timedelta(days=730)  # 2 years

def download_data(ticker):
    try:
        print(f"Downloading {ticker}...")
        df = yf.download(ticker, start=START_DATE, end=END_DATE)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        if not df.empty:
            file_path = os.path.join(RAW_DATA_DIR, f"{ticker}.csv")
            df.to_csv(file_path)
            print(f"Saved {ticker} to {file_path}")
        else:
            print(f"No data for {ticker}")
    except Exception as e:
        print(f"Error downloading {ticker}: {e}")

def main():
    for ticker in TICKERS:
        download_data(ticker)

if __name__ == "__main__":
    main()
