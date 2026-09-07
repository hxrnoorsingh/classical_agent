# Advisor Comparison Methodology

## Project

**Title:** *Modelling Investor Irrationality*

This document freezes the methodology for comparing professional sector recommendations with the project's computational investment agents before the advisor data are collected. Its purpose is to reduce researcher discretion and avoid changing the comparison rules after seeing which model performs best.

## 1. Research question

Can psychologically motivated features of investor decision-making—loss aversion, surprise, reference dependence through drawdown, and memory of past losses—produce sector preferences that more closely resemble professional investment advice than selected mechanical benchmarks?

The advisor comparison does **not** treat similarity to the cognitive agent as proof that an institution or analyst is irrational. A stronger similarity is interpreted as evidence that the published recommendation pattern is **more consistent with the behavioral mechanisms represented by the cognitive model** than with the selected benchmark models.

## 2. Main hypothesis

**H1:** Professional sector recommendations will, on average, exhibit greater rank similarity to the cognitive agent than to the classical volatility-targeting benchmark or the primary momentum benchmark.

Operationally, the primary expectation is:

- `rho(advisor, cognitive) > rho(advisor, classical)`
- `rho(advisor, cognitive) > rho(advisor, momentumA)`

Secondary evidence will come from mean absolute rank distance and top-/bottom-three agreement.

## 3. Unit of analysis

The basic observation is:

**Institution × publication date × sector**

Each eligible advisor publication produces one advisor snapshot. Each sector covered in that publication receives its original published stance, a standardized ordinal score, and a comparable rank.

The working dataset should preserve at least these fields:

| Field | Meaning |
|---|---|
| `institution` | Publishing institution |
| `publication_date` | Date of the advisor outlook |
| `sector` | Comparable sector / ETF ticker |
| `raw_stance` | Advisor's original label or wording |
| `normalized_score` | Standardized ordinal score |
| `source_title` | Publication title |
| `source_url` | Source location |
| `notes` | Coding notes, if needed |

Raw wording must always be retained. The numerical score must never replace the original source language.

## 4. Sector universe

Use the same 11 sector universe as the computational model:

- XLB — Materials
- XLC — Communication Services
- XLE — Energy
- XLF — Financials
- XLI — Industrials
- XLK — Technology
- XLP — Consumer Staples
- XLRE — Real Estate
- XLU — Utilities
- XLV — Health Care
- XLY — Consumer Discretionary

SPY remains the benchmark and is not included as a sector recommendation.

A sector not covered by an advisor is recorded as **missing**, not neutral.

## 5. Advisor sample target

The initial target is:

- **4 professional institutions**
- **up to 4 dated sector-outlook snapshots per institution**
- preferably quarterly observations within a common period
- up to 11 sectors per snapshot

This implies a maximum initial design of approximately `4 × 4 × 11 = 176` institution-date-sector observations before missing sectors.

Institution selection must be based on data availability and methodological eligibility, not on observed agreement with any model.

Potential institutions may include firms such as Schwab, Fidelity, J.P. Morgan, BlackRock, Vanguard, Morningstar, or other professional institutions that publish explicit dated sector views. Final inclusion depends on the criteria below.

## 6. Publication inclusion criteria

A publication is eligible for quantitative comparison only if all of the following hold:

1. It is issued by an identifiable professional investment institution.
2. It has a clear publication date.
3. It contains explicit sector-level investment views or recommendations.
4. The recommendations represent the publishing institution's own views.
5. The publication covers at least **6 of the 11** comparable sectors.
6. The recommendation language can be translated consistently into the standardized ordinal framework.
7. The publication date can be matched to available market data so model stances can be reconstructed without look-ahead.

Exclude a publication if any of the following apply:

- no reliable publication date;
- fewer than 6 comparable sectors;
- sectors are discussed but no relative stance is expressed;
- the article mainly quotes or summarizes another institution's views;
- the recommendation categories cannot be mapped consistently;
- the required historical market data are unavailable for the publication date.

Documents excluded from the quantitative sample may still be used qualitatively if clearly labeled as such.

## 7. Standardized advisor scoring

Advisor recommendations will be translated into a five-point ordinal scale:

| Standardized interpretation | Score |
|---|---:|
| Strongly favorable / highest conviction / strong overweight | +2 |
| Favorable / overweight / outperform / positive | +1 |
| Neutral / market weight | 0 |
| Unfavorable / underweight / underperform / negative | -1 |
| Strongly unfavorable / lowest conviction / strong underweight | -2 |

### Coding rules

- Prefer the institution's explicit rating label over interpretation of surrounding prose.
- If an institution labels a sector `Neutral`, the score is 0 even if the narrative discusses substantial risks or opportunities.
- Do not infer a recommendation from descriptive commentary alone unless the institution explicitly states a directional stance.
- If an institution uses fewer categories, map only the categories it actually provides. Do not artificially create `+2` or `-2` observations.
- Any ambiguous case must be documented in `notes` and resolved consistently across that institution's publications.

## 8. Ranking advisor views

The primary comparison uses **sector ranks**, not raw advisor scores.

Within each institution-date snapshot:

1. rank sectors from most favorable to least favorable;
2. use average ranks for tied scores;
3. retain only sectors observed in that advisor snapshot for comparison with model rankings.

Average ranks are required for ties. No arbitrary alphabetical or ticker-based tie-breaking is allowed.

Rank-based comparison is used because institutions employ different recommendation vocabularies and category counts.

## 9. Computational models

The advisor stance is compared with three primary computational models:

### Cognitive agent

The behaviorally motivated, path-dependent agent. Perceived risk combines:

- loss aversion;
- shock / surprise;
- drawdown relative to a running peak;
- decaying memory of prior losses.

The cognitive agent is the model of interest.

### Classical agent

The volatility-targeting agent is treated as a **mechanical risk-management benchmark**, not as a complete representation of a fully rational investor.

### Momentum A

The logistic 12–2 momentum specification is the **primary momentum benchmark**.

### Momentum B

The binary 12–2 momentum specification is retained as a **robustness check**, not as a separate primary hypothesis comparison.

## 10. Time alignment and look-ahead prevention

For an advisor publication dated `t`, all model stances must be reconstructed using only information available on or before `t`.

For each advisor snapshot:

- run the cognitive stance using cutoff date `t`;
- run the classical stance using cutoff date `t`;
- run Momentum A using cutoff date `t`;
- run Momentum B using cutoff date `t` for robustness.

The existing stance framework uses the most recent 21 trading days at the relevant cutoff to summarize each model's sector exposure.

A historical advisor recommendation must never be compared with a model stance computed using market data that occurred after the publication date.

## 11. Primary comparison statistic

The primary statistic is **Spearman rank correlation**.

For every eligible advisor snapshot, calculate:

- `rho(advisor, cognitive)`
- `rho(advisor, classical)`
- `rho(advisor, momentumA)`

Momentum B is reported as a robustness comparison.

Each correlation is computed only across sectors present in both the advisor snapshot and the model universe. The number of sectors `N` used in each comparison must be reported.

## 12. Secondary comparison statistics

### 12.1 Mean absolute rank distance (MARD)

For the `N` common sectors:

`MARD = (1/N) × Σ |advisor_rank_i - model_rank_i|`

Lower values indicate greater similarity.

### 12.2 Top-three agreement

Count the overlap between the advisor's three most favored sectors and each model's three highest-ranked sectors.

Possible range: 0–3.

Where ties prevent a unique top three, the handling rule must be documented and applied identically across models. The preferred implementation is to calculate top-three agreement from average ranks while preserving tied membership transparently.

### 12.3 Bottom-three agreement

Count the overlap between the advisor's three least favored sectors and each model's bottom three sectors.

Possible range: 0–3.

## 13. Snapshot-level results table

Each advisor snapshot should produce a table with at least:

| Institution | Date | N | Cognitive rho | Classical rho | Momentum A rho | Cognitive MARD | Classical MARD | Momentum A MARD | Cognitive Top-3 | Classical Top-3 | Momentum Top-3 | Cognitive Bottom-3 | Classical Bottom-3 | Momentum Bottom-3 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|

Momentum B can be reported in a robustness table or appendix.

## 14. Aggregate model comparison

Across all eligible advisor snapshots, summarize each model using:

- mean Spearman rank correlation;
- median Spearman rank correlation;
- mean MARD;
- mean top-three overlap;
- mean bottom-three overlap;
- number / proportion of advisor snapshots for which each model is the closest match.

The cognitive hypothesis receives support if the cognitive agent shows systematically higher rank similarity and/or lower rank distance than both primary benchmarks. A single favorable advisor snapshot is not sufficient evidence.

## 15. Missing sectors

No missing advisor sector is imputed as neutral.

For each snapshot, comparisons are performed on the common sector set:

`S_common = S_advisor ∩ S_model`

The resulting `N` must be displayed in the results table.

Snapshots with fewer than **6 sectors** are excluded from the quantitative analysis.

## 16. Interpretation rules

### Permitted interpretation

If professional recommendations align more closely with the cognitive model, the result may be described as:

> Professional sector recommendations are more consistent with the behavioral mechanisms represented by the cognitive agent than with the selected mechanical benchmark models.

### Claims not supported by this design

The study does not establish that:

- an individual advisor is psychologically irrational;
- the institution consciously exhibits loss aversion, drawdown regret, shock sensitivity, or memory;
- the cognitive agent is a validated psychological measurement instrument;
- cognitive similarity proves causality;
- behavioral modelling necessarily improves financial performance.

Advisor positions may also reflect valuation, fundamentals, macroeconomic forecasts, mandates, client objectives, or information not contained in the computational agents.

## 17. Robustness and sensitivity checks

The following are planned robustness checks rather than primary hypothesis tests:

1. compare advisor rankings with Momentum B as well as Momentum A;
2. examine whether results change when advisor snapshots with incomplete sector coverage are removed;
3. report results separately by institution as well as pooled across institutions;
4. inspect sensitivity to the 21-trading-day stance averaging window if time permits;
5. inspect sensitivity to cognitive-agent parameter choices if time permits;
6. distinguish results from periods of market stress from calmer periods if the sample becomes large enough.

Any robustness change made after viewing results must be labeled as exploratory unless it was specified here in advance.

## 18. Researcher-discretion rule

This document is the pre-analysis coding and comparison rule for the advisor extension.

After advisor data collection begins, the following should not be changed merely because results favor or disfavor the hypothesis:

- five-point stance mapping;
- minimum six-sector threshold;
- use of average ranks for ties;
- Spearman correlation as primary statistic;
- MARD and top-/bottom-three agreement as secondary statistics;
- Momentum A as the primary momentum benchmark;
- cutoff-date alignment rule;
- requirement to retain raw advisor wording.

A methodology change is allowed only to fix a genuine design flaw or address an unanticipated source format. Any such change must be documented with the reason and date.

## 19. Initial data-collection target

The next project task is to identify four institutions with suitable archived, dated sector outlooks and build the advisor dataset according to this methodology.

The preferred target is four snapshots per institution. If consistent quarterly histories are unavailable, use the largest comparable set available while preserving the eligibility rules and reporting the resulting sample size transparently.

## 20. Planned paper framing

The advisor study should answer:

**Which computational model best resembles professional sector recommendations?**

The broader paper, *Modelling Investor Irrationality*, uses the cognitive agent to operationalize selected behavioral-finance mechanisms and then asks whether the investment preferences produced by those mechanisms resemble professional human advice more closely than volatility-targeting or momentum alternatives.

The strongest defensible conclusion is about **behavioral consistency**, not proof of irrationality.