"""
COGNITIVE AGENT — a decision-maker with an inner life
=====================================================
Same skeleton as the classical agent (observe -> set exposure -> bear the
consequence) plus a psychology, following cognitive_agent_refactored.py:

  Perceived risk = loss aversion   (losses hurt more than equal gains)
                 + shock sensitivity (surprise hurts)
                 + drawdown regret (being below your peak hurts)
                 + decaying memory of past pain (trauma lingers)

  weight = 1 / (1 + perceived_risk * risk_sensitivity), clipped [0.05, 1.0]

Look-ahead fix applied (matching the classical agent): the weight for day t
is computed from what the agent has EXPERIENCED through day t-1 (yesterday's
return, current drawdown, accumulated memory). It never sees today's return
before choosing today's exposure.

This is the measuring instrument — a model of the human, not a trading
product. Its perceived_risk trace is the welfare signal the research
instruments (baseline stress, stress volatility, time-in-stress, etc.).
"""

import numpy as np
from dataclasses import dataclass


@dataclass
class AgentParams:
    loss: float = 1.5        # loss aversion weight
    shock: float = 1.2       # shock (surprise) sensitivity
    dd: float = 1.0          # drawdown regret weight
    mem_decay: float = 0.92  # memory decay factor per day
    rs: float = 8.0          # risk sensitivity (perceived risk -> weight)
    mem_scale: float = 0.42  # scaling of memory into perceived risk

    def to_dict(self):
        return self.__dict__.copy()


class CognitiveAgent:
    def __init__(self, params: AgentParams = None):
        self.params = params or AgentParams()
        # state carried between days
        self.memory = 0.0
        self.peak = 1.0
        self.value = 1.0
        self.last_r = 0.0
        # history
        self.weights = []
        self.values = [1.0]
        self.perceived_risks = []

    def _perceived_risk(self, avg_recent_r):
        p = self.params
        loss_comp = max(-self.last_r, 0) * p.loss
        shock_comp = abs(self.last_r - avg_recent_r) * p.shock
        dd_comp = (self.peak - self.value) / (self.peak + 1e-9) * p.dd
        mem_comp = self.memory * p.mem_scale
        return loss_comp + shock_comp + dd_comp + mem_comp

    def step(self, r_today, recent_returns):
        """recent_returns: returns up to and including yesterday."""
        p = self.params

        # ----- morning: form perceived risk from experience so far -----
        self.peak = max(self.peak, self.value)
        avg_recent = float(np.mean(recent_returns[-10:])) if len(recent_returns) else 0.0
        self.memory = self.memory * p.mem_decay + max(-self.last_r, 0)
        risk = self._perceived_risk(avg_recent)
        weight = float(np.clip(1.0 / (1.0 + risk * p.rs), 0.05, 1.0))

        # ----- day happens: bear the consequence -----
        self.value = self.value * (1 + weight * r_today)

        # ----- record -----
        self.weights.append(weight)
        self.values.append(self.value)
        self.perceived_risks.append(risk)
        self.last_r = r_today
        return weight

    def run(self, returns):
        returns = np.asarray(returns, dtype=float)
        for t in range(len(returns)):
            self.step(returns[t], returns[max(0, t - 10):t])
        return {
            'weights': np.array(self.weights),
            'values': np.array(self.values),
            'perceived_risks': np.array(self.perceived_risks),
        }

    def get_metrics(self):
        """Financial metrics (same definitions as the classical agent)."""
        values = np.array(self.values)
        weights = np.array(self.weights)
        n = len(weights)
        daily = np.diff(values) / values[:-1]

        total_ret = (values[-1] / values[0] - 1) * 100
        years = n / 252
        ann_ret = ((values[-1] / values[0]) ** (1 / years) - 1) * 100 if years > 0 else 0.0
        ann_vol = np.std(daily) * np.sqrt(252) * 100
        sharpe = ann_ret / max(ann_vol, 0.01)
        peak = np.maximum.accumulate(values)
        max_dd = np.max((peak - values) / (peak + 1e-9)) * 100

        return {
            'total_return_%': round(total_ret, 2),
            'annualized_return_%': round(ann_ret, 2),
            'annualized_vol_%': round(ann_vol, 2),
            'sharpe_ratio': round(sharpe, 3),
            'max_drawdown_%': round(max_dd, 2),
            'avg_exposure_%': round(weights.mean() * 100, 1),
        }

    def get_welfare_metrics(self):
        """The experiential axis — what the classical agent cannot report."""
        risks = np.array(self.perceived_risks)
        if len(risks) == 0:
            return {}
        thresh = np.percentile(risks, 90)  # high-stress threshold, own distribution
        high = risks > thresh

        # mean length of consecutive high-stress runs
        runs, cur = [], 0
        for h in high:
            if h:
                cur += 1
            elif cur:
                runs.append(cur)
                cur = 0
        if cur:
            runs.append(cur)

        return {
            'baseline_stress': round(float(risks.mean()), 4),
            'stress_volatility': round(float(risks.std()), 4),
            'peak_stress': round(float(risks.max()), 4),
            'time_in_stress_%': round(float(high.mean()) * 100, 1),
            'mean_stress_episode_days': round(float(np.mean(runs)), 1) if runs else 0.0,
            'current_stress': round(float(risks[-1]), 4),
        }


if __name__ == '__main__':
    rng = np.random.default_rng(42)
    agent = CognitiveAgent()
    agent.run(rng.normal(0.0003, 0.01, 504))
    print("CognitiveAgent self-test:", agent.get_metrics())
    print("Welfare:", agent.get_welfare_metrics())
