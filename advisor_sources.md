# Advisor Source Screening

Project: **Modelling Investor Irrationality**

This file records the source-selection stage for Task #2. Institutions are screened against the frozen rules in `advisor_methodology.md`. Selection is based on data structure and archive usability, not observed agreement with the cognitive model.

## Primary candidates

### 1. Charles Schwab — PASS

**Why it qualifies:** Schwab Center for Financial Research publishes a dated `Sector Views: Monthly Stock Sector Outlook` covering all 11 S&P 500/GICS sectors. Since March 2026 the ratings use a five-level scale: Most Favored, More Favored, Neutral, Less Favored, Least Favored. This maps directly to the frozen +2/+1/0/-1/-2 coding scheme.

**Initial snapshots located:**

- 2026-05-01 — all 11 sectors
- 2026-05-29 — all 11 sectors
- 2026-06-26 — all 11 sectors
- 2026-07-31 — all 11 sectors
- 2026-09-04 also exists and can be used later if needed

**Status:** selected for primary dataset.

### 2. Wells Fargo Investment Institute — PASS

**Why it qualifies:** Wells Fargo Investment Institute publishes explicit `Equity sector and sub-sector preferences` with sector-level tactical guidance across all 11 sectors. Labels include Most Favorable, Favorable, Neutral, and Unfavorable, which map cleanly to +2/+1/0/-1. Missing +2/-2 categories are not artificially created.

**Initial snapshots located:**

- 2024-12-10 — 2025 Outlook
- 2025-12-09 — 2026 Outlook
- 2026-03-16 — Asset Allocation Strategy Report
- 2026-06-16 — 2026 Midyear Outlook

**Status:** selected for primary dataset.

### 3. CFRA Research — PASS, collection incomplete

**Why it qualifies:** CFRA publishes quarterly `Sector Roundup` reports covering all 11 GICS sectors and uses explicit Overweight/Underweight sector recommendations. Public summaries confirm a Q1 2026 report and a Q2 2026 report. The Q1 summary explicitly identifies Financials and Information Technology as Overweight and Energy, Materials, and Real Estate as Underweight; the Q2 summary describes subsequent sector changes and continues full 11-sector coverage.

**Located:**

- 2026-04-13 — Sector Roundup: Q1 2026 Portfolio Positioning
- 2026-07-16 — Sector Roundup: Q2 2026 Portfolio Positioning

**Issue:** public landing pages do not expose the complete 11-sector rating table for every quarter; the full downloadable reports may be gated. We therefore do not code incomplete sector rows from summaries.

**Status:** selected provisionally; retain only if at least four eligible complete snapshots can be obtained without violating the frozen rules.

### 4. Morningstar — HOLD / backup candidate

Morningstar publishes frequent dated U.S. stock-market outlooks and a complete price/fair-value ranking by sector. It also provides explicit portfolio language in some periods (e.g. overweight/harvest/reallocate). However, its most systematic sector data are valuation ratios rather than a consistent categorical recommendation scale.

Using those ratios directly would require adding a new coding rule after the methodology was frozen. Therefore Morningstar is **not currently included in the primary categorical advisor dataset**. It may be useful as a robustness or continuous-ranking extension if that extension is documented separately.

## Candidates rejected from primary sample

### Morgan Stanley — REJECT for current design

The public 2026 Portfolio Solutions material screened here provides explicit regional and style allocations (e.g. U.S. overweight, cyclicals overweight) but not a complete 11-sector U.S. tactical rating table. Other Morgan Stanley commentary names favorite sectors, but that does not satisfy the minimum complete-sector requirement consistently.

**Reason for rejection:** insufficient comparable sector coverage in the public source located.

### Fidelity — REJECT for current design

Fidelity publishes extensive sector-fund manager commentary and portfolio over/underweights, but the material located is fund-specific rather than a single institution-wide 11-sector tactical recommendation framework. Combining different fund managers would change the unit of analysis and mix portfolio mandates.

**Reason for rejection:** no consistent institution-wide 11-sector stance series located in the initial screen.

## Current sample plan

Confirmed primary institutions:

1. Charles Schwab
2. Wells Fargo Investment Institute

Provisional third:

3. CFRA Research

Fourth institution remains **open** until a source with at least six sectors per dated snapshot and a repeatable categorical recommendation framework is verified. We will not weaken the frozen methodology merely to reach four institutions.

## Data already ready to code

Eight complete 11-sector snapshots have been located and can be coded immediately:

- Schwab: 4 snapshots × 11 sectors = 44 observations
- Wells Fargo: 4 snapshots × 11 sectors = 44 observations

**Initial verified dataset size: 88 institution-date-sector observations.**

The next collection step is to finish CFRA archive access and identify a fourth institution meeting the same standard.