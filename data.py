"""
data.py — fetch the panel once, freeze it, load it everywhere.

    python data.py            fetch a fresh snapshot
    from data import load_panel, latest_snapshot
"""
import glob
import os
import sys
from datetime import date

import pandas as pd

from agents import TICKERS

ROOT = os.path.dirname(os.path.abspath(__file__))
START = "1998-12-01"


def latest_snapshot(explicit=None):
    if explicit:
        return explicit
    found = [d for d in sorted(glob.glob(os.path.join(ROOT, "snapshot_*")))
             if os.path.isdir(d)]
    if not found:
        sys.exit("No snapshot_* folder. Run: python data.py")
    return found[-1]


def load_panel(snapshot=None, sectors_only=False, align_legacy=False):
    """Returns dict ticker -> Series of daily total returns.

    align_legacy=True trims the 1998-vintage funds to a common start date so
    SPY's extra fortnight does not distort cross-sector comparison. XLC and
    XLRE keep their own inception dates - aligning those would discard most
    of the panel.
    """
    snap = latest_snapshot(snapshot)
    panel = {}
    for path in sorted(glob.glob(os.path.join(snap, "*.csv"))):
        tk = os.path.basename(path)[:-4]
        if tk.startswith("_"):
            continue
        if sectors_only and tk == "SPY":
            continue
        df = pd.read_csv(path, parse_dates=["date"], index_col="date")
        panel[tk] = df["ret_tr"].dropna()

    if not panel:
        sys.exit(f"No CSVs in {snap}")

    if align_legacy:
        legacy = [t for t in panel if panel[t].index[0].year < 2000]
        if legacy:
            common = max(panel[t].index[0] for t in legacy)
            for t in legacy:
                panel[t] = panel[t].loc[common:]
    return panel


def fetch():
    import yfinance as yf
    snap = os.path.join(ROOT, f"snapshot_{date.today().isoformat()}")
    os.makedirs(snap, exist_ok=True)
    audit = []

    for tk in TICKERS:
        print(f"  {tk:5s}", end=" ", flush=True)
        try:
            raw = yf.download(tk, start=START, auto_adjust=False,
                              actions=True, progress=False)
        except Exception as exc:
            print(f"FAILED {type(exc).__name__}: {exc}")
            continue
        if raw.empty:
            print("FAILED empty response")
            continue
        if isinstance(raw.columns, pd.MultiIndex):
            raw.columns = raw.columns.get_level_values(0)

        df = pd.DataFrame(index=raw.index)
        df["close_raw"] = raw["Close"]
        df["close_tr"] = raw["Adj Close"]
        df["dividend"] = raw.get("Dividends", 0.0)
        df["ret_price"] = df["close_raw"].pct_change()
        df["ret_tr"] = df["close_tr"].pct_change()
        df.index.name = "date"
        df.to_csv(os.path.join(snap, f"{tk}.csv"))

        gap = (df["ret_tr"] - df["ret_price"]).abs()
        div = set(df.index[gap > 1e-6])
        paid = set(df.index[df["dividend"] > 0])
        audit.append({"ticker": tk, "rows": len(df),
                      "first": df.index[0].date(), "last": df.index[-1].date(),
                      "div_events": len(paid), "divergent": len(div),
                      "matched": len(div & paid)})
        print(f"{len(df):>5} rows  {df.index[0].date()} -> {df.index[-1].date()}")

    a = pd.DataFrame(audit)
    a.to_csv(os.path.join(snap, "_audit.csv"), index=False)
    print(f"\nsnapshot: {os.path.basename(snap)}\n")
    print(a.to_string(index=False))
    return snap


if __name__ == "__main__":
    fetch()
