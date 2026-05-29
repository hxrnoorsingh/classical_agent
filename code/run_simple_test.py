"""
Using simple generated data to test the classical agent code works end to end. The test CSV can be replaced with
real data.
"""

import pandas as pd
import numpy as np
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from classical_agent import ClassicalAgent


def main():
   

    print("="*60)
    print("CLASSICAL AGENT - SIMPLE TEST RUN")
    print("="*60)


    data_file = Path(__file__).parent.parent / 'data' / 'test_data.csv'
    print(f"\nLoading {data_file}...")

    try:
        df = pd.read_csv(str(data_file), index_col=0, parse_dates=True)
    except:
        df = pd.read_csv(str(data_file))

    prices = df['Close'].values
    returns = np.diff(prices) / prices[:-1]

    print(f"✓ Loaded {len(returns)} days of data")
    print(f"  Start: {prices[0]:.2f}")
    print(f"  End:   {prices[-1]:.2f}")
    print(f"  Return: {(prices[-1]/prices[0]-1)*100:.2f}%")

  
    print(f"\nRunning classical agent...")
    agent = ClassicalAgent(target_vol=0.10, window=20)
    result = agent.run(returns)
    metrics = agent.get_metrics(returns)

    # Printing results
    print(f"\nRESULTS:")
    print(f"  Total Return:        {metrics['total_return_%']:+.2f}%")
    print(f"  Annualized Return:   {metrics['annualized_return_%']:+.2f}%")
    print(f"  Annualized Volatility: {metrics['annualized_vol_%']:.2f}%")
    print(f"  Sharpe Ratio:        {metrics['sharpe_ratio']:.3f}")
    print(f"  Max Drawdown:        {metrics['max_drawdown_%']:.2f}%")
    print(f"  Average Exposure:    {metrics['avg_exposure_%']:.1f}%")

    # Saving results
    os.makedirs('../results', exist_ok=True)
    output_file = '../results/test_run_results.json'
    with open(output_file, 'w') as f:
        json.dump(metrics, f, indent=2)

    print(f"\n✓ Results saved to {output_file}")
    print("\n" + "="*60)
    print("NEXT STEP")
    print("="*60)
   


if __name__ == '__main__':
    main()
