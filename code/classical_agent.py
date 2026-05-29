"""
Based on: Markowitz (1952), Modern Portfolio Theory
Simple rule: weight = target_volatility / rolling_volatility
"""

import numpy as np
import pandas as pd


class ClassicalAgent:
  

    def __init__(self, target_vol=0.10, window=20):
      
      
        self.target_vol = target_vol
        self.window = window
        self.weights = []
        self.values = [1.0]
        self.exposures = []

    def run(self, returns):
      
        returns = np.array(returns)

        for t in range(len(returns)):
            # Get recent returns (rolling window)
            start_idx = max(0, t - self.window + 1)
            recent = returns[start_idx:t+1]

            # Compute rolling volatility (standard deviation)
            rolling_vol = np.std(recent)
            if rolling_vol < 0.001:
                rolling_vol = 0.001  # avoid division by zero

            # Volatility targeting: higher vol → lower weight
            # weight = target_volatility / current_volatility
            weight = self.target_vol / rolling_vol
            weight = np.clip(weight, 0.05, 1.0)  # keep in [0.05, 1.0]

            self.weights.append(weight)
            self.exposures.append(weight * 100)

            # Update portfolio value
            # new_value = old_value * (1 + weight * return)
            current_value = self.values[-1]
            new_value = current_value * (1 + weight * returns[t])
            self.values.append(new_value)

        return {
            'weights': np.array(self.weights),
            'values': np.array(self.values),
            'exposures': np.array(self.exposures),
        }

    def get_metrics(self, returns):
      
        returns = np.array(returns)
        values = np.array(self.values)
        weights = np.array(self.weights)

        n = len(returns)
        daily_returns = np.diff(values) / values[:-1]

        # Total return
        total_ret = (values[-1] / values[0] - 1) * 100

        # Annualized return (assuming 252 trading days/year)
        years = n / 252
        ann_ret = ((values[-1] / values[0]) ** (1/years) - 1) * 100 if years > 0 else 0

        # Annualized volatility
        ann_vol = np.std(daily_returns) * np.sqrt(252) * 100

        # Sharpe ratio (assuming 0% risk-free rate for simplicity)
        sharpe = ann_ret / max(ann_vol, 0.01)

        # Maximum drawdown
        peak = np.maximum.accumulate(values)
        drawdown = (peak - values) / (peak + 1e-9) * 100
        max_dd = np.max(drawdown)

        # Average exposure
        avg_exp = np.mean(weights) * 100

        return {
            'total_return_%': round(total_ret, 2),
            'annualized_return_%': round(ann_ret, 2),
            'annualized_vol_%': round(ann_vol, 2),
            'sharpe_ratio': round(sharpe, 3),
            'max_drawdown_%': round(max_dd, 2),
            'avg_exposure_%': round(avg_exp, 1),
        }


if __name__ == '__main__':
    # Quick self-test
    print("Testing ClassicalAgent...")
    rng = np.random.default_rng(42)
    test_returns = rng.normal(0.0001, 0.01, 252)

    agent = ClassicalAgent(target_vol=0.10, window=20)
    result = agent.run(test_returns)
    metrics = agent.get_metrics(test_returns)

    print("\nTest Results:")
    for key, val in metrics.items():
        print(f"  {key}: {val}")
    print("\n✓ Agent working correctly")
