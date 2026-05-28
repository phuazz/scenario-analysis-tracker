"""
build.py — combine parsed signals with price history, compute elapsed-time
horizons and actual returns, emit signals_compiled.json for the dashboard.

Usage: python scripts/build.py
Inputs: data/signals.json, data/prices.json (optional)
Output: data/signals_compiled.json, docs/index.html (injected build)
"""
import json
from datetime import date, datetime, timedelta
from pathlib import Path
from dateutil.relativedelta import relativedelta

ROOT = Path(__file__).resolve().parent.parent
SIGNALS_FILE = ROOT / "data" / "signals.json"
PRICES_FILE = ROOT / "data" / "prices.json"
TEMPLATE_FILE = ROOT / "template.html"
OUT_DATA = ROOT / "data" / "signals_compiled.json"
OUT_HTML = ROOT / "docs" / "index.html"

HORIZONS = [("1M", 1), ("2M", 2), ("3M", 3), ("4M", 4),
            ("5M", 5), ("6M", 6), ("1Y", 12)]


def add_months(d: date, months: int) -> date:
    """Add months using relativedelta to handle month/year boundaries safely."""
    return d + relativedelta(months=months)


def find_price_on_or_before(prices: dict, target: date):
    """Find the latest available price on or before target date."""
    if not prices:
        return None
    target_s = target.isoformat()
    # prices is {iso_date: price}; pick the largest key <= target
    eligible = [k for k in prices.keys() if k <= target_s]
    if not eligible:
        return None
    key = max(eligible)
    return {"date": key, "price": prices[key]}


def compute_actuals(signal: dict, prices: dict, today: date) -> dict:
    """For each horizon, compute the actual return if elapsed, else None."""
    signal_date = datetime.fromisoformat(signal["signal_date"]).date()
    price_at_signal = signal.get("asset", {}).get("price_at_signal")
    actuals = {}

    for label, months in HORIZONS:
        horizon_date = add_months(signal_date, months)
        elapsed = today >= horizon_date
        actual = {
            "horizon_date": horizon_date.isoformat(),
            "elapsed": elapsed,
            "actual_return_pct": None,
            "price_at_horizon": None,
            "current_return_pct": None,  # if not elapsed, show MTM
        }
        if not prices or price_at_signal is None:
            actuals[label] = actual
            continue

        if elapsed:
            p = find_price_on_or_before(prices, horizon_date)
            if p:
                actual["price_at_horizon"] = p["price"]
                actual["actual_return_pct"] = round(
                    (p["price"] / price_at_signal - 1) * 100, 2)
        else:
            # not yet elapsed — show current mark-to-market
            p = find_price_on_or_before(prices, today)
            if p:
                actual["current_return_pct"] = round(
                    (p["price"] / price_at_signal - 1) * 100, 2)

        actuals[label] = actual

    return actuals


def evaluate_signal(signal: dict, actuals: dict) -> dict:
    """Per-horizon evaluation: did actual land within max_loss/max_gain band?"""
    eval_out = {}
    fr = signal.get("forward_returns", {})
    for label, _ in HORIZONS:
        h_fr = fr.get(label, {})
        h_act = actuals.get(label, {})
        actual_pct = h_act.get("actual_return_pct")
        if actual_pct is None or not h_fr:
            eval_out[label] = {"status": "pending"}
            continue
        max_loss = h_fr.get("max_loss")
        max_gain = h_fr.get("max_gain")
        mean = h_fr.get("mean")
        in_band = (max_loss is not None and max_gain is not None
                   and max_loss <= actual_pct <= max_gain)
        eval_out[label] = {
            "status": "matured",
            "actual_pct": actual_pct,
            "vs_mean": round(actual_pct - mean, 2) if mean is not None else None,
            "in_band": in_band,
            "exceeded_max_gain": (max_gain is not None
                                  and actual_pct > max_gain),
            "breached_max_loss": (max_loss is not None
                                  and actual_pct < max_loss),
        }
    return eval_out


def main():
    if not SIGNALS_FILE.exists():
        print(f"ERROR: {SIGNALS_FILE} not found. Run parse_signals.py first.")
        return

    signals = json.loads(SIGNALS_FILE.read_text(encoding="utf-8"))

    # Load prices keyed by ticker; structure: {ticker: {iso_date: price}}
    all_prices = {}
    if PRICES_FILE.exists():
        all_prices = json.loads(PRICES_FILE.read_text(encoding="utf-8"))
    else:
        print(f"WARN: {PRICES_FILE} not found — actuals will be None.")

    today = date.today()
    compiled = []
    for sig in signals:
        ticker = sig.get("asset", {}).get("ticker")
        prices_for_ticker = all_prices.get(ticker, {})
        actuals = compute_actuals(sig, prices_for_ticker, today)
        evaluation = evaluate_signal(sig, actuals)
        compiled.append({
            **sig,
            "actuals": actuals,
            "evaluation": evaluation,
            "computed_at": today.isoformat(),
        })

    OUT_DATA.write_text(json.dumps(compiled, indent=2), encoding="utf-8")
    print(f"Wrote compiled data: {OUT_DATA.relative_to(ROOT)}")

    # Build dashboard: inject compiled JSON into template
    if TEMPLATE_FILE.exists():
        tpl = TEMPLATE_FILE.read_text(encoding="utf-8")
        injected = tpl.replace(
            "/*__SIGNALS_PLACEHOLDER__*/[]",
            json.dumps(compiled)
        )
        OUT_HTML.parent.mkdir(exist_ok=True)
        OUT_HTML.write_text(injected, encoding="utf-8")
        print(f"Wrote dashboard: {OUT_HTML.relative_to(ROOT)}")
    else:
        print(f"WARN: template.html not found, skipped dashboard build")


if __name__ == "__main__":
    main()
