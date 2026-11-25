import pandas as pd
import os
import sys

FILE = "data/raw/xptusdt_15m.csv"

def main():
    if not os.path.exists(FILE):
        print(f"ERROR: Data file not found: {FILE}")
        sys.exit(1)

    df = pd.read_csv(FILE)

    required = ["timestamp", "open", "high", "low", "close", "volume"]
    missing = [c for c in required if c not in df.columns]

    if missing:
        print("ERROR: Missing columns:", missing)
        sys.exit(1)

    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    numeric = ["open", "high", "low", "close", "volume"]

    for col in numeric:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    print("\nPLATINUM DATA VALIDATION")
    print("=" * 50)

    print(f"Rows: {len(df):,}")
    print(f"First: {df['timestamp'].min()}")
    print(f"Last:  {df['timestamp'].max()}")

    duplicates = df["timestamp"].duplicated().sum()
    print(f"Duplicate timestamps: {duplicates}")

    missing_values = df[required].isna().sum()
    print("\nMissing values:")
    print(missing_values.to_string())

    invalid_ohlc = (
        (df["high"] < df["low"]) |
        (df["high"] < df["open"]) |
        (df["high"] < df["close"]) |
        (df["low"] > df["open"]) |
        (df["low"] > df["close"]) |
        (df["open"] <= 0) |
        (df["high"] <= 0) |
        (df["low"] <= 0) |
        (df["close"] <= 0) |
        (df["volume"] < 0)
    )

    print(f"\nInvalid OHLCV rows: {invalid_ohlc.sum()}")

    df = df.sort_values("timestamp")
    gaps = df["timestamp"].diff()
    gap_rows = gaps[gaps != pd.Timedelta(minutes=15)].dropna()

    print(f"15-minute continuity breaks: {len(gap_rows)}")

    if len(gap_rows):
        print("\nFirst 10 gap timestamps:")
        print(df.loc[gap_rows.index, "timestamp"].head(10).to_string(index=False))

    print("\nIntegrity verdict:")
    if duplicates or missing_values.sum() or invalid_ohlc.sum():
        print("FAIL — Data requires correction.")
    else:
        print("BASIC PASS — Check gaps and coverage before backtesting.")

if __name__ == "__main__":
    main()
