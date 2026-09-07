# Advisor Comparison — Provisional Results

These results implement the frozen advisor-comparison methodology for all eight advisor snapshots, but currently use **10 of the 11 sectors** because the local analysis runtime did not contain the `XLY.csv` market snapshot. Advisor XLY observations remain preserved in `advisor_data.csv`; they have not been imputed or substituted.

The committed `advisor_comparison.py` pipeline will automatically use all 11 sectors when the repository snapshot contains XLY.

## Provisional 10-sector aggregate

| Model | Mean Spearman rho | Median rho | Mean MARD | Mean Top overlap | Mean Bottom overlap |
|---|---:|---:|---:|---:|---:|
| Cognitive | 0.171 | 0.178 | 2.888 | 1.875 | 0.375 |
| Classical | -0.118 | -0.093 | 3.638 | 0.750 | 0.250 |
| Momentum A | 0.204 | 0.140 | 2.888 | 1.125 | 0.625 |
| Momentum B | 0.416* | 0.466* | 2.325 | 0.375 | 0.250 |

`*` Momentum B Spearman correlation is defined in only 3 of the 8 snapshots in this provisional run because its binary exposure becomes constant across the available sectors in the other snapshots. MARD remains calculable but rank correlation is undefined when a model has no cross-sector rank variance. This is one reason Momentum B remains a robustness check rather than the primary momentum benchmark.

## By institution

### Charles Schwab (4 snapshots)

- Cognitive mean rho: **0.182**; mean MARD: **2.900**
- Classical mean rho: **-0.108**; mean MARD: **3.700**
- Momentum A mean rho: **0.137**; mean MARD: **3.175**

On the current 10-sector comparison, cognitive has the highest average rank correlation and lowest rank distance among the three primary models for Schwab.

### Wells Fargo Investment Institute (4 snapshots)

- Cognitive mean rho: **0.159**; mean MARD: **2.875**
- Classical mean rho: **-0.128**; mean MARD: **3.575**
- Momentum A mean rho: **0.271**; mean MARD: **2.600**

For Wells Fargo, Momentum A currently resembles the published sector views more closely than the cognitive model on both primary rank correlation and MARD.

## Interpretation before XLY is added

The current result does **not** support a simple claim that professional advice uniformly resembles the cognitive agent most closely.

It does support two more nuanced observations:

1. The cognitive agent substantially outperforms the classical volatility-targeting benchmark in average rank similarity across these cases.
2. The comparison with momentum is institution-dependent: cognitive currently leads for Schwab, while Momentum A leads for Wells Fargo.

Across all eight snapshots, Momentum A has a slightly higher mean Spearman correlation than cognitive (0.204 vs. 0.171), while the two have essentially the same provisional mean MARD (2.888). Therefore the pre-specified main hypothesis is **not yet supported in pooled results** on the 10-sector provisional sample.

This is a scientifically useful result rather than a failure: the momentum control is doing its intended job of testing whether apparent behavioral similarity is distinct from trend-following behavior.

## Required completion step

Add `XLY.csv` to the market snapshot and run:

```bash
python advisor_comparison.py
```

Only the resulting 11-sector files should be treated as final paper results. The provisional file is deliberately named `advisor_snapshot_comparison_provisional.csv` to prevent accidental use as the final table.
