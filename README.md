# Consolidated pipeline

One definition of each agent. Everything imports from `agents.py`.

```
agents.py     the three agents + metrics   <- ONLY place agents are defined
data.py       fetch / load the snapshot
analysis.py   every table, diagnostic, figure
```

## Run

```bash
pip install yfinance pandas numpy matplotlib
python data.py         # once. writes snapshot_YYYY-MM-DD/
python analysis.py     # finds the newest snapshot automatically
```

Paste the block between the PASTE BELOW markers.

## What replaced what

These five files are now obsolete - delete them:
`run_local.py`, `diagnose.py`, `build_results.py`, `component_diag.py`,
`momentum.py`, and the old `paper/code/` directory.

They duplicated the agent definitions, and two versions of the momentum agent
had different specifications (one without the skip month). That class of bug
is what this consolidation removes.

## Output blocks

| Block | What it settles |
|---|---|
| 0 | verification gate vs the Excel workbooks |
| 1 | Table 1 - three agents, legacy funds date-aligned |
| 2 | welfare ordering (Figure 3 data) |
| 3 | component shares of perceived risk |
| 4 | raw component scales *before* parameters |
| 5 | ablations - does the ORDERING survive removing each component |
| 6 | momentum contamination - is cognitive just trend-following |
| 7 | stance rankings, all agents, ready for the advisor column |

## Notes

- Sharpe defaults to the arithmetic convention (mean/sd), matching the
  workbook. `financial_metrics` also returns `sharpe_geo`.
- `load_panel(align_legacy=True)` trims 1998-vintage funds to a common start
  so SPY's extra fortnight does not distort cross-sector comparison.
- Momentum uses the 12-2 convention: twelve months, skipping the most recent
  month, because short-term reversal runs opposite to momentum.
- Blocks 3-5 exist because drawdown may dominate perceived risk. Check block 4:
  if drawdown's raw mean is an order of magnitude above the others, the
  parameters are not relative weights.
