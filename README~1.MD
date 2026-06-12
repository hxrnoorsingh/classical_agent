When markets are volatile, reduce exposure. When calm, stay invested
When market volatility is high → reduce exposure  
When market volatility is low → increase exposure



to run it yourself use this :

cd classical_agent
python code/run_simple_test.py

this is the output it gives as of now :

CLASSICAL AGENT - SIMPLE TEST RUN


Loading data/test_data.csv...
✓ Loaded 100 days of data
  Start: $100.00
  End:   $98.55
  Return: -1.45%

Running classical agent...

RESULTS:
  Total Return:        -1.45%
  Annualized Return:   -3.62%
  Annualized Volatility: 14.72%
  Sharpe Ratio:        -0.246
  Max Drawdown:        9.90%
  Average Exposure:    100.0%

✓ Results saved to results/test_run_results.json
```

✓ If you see this, **code is working**

---




This is the decision rule as per the source: 

For each day:
1. Measure volatility of last 20 days
2. Compute weight = 10% / volatility
3. Clip to stay in [5%, 100%] range
4. Apply weight to market return
5. Update portfolio value
