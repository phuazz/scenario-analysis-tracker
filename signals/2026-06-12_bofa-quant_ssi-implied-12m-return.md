---
id: 2026-06-12_bofa-quant_ssi-implied-12m-return
signal_date: 2026-06-12
source: BofA US Equity & Quant Strategy
signal_name: Sell Side Indicator (May 2026 reading) implies ~+13% S&P 500 price return over 12M
asset:
  ticker: SPX
  name: S&P 500 Index
  wrapper_ticker: SPY
  wrapper_note: SPDR S&P 500 ETF as deployable proxy
  price_at_signal: 7431.46
preferred_horizon: 1Y
sample_size: 477
lookback_start: 1985-08-01
forward_returns:
  1Y: {mean: 13.0}
context:
  dist_from_60d_high_pct: -2.3
  trailing_60d_return_pct: 12.5
  vol_regime: normal
  entry_point_descriptor: neutral (just outside the 2% post-rally band after a +12.5% 60d run)
credibility_score:
  sample_size: 1
  t_stat: 1
  tail_asymmetry: 0
  entry_point: 1
  recent_performance: 0
  total: 3
  action: ignore
status: active
---

# Notes

Factual attribution of a published call. BofA's Sell Side Indicator — the
average recommended equity allocation of Wall Street strategists, tracked
monthly since August 1985 as a contrarian gauge — rose in May 2026 to its
highest level since February 2025, and at that level implies an S&P 500 price
return of approximately +13% over the following 12 months. The indicator sits
between its Buy and Sell thresholds, closer to Sell (1.9ppt away) than to Buy
(4.4ppt away).

Source: BofA Global Research, Quantitative Primer (17th ed.), 12 June 2026,
pp. 35–37. Signal date is the publication date; the underlying reading is the
May 2026 month-end observation.

**Data flag:** the source is internally inconsistent on the level — the text
cites 55.6% (and ties the +13% implied return to it) while Exhibit 68 shows
"Latest = 56.2%". Recorded expectation is therefore approximate. The +13% is a
regression-implied point estimate, not the mean of a discrete event study, so
no median, tails, or per-horizon table exists to log.

**Compliance note:** the indicator is BofA-proprietary and explicitly
indicative-only (not for third-party reliance). This entry is a one-line
factual attribution of a dated, falsifiable published call, logged to build
the provider-level track record. No reproduction of source exhibits.

## Credibility gate

| Input | Score | Rationale |
|---|---|---|
| Sample size | 1 | 477 monthly readings over ~40 years, but the 12M-forward regression uses overlapping windows — roughly 40 independent annual observations |
| T-stat at 1Y | 1 | Not published. R² of 25% (34% at Buy/Sell extremes) implies a healthy t on independent windows, but derived rather than published — capped at 1 |
| Tail asymmetry at 1Y | 0 | Not published |
| Entry-point fit | 1 | SPX −2.3% from 60d high — outside the 2% post-rally band, nowhere near the 7% drawdown band; trailing 60d +12.5% |
| Recent performance (last 5) | 0 | Not published; mid-range readings (neither extreme) are the indicator's weakest zone by its own R² split |
| **Total** | **3** | Below action threshold of 7 |

## Decision

Log only. No position-sizing authority. Purpose is to seed a BofA US Equity &
Quant Strategy provider track record in this tracker; evaluate at maturation
(June 2027) against the +13.0 mean via vs_mean — no max_loss/max_gain band
exists for this signal type. There is no ongoing BofA feed: this is a
point-in-time reference from a one-off primer, with no interim updates
expected before maturation.
