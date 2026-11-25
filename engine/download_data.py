import ccxt
import pandas as pd
import os
import sys
import time

SYMBOL = "XPT/USDT:USDT"
TIMEFRAME = "15m"
DATA_FILE = "data/raw/xptusdt_15m.csv"
START_DATE = "2020-01-01T00:00:00Z"

def main():
    exchange = ccxt.binanceusdm({
        "enableRateLimit": True
    })

    print(f"Fetching {SYMBOL} {TIMEFRAME} historical data...")
    since = exchange.parse8601(START_DATE)
    all_candles = []

    while True:
        try:
            candles = exchange.fetch_ohlcv(
                SYMBOL,
                timeframe=TIMEFRAME,
                since=since,
                limit=1000
            )

            if not candles:
                break

            all_candles.extend(candles)
            since = candles[-1][0] + 1

            print(f"Downloaded {len(all_candles)} candles...", end="\r")

            if len(candles) < 1000:
                break

        except Exception as e:
            print(f"\nDownload error: {e}")
            time.sleep(5)
            continue

    if not all_candles:
        raise RuntimeError("No candles downloaded. Verify symbol availability.")

    df = pd.DataFrame(
        all_candles,
        columns=["timestamp", "open", "high", "low", "close", "volume"]
    )

    df = df.drop_duplicates(subset="timestamp")
    df = df.sort_values("timestamp")
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)

    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    df.to_csv(DATA_FILE, index=False)

    print("\n\nDATA DOWNLOAD SUMMARY")
    print("-" * 40)
    print(f"Symbol: {SYMBOL}")
    print(f"Timeframe: {TIMEFRAME}")
    print(f"Candles: {len(df):,}")
    print(f"First candle: {df['timestamp'].min()}")
    print(f"Last candle: {df['timestamp'].max()}")
    print(f"Saved: {DATA_FILE}")

if __name__ == "__main__":
    main()
