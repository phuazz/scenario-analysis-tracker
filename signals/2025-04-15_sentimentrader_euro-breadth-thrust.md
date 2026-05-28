---
id: 2025-04-15_sentimentrader_euro-breadth-thrust
signal_date: 2025-04-15
source: SentimenTrader
signal_name: European 10-day breadth thrust (<25 to >75 in 21D)
asset:
  ticker: STOXX
  name: STOXX Europe 600 Price Index (EUR)
  wrapper_ticker: EZU
  price_at_signal: 519.20
preferred_horizon: 4M
sample_size: 144
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
  3M: {neg: 29, pos: 19}
  6M: {neg: 43, pos: 53}
  1Y: {neg: 56, pos: 95}
context:
  dist_from_60d_high_pct: -8.5
  trailing_60d_return_pct: -4.2
  vol_regime: elevated
  entry_point_descriptor: post-drawdown thrust
credibility_score:
  sample_size: 2
  t_stat: 1
  tail_asymmetry: 1
  entry_point: 2
  recent_performance: 1
  total: 7
  action: act
status: matured

# Realised forward returns (from SentimenTrader 2025-04-15 row in the published table)
realised_returns:
  1M: 8.1
  2M: 7.6
  3M: 7.3
  4M: 8.4
  5M: 9.3
  6M: 11.0
  1Y: 20.8
---

# Notes

Historical example: April 2025 signal that scored well on the credibility gate
because it fired post-drawdown (STOXX 600 down ~8.5 percent from 60D high,
trailing 60D return negative) rather than post-rally. Forward returns came in
materially above mean at every horizon — a textbook case of the conditional
entry-point context flagging where the signal is most productive.

Compare directly with the 2026-05-22 instance, which scored 4/10 because it
fired near recent highs with positive trailing returns. The credibility gate
discriminates between the two even though the underlying signal mechanics are
identical.

This is the use case for the tracker: same signal, different context, very
different expected outcome.
