---
id: 2026-05-22_sentimentrader_euro-breadth-thrust
signal_date: 2026-05-22
source: SentimenTrader
signal_name: European 10-day breadth thrust (<25 to >75 in 21D)
asset:
  ticker: STOXX
  name: STOXX Europe 600 Price Index (EUR)
  wrapper_ticker: EZU
  wrapper_note: iShares MSCI Eurozone ETF as deployable proxy
  price_at_signal: 628.01
preferred_horizon: 4M
sample_size: 145
lookback_start: 2003-02-18
forward_returns:
  1M: {mean: 0.6, median: 1.7, pct_pos: 62, max_loss: -3.2, max_gain: 3.0, t_stat: 2.8}
  2M: {mean: 0.7, median: 1.8, pct_pos: 59, max_loss: -4.8, max_gain: 4.5, t_stat: 1.7}
  3M: {mean: 0.9, median: 1.9, pct_pos: 65, max_loss: -6.0, max_gain: 5.7, t_stat: 1.3}
  4M: {mean: 2.1, median: 3.8, pct_pos: 66, max_loss: -6.7, max_gain: 6.8, t_stat: 2.2}
  5M: {mean: 2.6, median: 4.5, pct_pos: 69, max_loss: -7.5, max_gain: 7.8, t_stat: 2.1}
  6M: {mean: 3.3, median: 4.9, pct_pos: 68, max_loss: -8.0, max_gain: 8.8, t_stat: 1.7}
  1Y: {mean: 6.2, median: 10.0, pct_pos: 70, max_loss: -11.0, max_gain: 14.2, t_stat: 2.6}
tail_count_10pct:
  1M: {neg: 11, pos: 1}
  2M: {neg: 20, pos: 10}
  3M: {neg: 29, pos: 19}
  4M: {neg: 35, pos: 30}
  5M: {neg: 42, pos: 42}
  6M: {neg: 43, pos: 53}
  1Y: {neg: 56, pos: 95}
context:
  dist_from_60d_high_pct: -1.1
  trailing_60d_return_pct: 8.4
  vol_regime: normal
  entry_point_descriptor: post-rally near highs
credibility_score:
  sample_size: 2
  t_stat: 1
  tail_asymmetry: 0
  entry_point: 0
  recent_performance: 1
  total: 4
  action: ignore
status: active
---

# Notes

Short-term breadth aggregate across FTSE / CAC / DAX / SMI surged from below
25 percent to above 75 percent within 21 days. Aggregate metric sits at 76.5
and continues to trend higher at signal time.

Author flags 1 to 3 month win rates as "passable" (62 to 65 percent positive)
but acknowledges average returns fail to compound meaningfully and tail
asymmetry is materially unfavourable in the near term (11:1 against at 1M,
1.5:1 against at 3M).

Where the signal pays off: 4M to 1Y, where median returns climb to 3.8 to 10.0
percent and tail asymmetry flips favourable from 5M onward.

## Credibility gate

| Input | Score | Rationale |
|---|---|---|
| Sample size | 2 | 145 signals over 23 years |
| T-stat at 4M | 1 | 2.2 — meaningful but not exceptional |
| Tail asymmetry at 4M | 0 | 35 negative vs 30 positive — slightly unfavourable |
| Entry-point fit | 0 | Signal fires post-rally, STOXX 600 near recent highs |
| Recent performance (last 5) | 1 | 2024-07-11 negative, 2024-08-14 positive, 2024-10-18 negative, 2025-01-16 mixed, 2025-04-15 strong |
| **Total** | **4** | Below action threshold of 7 |

## Decision

Log and monitor only. Do not deploy fresh capital. Watch for next thrust event
that fires from a drawdown of greater than 7 percent from 60-day high — that
is the historically productive subset that this conditional context check
would flag.
