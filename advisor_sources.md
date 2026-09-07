# Advisor Source Screening

Project: **Modelling Investor Irrationality**

This file records the source-selection stage for Task #2. Institutions were screened against `advisor_methodology.md`. The primary sample is now frozen at two institutions as a small-sample comparative case study.

## Primary sample — FROZEN

### 1. Charles Schwab — INCLUDED

Schwab Center for Financial Research publishes a dated `Sector Views: Monthly Stock Sector Outlook` covering all 11 S&P 500/GICS sectors. Since March 2026 the ratings use a five-level scale: Most Favored, More Favored, Neutral, Less Favored, Least Favored. This maps directly to the frozen +2/+1/0/-1/-2 coding scheme.

**Primary snapshots:**

- 2026-05-01 — all 11 sectors
- 2026-05-29 — all 11 sectors
- 2026-06-26 — all 11 sectors
- 2026-07-31 — all 11 sectors

**Primary observations:** 44.

### 2. Wells Fargo Investment Institute — INCLUDED

Wells Fargo Investment Institute publishes explicit `Equity sector and sub-sector preferences` with sector-level tactical guidance across all 11 sectors. Labels include Most Favorable, Favorable, Neutral, and Unfavorable, which map cleanly to +2/+1/0/-1. Missing +2/-2 categories are not artificially created.

**Primary snapshots:**

- 2024-12-10 — 2025 Outlook
- 2025-12-09 — 2026 Outlook
- 2026-03-16 — Asset Allocation Strategy Report
- 2026-06-16 — 2026 Midyear Outlook

**Primary observations:** 44.

## Frozen primary dataset

- **2 institutions**
- **4 snapshots per institution**
- **8 advisor snapshots total**
- **11 sectors per snapshot**
- **88 institution-date-sector observations**

This is intentionally a comparative case study. The sample should not be described as representative of the financial-advisory industry.

## Institutions screened but not included in the primary sample

### CFRA Research — future extension

CFRA publishes quarterly `Sector Roundup` reports covering all 11 GICS sectors and uses explicit sector recommendations. It appeared methodologically promising, but complete historical rating tables were not consistently available through the public material screened. Because the primary two-institution dataset is sufficient for the symposium project, further CFRA collection is no longer required.

### Morningstar — future continuous-ranking extension

Morningstar publishes frequent dated U.S. market outlooks and systematic sector valuation rankings. However, its most consistent sector series is valuation-based rather than a categorical recommendation scale. Incorporating it would require a different coding framework, so it is excluded from the frozen primary dataset.

### Morgan Stanley — not included

The public material screened provided regional/style allocations and selected sector commentary but not a repeatable complete U.S. 11-sector tactical rating table suitable for the frozen framework.

### Fidelity — not included

The material screened was primarily fund- or manager-specific rather than a single institution-wide 11-sector tactical recommendation framework. Combining managers would change the unit of analysis and mix different portfolio mandates.

## Next analysis step

Advisor collection for the primary study is complete. The next step is to reconstruct the cognitive, classical, Momentum A, and Momentum B model stances at each of the eight publication dates using only information available on or before each date, then calculate:

1. Spearman rank correlation;
2. mean absolute rank distance (MARD);
3. top-three agreement;
4. bottom-three agreement;
5. institution-level and pooled summaries.

No additional institution is required for the primary analysis.