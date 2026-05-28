# Signal Tracker

A personal database of scenario-analysis events — third-party research signals
and internal dashboard triggers — with credibility gating and actual-vs-expected
monitoring over time.

## Why this exists

Research providers (SentimenTrader, BCA, sell-side desks) publish "if X happens,
the historical forward returns are Y" tables regularly. These are useful but
hard to manage without structure: signals arrive, get read, get forgotten, and
the question of whether the provider's track record actually justifies attention
never gets answered systematically.

This tracker logs every signal as it arrives, scores its credibility, monitors
actual returns against the published expectation, and over time builds a
provider-level track record so you can tell which research streams have earned
acting authority.

## Architecture

```
signal-tracker/
├── signals/                  # markdown source files (one per signal)
├── data/
│   ├── prices.json           # daily closes per ticker (Stooq)
│   ├── signals.json          # parsed signals (from parse_signals.py)
│   └── signals_compiled.json # parsed + actuals (from build.py)
├── scripts/
│   ├── parse_signals.py      # markdown → signals.json
│   ├── fetch_prices.py       # Stooq → prices.json
│   └── build.py              # combine → signals_compiled.json + docs/index.html
├── template.html             # dashboard source (~14KB)
└── docs/index.html           # built dashboard (GitHub Pages)
```

## Workflow

### Logging a new signal

1. Create a new markdown file in `signals/`. Filename convention:
   `YYYY-MM-DD_source_short-name.md`
2. Fill in the YAML frontmatter using `signals/2026-05-22_sentimentrader_euro-breadth-thrust.md`
   as the template
3. Score the credibility gate (see rubric below)
4. Write a notes section with your decision rationale
5. Run the build pipeline:
   ```bash
   python scripts/parse_signals.py
   python scripts/fetch_prices.py     # only if new ticker
   python scripts/build.py
   ```
6. Open `docs/index.html` to verify

### Local development

```bash
npx serve .                   # standalone dev with fetch fallback
# or
npx serve docs                # test the built artifact
```

### GitHub Actions

The included workflow (`.github/workflows/update.yml` — to be added) runs daily
to refresh prices and rebuild the dashboard. No action needed once configured.

## Credibility gate rubric

Each signal is scored 0-2 on five dimensions, total 0-10:

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Sample size | <30 | 30-100 | >100 |
| T-stat at preferred horizon | <1.5 | 1.5-2.5 | >2.5 |
| Tail asymmetry at preferred horizon | unfavourable (more ±10% losses than gains) | even | favourable |
| Entry-point fit | post-rally near highs (within 2% of 60D high) | neutral | post-drawdown (>7% below 60D high) |
| Recent performance | last 5 instances mostly negative | mixed | mostly positive |

**Action thresholds:**
- 7-10: **act** — signal earns position-sizing authority
- 5-6: **monitor** — track actuals but no fresh capital
- 0-4: **ignore** — log only

The entry-point dimension is the most important one in this rubric. It encodes
the principle that the same signal fired from a drawdown is materially more
productive than from a rally. This is missing from most published signal
analyses and is the single highest-value extension over what providers ship.

## Variable preferred horizon

Each signal picks its own preferred horizon in the frontmatter. This matters
because some signals are inherently short-term (breadth thrusts pay off at
4-6M) while others are long-term (regime indicators at 1Y+). The credibility
gate scores against the preferred horizon, and the dashboard summary uses it
for the top-level expected-vs-actual comparison. All seven horizons (1M, 2M,
3M, 4M, 5M, 6M, 1Y) remain visible in the detail drawer.

## Status lifecycle

- **active** — signal is within its 1Y observation window
- **matured** — 1Y has elapsed; actuals fully observed; contributes to track
  record
- **killed** — signal invalidated by a follow-on event (e.g. opposite signal
  fires, regime breaks) before maturation. Set manually.

## Notes for operations

- Ticker mapping in `fetch_prices.py` (`STOOQ_MAP`) needs extension as new
  assets are added. Verify Stooq symbols before relying on data.
- Date arithmetic uses `python-dateutil` `relativedelta` to handle month and
  year boundaries cleanly — never compute month offsets manually.
- The dashboard template stays under 200KB so the file-size editing guardrails
  from the working specs apply only to `docs/index.html` (which is the built
  output and should not be edited directly).
- White / light theme by default.
- Add new credibility-gate dimensions cautiously. The five above are chosen
  to be (a) computable from published research and (b) genuinely additive.
  Adding more dilutes the signal.

## Future extensions

- Conditional backtest engine: for each signal type, separate published
  forward returns by entry-point context (post-rally vs post-drawdown) and
  produce a context-aware expected-return table. This would let the tracker
  show "expected at this context" instead of "expected on full sample".
- Source-level track record analytics: hit rate vs published expectation by
  research provider, regressed against time and signal type.
- Telegram or email notification when an active signal's actual return breaches
  its avg max loss or exceeds its avg max gain (early-signal-failure or
  early-signal-confirmation alerts).
