"""
analysis.py — every table and diagnostic. Imports agents from agents.py.

    python analysis.py              run everything on the latest snapshot
    python analysis.py snapshot_X   or name one
"""
import os
import sys

import numpy as np
import pandas as pd

from agents import (run_classical, run_cognitive, run_momentum, COGNITIVE,
                    SECTORS, SECTOR_NAMES, financial_metrics, welfare_metrics)
from data import load_panel, latest_snapshot

OUT = "results"
WINDOW = 21

# Workbook verification targets (SPY, 2019-12-01 .. 2020-06-30)
GATE_WINDOW = ("2019-12-01", "2020-06-30")
GATE = {"classical_maxdd": 0.1153, "classical_avg_exposure": 0.5451,
        "cognitive_baseline_stress": 0.126317,
        "cognitive_peak_stress": 0.564453,
        "cognitive_time_in_stress": 0.1034}


def verification_gate(panel):
    lo, hi = GATE_WINDOW
    w = panel["SPY"].loc[lo:hi]
    cla, cog = run_classical(w), run_cognitive(w)
    fc, wf = financial_metrics(cla), welfare_metrics(cog)
    got = {"classical_maxdd": fc["max_drawdown"],
           "classical_avg_exposure": fc["avg_exposure"],
           "cognitive_baseline_stress": wf["baseline_stress"],
           "cognitive_peak_stress": wf["peak_stress"],
           "cognitive_time_in_stress": wf["time_in_stress"]}
    rows = [{"metric": k, "target": v, "got": round(got[k], 6),
             "diff": round(abs(got[k] - v), 6),
             "pass": "YES" if abs(got[k] - v) < 0.005 else "NO"}
            for k, v in GATE.items()]
    rows.append({"metric": "classical_sharpe (arith)", "target": 0.2525,
                 "got": round(financial_metrics(cla)["sharpe"], 6),
                 "diff": round(abs(financial_metrics(cla)["sharpe"] - 0.2525), 6),
                 "pass": "YES" if abs(financial_metrics(cla)["sharpe"] - 0.2525)
                         < 0.005 else "NO"})
    return pd.DataFrame(rows)


def table_one(panel):
    rows = []
    for tk, r in panel.items():
        cla, cog, mom = run_classical(r), run_cognitive(r), run_momentum(r)
        fc, fg, fm = (financial_metrics(cla), financial_metrics(cog),
                      financial_metrics(mom))
        wf = welfare_metrics(cog)
        rows.append({"ticker": tk, "obs": len(r), "start": r.index[0].date(),
                     "cla_sharpe": fc["sharpe"], "cog_sharpe": fg["sharpe"],
                     "mom_sharpe": fm["sharpe"],
                     "cla_maxdd": fc["max_drawdown"],
                     "cog_maxdd": fg["max_drawdown"],
                     "mom_maxdd": fm["max_drawdown"],
                     "baseline_stress": wf["baseline_stress"],
                     "stress_vol": wf["stress_volatility"],
                     "peak_stress": wf["peak_stress"],
                     "episode_days": wf["mean_episode_days"]})
    return pd.DataFrame(rows).set_index("ticker")


def component_shares(panel):
    rows = []
    for tk in SECTORS:
        if tk not in panel:
            continue
        d = run_cognitive(panel[tk])
        tot = d["risk"].mean()
        rows.append({"tk": tk,
                     "loss_%": round(100 * d["loss"].mean() / tot, 1),
                     "shock_%": round(100 * d["shock"].mean() / tot, 1),
                     "dd_%": round(100 * d["dd"].mean() / tot, 1),
                     "mem_%": round(100 * d["mem_comp"].mean() / tot, 1)})
    return pd.DataFrame(rows).set_index("tk")


def raw_scales(panel):
    d = run_cognitive(panel["SPY"])
    raw = {"loss max(-r,0)": d["loss"] / COGNITIVE["loss_aversion"],
           "shock |r-avg|": d["shock"] / COGNITIVE["shock_sensitivity"],
           "drawdown frac": d["dd"] / COGNITIVE["drawdown_regret"],
           "memory accum": d["mem_comp"] / COGNITIVE["memory_scale"]}
    return pd.DataFrame({k: {"mean": v.mean(), "p90": v.quantile(.9),
                             "max": v.max()} for k, v in raw.items()}).T


def ablations(panel):
    variants = {"full": {}, "no_loss": {"loss_aversion": 0.0},
                "no_shock": {"shock_sensitivity": 0.0},
                "no_drawdown": {"drawdown_regret": 0.0},
                "no_memory": {"memory_scale": 0.0}}
    orders, rows = {}, []
    for name, ov in variants.items():
        p = dict(COGNITIVE, **ov)
        orders[name] = pd.Series(
            {tk: welfare_metrics(run_cognitive(panel[tk], p))["baseline_stress"]
             for tk in SECTORS if tk in panel})
    base = orders["full"].rank()
    for name, s in orders.items():
        rows.append({"variant": name,
                     "mean_stress": round(s.mean(), 4),
                     "spearman_vs_full": round(
                         base.corr(s.rank(), method="spearman"), 3),
                     "top3": ", ".join(s.sort_values(ascending=False).index[:3])})
    return pd.DataFrame(rows)


def contamination(panel):
    rows = []
    for tk in SECTORS:
        if tk not in panel:
            continue
        a = run_cognitive(panel[tk])["exposure"]
        b = run_momentum(panel[tk])["exposure"].reindex(a.index)
        ok = a.notna() & b.notna()
        c = a[ok].corr(b[ok])
        rows.append({"tk": tk, "corr": round(c, 3), "r2": round(c ** 2, 3)})
    return pd.DataFrame(rows).set_index("tk")


def stances(panel, cutoff=None):
    sc, risk = {}, {}
    for tk in SECTORS:
        if tk not in panel:
            continue
        r = panel[tk].loc[:cutoff] if cutoff else panel[tk]
        cog = run_cognitive(r)
        sc[tk] = {"cognitive": cog["exposure"].iloc[-WINDOW:].mean(),
                  "classical": run_classical(r)["exposure"].iloc[-WINDOW:].mean(),
                  "momentumA": run_momentum(r)["exposure"].iloc[-WINDOW:].mean(),
                  "momentumB": run_momentum(r, binary=True)["exposure"]
                               .iloc[-WINDOW:].mean()}
        risk[tk] = cog["risk"].iloc[-WINDOW:].mean()
    st = pd.DataFrame(sc).T
    st["cog_risk"] = pd.Series(risk)
    for c in ("cognitive", "classical", "momentumA", "momentumB"):
        st[c + "_rk"] = st[c].rank(ascending=False).astype(int)
    st["risk_rk"] = st["cog_risk"].rank(ascending=True).astype(int)
    agree = bool((st["cognitive_rk"] == st["risk_rk"]).all())
    return st.sort_values("cognitive_rk"), agree


def figures(panel, t1):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    lo, hi = "2019-12-01", "2020-07-31"
    spy = panel["SPY"]
    cla, cog = run_classical(spy), run_cognitive(spy)

    fig, ax = plt.subplots(2, 1, figsize=(9, 6), sharex=True,
                           gridspec_kw={"height_ratios": [2, 1]})
    ax[0].plot(cla.loc[lo:hi].index, cla.loc[lo:hi, "exposure"],
               label="Classical", lw=1.3)
    ax[0].plot(cog.loc[lo:hi].index, cog.loc[lo:hi, "exposure"],
               label="Cognitive", lw=1.3)
    ax[0].set_ylabel("Exposure"); ax[0].set_ylim(0, 1.05)
    ax[0].legend(frameon=False); ax[0].set_title("SPY through the COVID crash")
    ax[1].plot(cog.loc[lo:hi].index, cog.loc[lo:hi, "ret_tr"], lw=.7, color="0.4")
    ax[1].axhline(0, lw=.5, color="0.7"); ax[1].set_ylabel("Daily return")
    fig.tight_layout(); fig.savefig(f"{OUT}/fig1_exposure.png", dpi=200)
    plt.close(fig)

    sl = cog.loc[lo:hi]
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.stackplot(sl.index, sl["loss"], sl["shock"], sl["dd"], sl["mem_comp"],
                 labels=["Loss", "Shock", "Drawdown", "Memory"], alpha=.85)
    ax.plot(sl.index, sl["risk"], color="black", lw=1.0, label="Perceived risk")
    ax.set_ylabel("Perceived risk"); ax.set_title("The fear signal, decomposed")
    ax.legend(frameon=False, ncol=5, fontsize=8)
    fig.tight_layout(); fig.savefig(f"{OUT}/fig2_components.png", dpi=200)
    plt.close(fig)

    d = t1.sort_values("baseline_stress")
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(d.index, d["baseline_stress"],
            color=["0.6" if t == "SPY" else "0.3" for t in d.index])
    ax.set_xlabel("Baseline stress (mean perceived risk)")
    ax.set_title("Sector welfare ordering")
    fig.tight_layout(); fig.savefig(f"{OUT}/fig3_welfare.png", dpi=200)
    plt.close(fig)


def main():
    snap = latest_snapshot(sys.argv[1] if len(sys.argv) > 1 else None)
    panel = load_panel(snap, align_legacy=True)
    os.makedirs(OUT, exist_ok=True)
    print(f"{os.path.basename(snap)}: {len(panel)} series "
          f"(legacy funds aligned)\n")
    print("=" * 72); print("PASTE BELOW"); print("=" * 72)

    print("\n--- [0] VERIFICATION GATE ---")
    print(verification_gate(load_panel(snap)).to_string(index=False))

    print("\n--- [1] TABLE 1 ---")
    t1 = table_one(panel); t1.to_csv(f"{OUT}/table1.csv")
    print(t1.drop(columns=["start"]).round(3).to_string())
    s = t1.loc["SPY", "baseline_stress"]
    calmer = int((t1.drop("SPY")["baseline_stress"] < s).sum())
    print(f"\nSPY stress {s:.4f}: {len(t1)-1-calmer} sectors more stressful, "
          f"{calmer} calmer")

    print("\n--- [2] WELFARE ORDERING ---")
    for i, (tk, v) in enumerate(
            t1["baseline_stress"].sort_values(ascending=False).items(), 1):
        print(f"{i:>3}. {tk:<5} {v:.4f}  {SECTOR_NAMES[tk]}")

    print("\n--- [3] COMPONENT SHARES (% of mean perceived risk) ---")
    cs = component_shares(panel); cs.to_csv(f"{OUT}/component_shares.csv")
    print(cs.to_string())
    print("panel mean: " + "  ".join(f"{c}={cs[c].mean():.1f}" for c in cs.columns))

    print("\n--- [4] RAW SCALES, before parameters (SPY) ---")
    print(raw_scales(panel).round(4).to_string())

    print("\n--- [5] ABLATIONS ---")
    ab = ablations(panel); ab.to_csv(f"{OUT}/ablations.csv", index=False)
    print(ab.to_string(index=False))
    print("spearman_vs_full near 1 => that component does not drive the ORDERING")

    print("\n--- [6] MOMENTUM CONTAMINATION ---")
    ct = contamination(panel); ct.to_csv(f"{OUT}/contamination.csv")
    print(ct.to_string()); print(f"mean r2 {ct['r2'].mean():.3f}")

    print("\n--- [7] STANCE RANKINGS ---")
    st, agree = stances(panel); st.to_csv(f"{OUT}/stances.csv")
    print(st.round(3).to_string())
    print(f"exposure rank == risk rank: {agree}")

    figures(panel, t1)
    print(f"\nfigures -> {OUT}/"); print("=" * 72)


if __name__ == "__main__":
    main()
