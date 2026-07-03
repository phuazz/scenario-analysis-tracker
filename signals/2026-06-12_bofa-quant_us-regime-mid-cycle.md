---
id: 2026-06-12_bofa-quant_us-regime-mid-cycle
signal_date: 2026-06-12
source: BofA US Equity & Quant Strategy
signal_name: US Regime Indicator confirms Mid Cycle (May 2026, second consecutive month)
asset:
  ticker: SPHB
  name: Invesco S&P 500 High Beta ETF — our proxy for the favoured High Risk factor
  wrapper_ticker: SPY
  wrapper_note: Relative leg — the published claim is factor leadership versus the market; judge SPHB minus SPY, not SPHB alone
  price_at_signal: 148.73
preferred_horizon: 1Y
sample_size: 9
lookback_start: 1990-01-01
forward_returns: {}
context:
  dist_from_60d_high_pct: -2.9
  trailing_60d_return_pct: 25.1
  vol_regime: elevated (SPHB 20d realised 38.5% vs 23.9% 1y average)
  entry_point_descriptor: neutral (outside both the 2% post-rally and 7% post-drawdown bands)
credibility_score:
  sample_size: 0
  t_stat: 0
  tail_asymmetry: 0
  entry_point: 1
  recent_performance: 0
  total: 1
  action: ignore
status: active
---

# Notes

Factual attribution of a published regime read. BofA's US Regime Indicator
advanced further in May 2026, confirming Mid Cycle on the second consecutive
month (their confirmation rule). Mid Cycle is defined as above-average and
improving macro trends; the styles they report as historically favoured in
this phase are Value, Momentum, Growth, High Risk, Low Quality and Small Size,
with High Risk and Low Quality the most consistent (89% hit rate each since
1990).

Source: BofA Global Research, Quantitative Primer (17th ed.), 12 June 2026,
pp. 81–83 (Exhibits 199–200). Signal date is the publication date; the
underlying reading is the May 2026 observation.

**Tracking construct (ours, not BofA's):** the published claim is
cross-sectional factor leadership over a phase, not a single-instrument price
path. SPHB is our chosen proxy for the High Risk factor (their most consistent
Mid-Cycle leader), judged relative to SPY. `forward_returns` is deliberately
empty: the published statistics are per-phase returns relative to the
equal-weight S&P 500, not fixed-horizon absolute returns, so mapping them into
the horizon table would manufacture false precision. The dashboard will show
mark-to-market only; evaluate manually at maturation as SPHB minus SPY.

**Data flags:** sample size of 9 Mid-Cycle instances since 1990 is inferred
from the hit-rate granularity (89% ≈ 8/9), not stated directly. The 1Y
preferred horizon is our approximation of a typical phase length. All
underlying performance figures are hypothetical, gross-of-cost, US
single-stock backtests.

**Compliance note:** the indicator is BofA-proprietary and explicitly
indicative-only (not for third-party reliance). This entry is a one-line
factual attribution of a dated regime read, logged for provider track record.
No reproduction of source exhibits.

## Credibility gate

| Input | Score | Rationale |
|---|---|---|
| Sample size | 0 | ~9 Mid-Cycle phase instances since 1990 — below 30 |
| T-stat at 1Y | 0 | Not published for phase-conditional factor returns |
| Tail asymmetry at 1Y | 0 | Not published |
| Entry-point fit | 1 | SPHB −2.9% from 60d high after a +25.1% 60d run — neutral by the rubric, though the run argues caution |
| Recent performance (last 5) | 0 | Not published; no per-instance history disclosed |
| **Total** | **1** | Below action threshold of 7 |

## Decision

Log only. No position-sizing authority. Kill condition: set status to
`killed` if BofA's published read moves to Late Cycle or Downturn before
maturation. The productive use of this entry is the track record — does the
Mid-Cycle factor map (High Beta over market) actually pay from a dated,
public, ex-ante read?
