"""
fetch_prices.py — pull daily close history for every ticker referenced in
signals/. Uses Yahoo Finance via yfinance (free, no API key) as primary source.

Usage: python scripts/fetch_prices.py
Output: data/prices.json  ({ticker: {iso_date: close_price}})

Note: the prototype originally used Stooq, but Stooq now requires a per-user
API key behind a browser captcha. yfinance gives equivalent or better coverage
for indices and ETFs without any credential.

Ticker mapping below converts a project-internal symbol (used in the signal
markdown files) to the Yahoo Finance symbol. Extend YF_MAP as new assets land.
"""
import json
import sys
import warnings
from datetime import date
from pathlib import Path

# Silence yfinance's noisy FutureWarnings and informational prints
warnings.filterwarnings("ignore")

try:
    import yfinance as yf
except ImportError:
    print("ERROR: yfinance required. Install with: pip install yfinance")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
SIGNALS_FILE = ROOT / "data" / "signals.json"
OUT_FILE = ROOT / "data" / "prices.json"

# Project-internal ticker → Yahoo Finance symbol.
# Verify any new symbol returns data before relying on it.
YF_MAP = {
    "STOXX": "^STOXX",        # STOXX Europe 600 Price Index (EUR)
    "STOXX50": "^STOXX50E",   # EURO STOXX 50 Price Index (EUR)
    "EZU": "EZU",             # iShares MSCI Eurozone ETF (USD)
    "FEZ": "FEZ",             # SPDR EURO STOXX 50 ETF (USD)
    "VGK": "VGK",             # Vanguard FTSE Europe ETF (USD)
    "SPX": "^GSPC",           # S&P 500 Index
    "SPY": "SPY",             # SPDR S&P 500 ETF
    "SPHB": "SPHB",           # Invesco S&P 500 High Beta ETF
    "QQQ": "QQQ",             # Invesco QQQ Trust (Nasdaq 100)
    "BTC": "BTC-USD",         # Bitcoin USD
    "ETH": "ETH-USD",         # Ethereum USD
}

# How far back to fetch on each run. Three years comfortably covers a 1Y
# horizon plus context windows; extend if a signal looks further back.
HISTORY_YEARS = 3


def fetch_yfinance(symbol: str, years: int = HISTORY_YEARS) -> dict:
    """Fetch daily close history from Yahoo Finance.

    Returns {iso_date: close_price}. Empty dict on failure or no data.
    """
    try:
        df = yf.download(
            symbol,
            period=f"{years}y",
            progress=False,
            auto_adjust=False,
            threads=False,
        )
    except Exception as e:
        print(f"    fetch failed for {symbol}: {e}")
        return {}

    if df is None or df.empty:
        return {}

    # yfinance returns a MultiIndex column layout (Price, Ticker) for
    # single-symbol downloads in recent versions. Normalise to a flat Close series.
    if hasattr(df.columns, "levels"):
        try:
            closes = df["Close"][symbol]
        except (KeyError, ValueError):
            closes = df["Close"].iloc[:, 0]
    else:
        closes = df["Close"]

    out = {}
    for idx, value in closes.items():
        try:
            iso = idx.date().isoformat()
            out[iso] = round(float(value), 4)
        except (ValueError, TypeError):
            continue
    return out


def main():
    if not SIGNALS_FILE.exists():
        print(f"ERROR: {SIGNALS_FILE} not found. Run parse_signals.py first.")
        sys.exit(1)

    signals = json.loads(SIGNALS_FILE.read_text(encoding="utf-8"))
    tickers = sorted({s.get("asset", {}).get("ticker")
                      for s in signals if s.get("asset", {}).get("ticker")})

    # Also pull wrapper tickers if present — useful when the signal references
    # an index but the deployable instrument is an ETF.
    wrappers = sorted({s.get("asset", {}).get("wrapper_ticker")
                       for s in signals if s.get("asset", {}).get("wrapper_ticker")})
    all_symbols = sorted(set(tickers) | set(wrappers))

    # Merge into existing cache so a transient fetch failure does not wipe history.
    existing = {}
    if OUT_FILE.exists():
        try:
            existing = json.loads(OUT_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            existing = {}

    for t in all_symbols:
        symbol = YF_MAP.get(t)
        if not symbol:
            print(f"  no YF mapping for {t} — skipping (add to YF_MAP)")
            continue
        print(f"  fetching {t} ({symbol})...")
        prices = fetch_yfinance(symbol)
        if prices:
            # Merge new closes over existing — newest values win for the same date.
            existing[t] = {**existing.get(t, {}), **prices}
            print(f"    got {len(prices)} daily closes "
                  f"(total cached: {len(existing[t])})")
        else:
            print(f"    no data returned")

    OUT_FILE.parent.mkdir(exist_ok=True)
    OUT_FILE.write_text(json.dumps(existing, indent=2), encoding="utf-8")
    print(f"\nWrote {OUT_FILE.relative_to(ROOT)} "
          f"({sum(len(v) for v in existing.values())} closes across "
          f"{len(existing)} tickers)")


if __name__ == "__main__":
    main()
