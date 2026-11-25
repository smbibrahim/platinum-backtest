import ccxt
import json

exchange = ccxt.binanceusdm({"enableRateLimit": True})

print("Loading Binance USD-M Futures markets...")
markets = exchange.load_markets()

matches = [
    m for m in markets.values()
    if "XPT" in m["symbol"].upper()
    or "PLATINUM" in m["symbol"].upper()
    or "XPT" in m.get("id", "").upper()
]

print("\nPLATINUM MARKET SEARCH")
print("=" * 60)

if not matches:
    print("No matching Platinum market found in Binance USD-M Futures.")
else:
    for m in matches:
        details = {
            "symbol": m.get("symbol"),
            "id": m.get("id"),
            "base": m.get("base"),
            "quote": m.get("quote"),
            "settle": m.get("settle"),
            "type": m.get("type"),
            "swap": m.get("swap"),
            "future": m.get("future"),
            "active": m.get("active"),
            "precision": m.get("precision"),
            "limits": m.get("limits")
        }
        print(json.dumps(details, indent=2))

    with open("config/platinum_market.json", "w") as f:
        json.dump(matches[0], f, indent=2, default=str)

    print("\nFirst matching market saved to config/platinum_market.json")
