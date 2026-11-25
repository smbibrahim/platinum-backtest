import pandas as pd
import os

FILE = "data/raw/xptusdt_15m.csv"
OUTPUT = "reports/data_audit.txt"

df = pd.read_csv(FILE)
df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
df = df.sort_values("timestamp").reset_index(drop=True)

df["date_utc"] = df["timestamp"].dt.date
daily = df.groupby("date_utc").size()

expected = 96  # 15-minute candles per 24-hour day

with open(OUTPUT, "w") as f:
    f.write("PLATINUM XPTUSDT DATA AUDIT\n")
    f.write("=" * 50 + "\n\n")
    f.write(f"Total candles: {len(df):,}\n")
    f.write(f"First timestamp: {df['timestamp'].min()}\n")
    f.write(f"Last timestamp: {df['timestamp'].max()}\n")
    f.write(f"Trading dates: {len(daily)}\n")
    f.write(f"Expected candles/day: {expected}\n\n")

    f.write("DAILY CANDLE COUNTS\n")
    f.write("-" * 50 + "\n")
    f.write(daily.to_string() + "\n\n")

    incomplete = daily[daily != expected]

    f.write("DAILY COVERAGE CHECK\n")
    f.write("-" * 50 + "\n")
    f.write(f"Days with exactly 96 candles: {(daily == expected).sum()}\n")
    f.write(f"Days with fewer/more than 96 candles: {len(incomplete)}\n\n")

    if len(incomplete):
        f.write("Non-standard days:\n")
        f.write(incomplete.to_string() + "\n")

print("\nPLATINUM DATA AUDIT")
print("=" * 50)
print(f"Total candles: {len(df):,}")
print(f"First: {df['timestamp'].min()}")
print(f"Last: {df['timestamp'].max()}")
print(f"Trading dates: {len(daily)}")
print(f"Full 96-candle days: {(daily == expected).sum()}")
print(f"Non-standard days: {len(incomplete)}")
print(f"Report: {OUTPUT}")

if len(incomplete):
    print("\nFirst 20 non-standard days:")
    print(incomplete.head(20).to_string())
