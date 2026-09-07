"""advisor_comparison.py — compare dated advisor sector views with all agents.

Uses the frozen rules in advisor_methodology.md.

    python advisor_comparison.py

Outputs:
    results/advisor_snapshot_comparison.csv
    results/advisor_institution_summary.csv
    results/advisor_model_summary.csv

The script reconstructs every model using market data only through each advisor
publication date. It uses average ranks for ties, Spearman rank correlation as
the primary statistic, MARD as a secondary distance measure, and tied-set
Top/Bottom-3 overlap as descriptive secondary measures.
"""
import os
import numpy as np
import pandas as pd

from agents import run_classical, run_cognitive, run_momentum, SECTORS
from data import load_panel, latest_snapshot

WINDOW = 21
ADVISOR_FILE = "advisor_data.csv"
OUT = "results"
MODELS = ("cognitive", "classical", "momentumA", "momentumB")


def model_stances(panel, cutoff):
    """Sector exposures using only data through cutoff."""
    sc = {}
    for tk in SECTORS:
        if tk not in panel:
            continue
        r = panel[tk].loc[:cutoff]
        if r.empty:
            continue
        cog = run_cognitive(r)
        sc[tk] = {
            "cognitive": cog["exposure"].iloc[-WINDOW:].mean(),
            "classical": run_classical(r)["exposure"].iloc[-WINDOW:].mean(),
            "momentumA": run_momentum(r)["exposure"].iloc[-WINDOW:].mean(),
            "momentumB": run_momentum(r, binary=True)["exposure"].iloc[-WINDOW:].mean(),
        }
    return pd.DataFrame(sc).T


def tied_rank(s):
    """Most favorable / highest exposure receives rank 1; ties get averages."""
    return s.rank(ascending=False, method="average")


def tied_top_bottom(rank):
    """Return transparent tied sets around the top/bottom-three cutoffs.

    Because advisor categories create ties, these sets can contain fewer or more
    than exactly three names. Their sizes are reported alongside overlap counts.
    """
    n = len(rank)
    top = set(rank[rank <= 3].index)
    bottom = set(rank[rank >= n - 2].index)
    return top, bottom


def compare_snapshot(advisor_scores, model_df):
    common = advisor_scores.index.intersection(model_df.index)
    a = advisor_scores.loc[common].astype(float)
    m = model_df.loc[common]
    ar = tied_rank(a)
    atop, abot = tied_top_bottom(ar)

    out = {"N": len(common)}
    for model in MODELS:
        mr = tied_rank(m[model])
        mtop, mbot = tied_top_bottom(mr)
        out[f"{model}_rho"] = ar.corr(mr)
        out[f"{model}_mard"] = (ar - mr).abs().mean()
        out[f"{model}_top_overlap"] = len(atop & mtop)
        out[f"{model}_bottom_overlap"] = len(abot & mbot)
        out[f"advisor_top_n"] = len(atop)
        out[f"advisor_bottom_n"] = len(abot)
        out[f"{model}_top_n"] = len(mtop)
        out[f"{model}_bottom_n"] = len(mbot)
    return out


def summarize(df, group=None):
    groups = [("ALL", df)] if group is None else df.groupby(group)
    rows = []
    for name, g in groups:
        for model in MODELS:
            rho = g[f"{model}_rho"]
            row = {
                "group": name,
                "model": model,
                "snapshots": len(g),
                "valid_rho": int(rho.notna().sum()),
                "mean_rho": rho.mean(),
                "median_rho": rho.median(),
                "mean_mard": g[f"{model}_mard"].mean(),
                "mean_top_overlap": g[f"{model}_top_overlap"].mean(),
                "mean_bottom_overlap": g[f"{model}_bottom_overlap"].mean(),
            }
            rows.append(row)
    return pd.DataFrame(rows)


def main():
    if not os.path.exists(ADVISOR_FILE):
        raise SystemExit(f"Missing {ADVISOR_FILE}")

    adv = pd.read_csv(ADVISOR_FILE, parse_dates=["publication_date"])
    panel = load_panel(latest_snapshot(), align_legacy=True)

    rows = []
    for (institution, date), g in adv.groupby(["institution", "publication_date"], sort=True):
        scores = g.set_index("sector")["normalized_score"]
        stance = model_stances(panel, date)
        comp = compare_snapshot(scores, stance)
        if comp["N"] < 6:
            continue
        rows.append({"institution": institution,
                     "publication_date": date.date(), **comp})

    snap = pd.DataFrame(rows)
    os.makedirs(OUT, exist_ok=True)
    snap.to_csv(f"{OUT}/advisor_snapshot_comparison.csv", index=False)

    inst = summarize(snap, "institution")
    inst.to_csv(f"{OUT}/advisor_institution_summary.csv", index=False)

    overall = summarize(snap)
    overall.to_csv(f"{OUT}/advisor_model_summary.csv", index=False)

    print("\n--- ADVISOR SNAPSHOT COMPARISON ---")
    show = ["institution", "publication_date", "N"]
    for model in ("cognitive", "classical", "momentumA", "momentumB"):
        show += [f"{model}_rho", f"{model}_mard"]
    print(snap[show].round(3).to_string(index=False))

    print("\n--- INSTITUTION SUMMARY ---")
    print(inst.round(3).to_string(index=False))

    print("\n--- OVERALL MODEL SUMMARY ---")
    print(overall.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
