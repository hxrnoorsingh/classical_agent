"""
agents.py — THE single source of truth for all three agents.

Nothing else in this project defines an agent. If you change a formula or a
parameter, change it here and it propagates everywhere.

    from agents import run_classical, run_cognitive, run_momentum

Verified 2026-08-06 against Classical_Agent_SPY_Excel.xlsx:
    classical max drawdown   0.115372  (target 0.1153)
    classical avg exposure   0.547179  (target 0.5451)
    cognitive baseline stress 0.126151 (target 0.126317)
    cognitive peak stress     0.564453 (target 0.564453, exact)
    cognitive time in stress  0.102740 (target 0.1034)
Sharpe differs by convention only; see sharpe() below.
"""
import numpy as np
import pandas as pd

# ----------------------------------------------------------------- parameters
CLASSICAL = dict(target_vol=0.10, lookback=20, w_min=0.05, w_max=1.0,
                 trading_days=252, vol_floor=1e-4)

COGNITIVE = dict(loss_aversion=1.5, shock_sensitivity=1.2, drawdown_regret=1.0,
                 memory_decay=0.92, memory_scale=0.42, risk_sensitivity=8.0,
                 shock_window=10, w_min=0.05, w_max=1.0)

MOMENTUM = dict(lookback=252, skip=21, min_obs=120, steepness=6.0,
                w_min=0.05, w_max=1.0)

TICKERS = ["XLB", "XLC", "XLE", "XLF", "XLI", "XLK",
           "XLP", "XLRE", "XLU", "XLV", "XLY", "SPY"]
SECTORS = [t for t in TICKERS if t != "SPY"]

SECTOR_NAMES = {
    "XLB": "Materials", "XLC": "Communication services", "XLE": "Energy",
    "XLF": "Financials", "XLI": "Industrials", "XLK": "Technology",
    "XLP": "Consumer staples", "XLRE": "Real estate", "XLU": "Utilities",
    "XLV": "Health care", "XLY": "Consumer discretionary",
    "SPY": "S&P 500 (benchmark)",
}


def _wrap(index, r, exposure, extra=None):
    """Common tail: realise returns, build equity, compute drawdown."""
    agent_ret = exposure * r
    equity = 100.0 * np.cumprod(1.0 + agent_ret)
    peak = np.maximum.accumulate(equity)
    df = pd.DataFrame({"ret_tr": r, "exposure": exposure,
                       "agent_ret": agent_ret, "equity": equity,
                       "drawdown": (peak - equity) / peak}, index=index)
    for k, v in (extra or {}).items():
        df[k] = v
    return df


# ------------------------------------------------------------------ classical
def run_classical(returns, p=CLASSICAL):
    """Volatility targeting. Stateless. The emotion-free control."""
    s = returns.dropna()
    r = s.values
    n = len(r)
    vol = np.full(n, np.nan)
    exposure = np.full(n, p["w_max"])

    for t in range(n):
        w = r[max(0, t - p["lookback"]):t]           # strictly before t
        if len(w) >= 2:
            vol[t] = w.std(ddof=0) * np.sqrt(p["trading_days"])
            exposure[t] = np.clip(p["target_vol"] / max(vol[t], p["vol_floor"]),
                                  p["w_min"], p["w_max"])

    return _wrap(s.index, r, exposure, {"vol_ann": vol})


# ------------------------------------------------------------------ cognitive
def run_cognitive(returns, p=COGNITIVE):
    """Prospect-theoretic perceived risk. Stateful: memory and peak carry."""
    s = returns.dropna()
    r = s.values
    n = len(r)
    h = p["shock_window"]

    keys = ("avg_h", "peak", "memory", "loss", "shock", "dd",
            "mem_comp", "risk")
    cols = {k: np.zeros(n) for k in keys}
    exposure = np.zeros(n)

    equity_prev = peak_prev = 100.0
    mem_prev = 0.0

    for t in range(n):
        yday = r[t - 1] if t > 0 else 0.0
        win = r[max(0, t - h):t]
        avg_h = win.mean() if len(win) else 0.0

        peak = max(peak_prev, equity_prev)
        memory = mem_prev * p["memory_decay"] + max(-yday, 0.0)

        loss = max(-yday, 0.0) * p["loss_aversion"]
        shock = abs(yday - avg_h) * p["shock_sensitivity"]
        dd = (peak - equity_prev) / peak * p["drawdown_regret"]
        mem_comp = memory * p["memory_scale"]
        risk = loss + shock + dd + mem_comp

        w = np.clip(1.0 / (1.0 + risk * p["risk_sensitivity"]),
                    p["w_min"], p["w_max"])
        equity = equity_prev * (1.0 + w * r[t])

        for k, v in zip(keys, (avg_h, peak, memory, loss, shock, dd,
                               mem_comp, risk)):
            cols[k][t] = v
        exposure[t] = w
        equity_prev, peak_prev, mem_prev = equity, peak, memory

    return _wrap(s.index, r, exposure, cols)


# ------------------------------------------------------------------- momentum
def _trailing(r, t, p):
    """Cumulative return over [t-lookback, t-skip). Data through t-1 only.

    The skip month is the standard 12-2 convention: momentum measured through
    yesterday is contaminated by short-term reversal, which runs the other way.
    """
    hi = t - p["skip"]
    lo = max(0, hi - p["lookback"])
    if hi <= lo:
        return np.nan
    w = r[lo:hi]
    if len(w) < p["min_obs"]:
        return np.nan
    return float(np.prod(1.0 + w) - 1.0)


def run_momentum(returns, p=MOMENTUM, binary=False):
    """Trend-following control. Instantiates the boring alternative:
    'the committee just likes recent winners'.

    binary=False : logistic squash of trailing return (spec A)
    binary=True  : full exposure if trailing return positive, else min (spec B)

    Spec B is cruder but free of the logistic's arbitrary shape. Report both;
    if their rankings disagree, the comparison rests on that shape.
    """
    s = returns.dropna()
    r = s.values
    n = len(r)
    trail = np.full(n, np.nan)
    exposure = np.full(n, p["w_max"])

    for t in range(n):
        m = _trailing(r, t, p)
        trail[t] = m
        if np.isnan(m):
            continue
        if binary:
            exposure[t] = p["w_max"] if m > 0 else p["w_min"]
        else:
            exposure[t] = np.clip(1.0 / (1.0 + np.exp(-p["steepness"] * m)),
                                  p["w_min"], p["w_max"])

    return _wrap(s.index, r, exposure, {"trail": trail})


AGENTS = {"classical": run_classical,
          "cognitive": run_cognitive,
          "momentum": run_momentum}


# -------------------------------------------------------------------- metrics
def sharpe(df, td=252, geometric=False):
    """Default is the arithmetic convention (mean/sd), which is what the
    workbook uses. Set geometric=True for CAGR / annualised volatility.
    """
    ar = df["agent_ret"].values
    sd = ar.std(ddof=0)
    if sd == 0:
        return np.nan
    if geometric:
        eq = df["equity"].values
        return ((eq[-1] / 100) ** (td / len(eq)) - 1) / (sd * np.sqrt(td))
    return ar.mean() / sd * np.sqrt(td)


def financial_metrics(df, td=252):
    eq, ar = df["equity"].values, df["agent_ret"].values
    return {
        "total_return": eq[-1] / 100 - 1,
        "ann_return": (eq[-1] / 100) ** (td / len(eq)) - 1,
        "ann_vol": ar.std(ddof=0) * np.sqrt(td),
        "sharpe": sharpe(df, td),
        "sharpe_geo": sharpe(df, td, geometric=True),
        "max_drawdown": df["drawdown"].max(),
        "avg_exposure": df["exposure"].mean(),
    }


def welfare_metrics(df):
    """Only defined for the cognitive agent: needs a 'risk' column."""
    if "risk" not in df:
        return None
    risk = df["risk"].values
    thr = np.percentile(risk, 90)
    stressed = risk > thr
    starts = int(np.sum(stressed & ~np.r_[False, stressed[:-1]]))
    return {
        "baseline_stress": risk.mean(),
        "stress_volatility": risk.std(ddof=0),
        "peak_stress": risk.max(),
        "high_stress_threshold": thr,
        "time_in_stress": stressed.mean(),
        "mean_episode_days": stressed.sum() / max(starts, 1),
    }
