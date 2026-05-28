"""
fetch_prices.py — pull daily close history for every ticker referenced in
signals/. Uses Stooq (free, no API key) as primary source.

Usage: python scripts/fetch_prices.py
Output: data/prices.json  ({ticker: {iso_date: close_price}})

Note: ticker symbols may need adjustment per Stooq conventions. The mapping
below handles common cases; extend as needed.
"""
import json
import sys
from datetime import date, timedelta
from pathlib import Path
from urllib.request import urlopen, Request

ROOT = Path(__file__).resolve().parent.parent
SIGNALS_FILE = ROOT / "data" / "signals.json"
OUT_FILE = ROOT / "data" / "prices.json"

# Ticker → Stooq symbol mapping. Stooq uses lowercase, sometimes with suffix.
STOOQ_MAP = {
    "STOXX": "^stoxx",       # STOXX Europe 600 — verify on Stooq before relying
    "EZU": "ezu.us",
    "VGK": "vgk.us",
    "SPX": "^spx",
    "SPY": "spy.us",
    "QQQ": "qqq.us",
    "BTC": "btcusd",
    "ETH": "ethusd",
}


def fetch_stooq(symbol: str, years: int = 3) -> dict:
    """Fetch daily close history from Stooq CSV endpoint."""
    url = f"https://stooq.com/q/d/l/?s={symbol}&i=d"
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urlopen(req, timeout=20) as r:
            raw = r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"  fetch failed for {symbol}: {e}")
        return {}

    out = {}
    cutoff = (date.today() - timedelta(days=365 * years)).isoformat()
    for i, line in enumerate(raw.strip().split("\n")):
        if i == 0:
            continue  # header
        parts = line.split(",")
        if len(parts) < 5:
            continue
        d, _, _, _, close = parts[0], parts[1], parts[2], parts[3], parts[4]
        if d < cutoff:
            continue
        try:
            out[d] = float(close)
        except ValueError:
            continue
    return out


def main():
    if not SIGNALS_FILE.exists():
        print(f"ERROR: {SIGNALS_FILE} not found. Run parse_signals.py first.")
        sys.exit(1)

    signals = json.loads(SIGNALS_FILE.read_text(encoding="utf-8"))
    tickers = sorted({s.get("asset", {}).get("ticker")
                      for s in signals if s.get("asset", {}).get("ticker")})

    existing = {}
    if OUT_FILE.exists():
        existing = json.loads(OUT_FILE.read_text(encoding="utf-8"))

    for t in tickers:
        symbol = STOOQ_MAP.get(t)
        if not symbol:
            print(f"  no Stooq mapping for {t} — skipping (add to STOOQ_MAP)")
            continue
        print(f"  fetching {t} ({symbol})...")
        prices = fetch_stooq(symbol)
        if prices:
            existing[t] = prices
            print(f"    got {len(prices)} daily closes")
        else:
            print(f"    no data returned")

    OUT_FILE.write_text(json.dumps(existing, indent=2), encoding="utf-8")
    print(f"\nWrote {OUT_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
