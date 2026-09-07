# Modelling Investor Irrationality

## Research Update for Richard

*Where the project stands, what we have learned, and what comes next*

Richard — this is a simple overview of the project so you can quickly understand the idea, the work completed so far, the results we have, and the remaining work before the symposium paper is finished.

## 1. The project in one minute

The paper is titled **“Modelling Investor Irrationality.”** The basic idea is to ask whether we can represent some well-known behavioral-finance mechanisms inside a computational investor, and then see how the decisions of that investor compare with simpler investment rules and with real professional sector recommendations.

We are not trying to prove that financial advisors are irrational. The more defensible question is: **do professional sector recommendations sometimes look more like the output of a path-dependent behavioral model than the output of simple volatility management or trend-following?**

## 2. The three investment agents

| Agent | Simple question it asks | Role in the research |
|---|---|---|
| Classical | How volatile is this asset? | Mechanical risk-management benchmark. |
| Momentum | Has this asset been trending upward or downward? | Checks whether simple trend-following can explain the same behavior. |
| Cognitive | How risky does this market experience feel given losses, surprises, drawdown, and remembered losses? | Main behavioral model being studied. |

The momentum agent is especially important. If the cognitive agent resembles professional advice, we need to know whether that similarity is genuinely associated with the richer behavioral state or whether a much simpler rule—following recent winners and losers—could produce the same result.

## 3. What makes the cognitive agent “cognitive”?

Its perceived-risk state contains four stylized components:

- **Loss sensitivity:** negative returns matter more strongly than comparable positive outcomes.
- **Surprise/shock:** unusual market moves increase perceived risk.
- **Drawdown/reference dependence:** being below a previous peak affects perceived risk.
- **Memory:** previous losses continue to influence the agent for a period of time rather than disappearing immediately.

An important result from our own model diagnostics is that drawdown is by far the dominant component. Roughly **62–76% of average perceived risk** comes from the drawdown term across sectors. So the implemented model is best understood as a **reference-dependent, drawdown-sensitive behavioral risk model with memory**—not as a claim that all four psychological mechanisms contribute equally.

## 4. What data are we using?

The market side uses SPY plus the 11 major U.S. sector ETFs. We run the different agents over historical returns and examine their exposures, conventional financial performance, cognitive stress/perceived risk, component shares, ablation tests, and the relationship between cognitive and momentum behavior.

For the human comparison, we froze a small two-institution case study: **Charles Schwab and Wells Fargo Investment Institute**. We collected four dated sector-outlook snapshots from each institution, covering 11 sectors. That gives **8 advisor snapshots and 88 institution-date-sector observations**.

## 5. How the human-advisor comparison works

Each published advisor stance is converted to a standardized ordinal score while keeping the original wording. For every publication date, we reconstruct all model rankings using only market information that was available on or before that date. This prevents look-ahead bias.

We then compare the advisor’s sector ranking with each model. The main statistic is **Spearman rank correlation**: a higher positive value means the model orders sectors more similarly to the advisor. We also use **mean absolute rank distance (MARD)**, where lower is better, plus top-three and bottom-three agreement.

## 6. What we have found so far

| Primary model | Mean Spearman correlation | Mean rank distance (MARD) |
|---|---:|---:|
| **Cognitive** | **0.284** | **2.909** |
| Momentum A | 0.224 | 3.159 |
| Classical | -0.044 | 3.852 |

Across the pooled eight advisor snapshots, the cognitive agent is currently the closest of the three primary models: it has the highest average rank correlation and the lowest average rank distance. This gives **qualified support** to the main hypothesis.

But the result is not universal. For **Schwab**, the cognitive model is clearly the strongest match. For **Wells Fargo**, the momentum model is slightly stronger. This institutional difference is important: it suggests professional advice is not behaviorally homogeneous, and it prevents us from making an exaggerated claim that the cognitive model explains every advisor.

## 7. What the result means — and does not mean

### What we can reasonably say

- The cognitive agent behaves differently from a simple volatility-targeting model.
- The cognitive agent is related to momentum but is not simply identical to it.
- In the pooled Schwab/Wells Fargo sample, the cognitive ranking resembles professional sector recommendations more closely than the two primary benchmarks.
- The strength of that relationship differs by institution.

### What we cannot claim

- That Schwab or Wells Fargo is irrational.
- That similarity proves the advisors are actually thinking through loss aversion, drawdown, or memory.
- That the two institutions represent all professional advisors.
- That the cognitive model is a validated psychological measurement instrument.
- That the cognitive strategy is a superior trading strategy.

## 8. Why the project still matters

The interesting contribution is not simply whether the cognitive agent “wins.” The project creates competing explanations for investment behavior and tests them against the same observations. Volatility targeting represents mechanical risk management; momentum represents a simple trend-based explanation; the cognitive agent adds a persistent behavioral state. The advisor comparison then asks which of these simplified mechanisms produces sector preferences most similar to observed professional recommendations.

The fact that momentum performs well—especially for Wells Fargo—actually strengthens the research design because it stops us from automatically attributing every dynamic recommendation to psychology.

## 9. Literature foundation completed

We have also built the theoretical literature framework. The core sources include Kahneman and Tversky on prospect theory and reference dependence; Barberis, Huang, and Santos on prior investment outcomes and state-dependent risk attitudes; Jegadeesh and Titman on momentum; Grinblatt and Han on the connection between reference dependence and momentum; research on behavioral patterns among professional investors; and computational-finance literature supporting the use of programmed investment agents.

## 10. Where we are in the project

| Task | Status | What it accomplished |
|---|---|---|
| 1. Freeze methodology | Complete | Defined the advisor comparison before seeing the final results. |
| 2. Advisor dataset + quantitative comparison | Complete | Built the 88-observation dataset and ran the 11-sector model comparison. |
| 3. Paper narrative | Complete | Locked the argument, paper structure, claims, limitations, figures, and tables. |
| 4. Literature framework | Complete | Mapped the model mechanisms and controls to the core academic literature. |
| 5. Draft the paper | **Next** | Turn the completed research design and results into the actual symposium paper. |

## 11. What comes next

1. Merge/lock the completed research branches and preserve the current methodology and results.
2. Draft the Introduction and Behavioral Motivation / Model Design sections using the literature framework.
3. Write the Data and Empirical Design section so another reader can understand exactly how the experiment was run.
4. Turn the existing computational outputs and advisor comparison into the Results section, including a clean advisor-similarity figure/table.
5. Write the Discussion and Limitations with special attention to drawdown dominance, momentum as a competing explanation, and the small two-institution advisor sample.
6. Finish the Abstract and Conclusion only after the body of the paper is stable.
7. Convert the paper into a concise symposium presentation: question → agents → mechanism → advisor test → result → limitations → conclusion.

## 12. The simplest way to describe the project

**We built three simplified investors: one reacts to volatility, one follows market trends, and one carries a behavioral risk state based on losses, surprises, drawdowns, and memory. We then asked which model’s sector preferences most closely resemble dated recommendations from Schwab and Wells Fargo. The behavioral model is the strongest match overall, especially for Schwab, but momentum is competitive and slightly stronger for Wells Fargo. So the evidence is consistent with behavioral influences in some professional advice, but it does not prove that advisors are irrational.**

*Current stage: research design and analysis substantially complete; paper drafting is next.*